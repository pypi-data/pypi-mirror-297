from __future__ import annotations

import argparse
import csv
import json
import logging
import re
from abc import ABC
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Iterable, Mapping, Literal

import numpy as np

from chemtrayzer.core.chemid import InchiReadWriteError, Reaction, Species
from chemtrayzer.core.coords import Geometry, InvalidXYZFileError, TSGeometry
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.md import (
    BAROSTATS,
    THERMOSTATS,
    BoxType,
    MDIntegrator,
    MDJob,
    MDJobFactory,
    MDMetadata,
    TrajectoryParser,
)
from chemtrayzer.engine.cmdtools import (
    CommandLineInterface,
    IllegalCmdArgsError,
    IllegalConfigError,
    TypeConversionError,
    UserError,
    dict2dataclass,
)
from chemtrayzer.engine.investigation import Investigation, InvestigationContext
from chemtrayzer.engine.jobsystem import Memory
from chemtrayzer.io.fileutils import unique_file
from chemtrayzer.jobs.ams import AMSTrajectoryParser
from chemtrayzer.jobs.lammps import Lammps, LammpsReaxFFJobFactory, LammpsTrajParser
from chemtrayzer.jobs.mdbox import MDBoxJob, MDBoxJobFactory
from chemtrayzer.reaction_sampling.reaction_detection import (
    NVTRateConstants,
    ReactionDetector,
)


class MDReactionSamplingInvestigation(Investigation):
    '''
    A workflow similar to CTY version 1.0. An MD trajectory is created unless provided, and analyzed to find reactions and NVT rate coefficients.
    This investigation either takes a trajectory parser and analyzes the contained trajectory, or takes a MDJob factory to produce the trajectory.
    In case of providing the MDJob factory, Options.metadata must be set too and there must be an initial box geometry, either via
    Options.initial_geometry or by providing .packmolpath and .initial_composition in Options.
    :param options: Various options for running and analyzing the MD simulation.
    :param trajectoryparser: A parser object that provides the MD trajectory. If mdjobfactory is set to None, a trajectory parser is mandatory.
    :param mdjobfactory: An MDJobFactory object that provides an MDJob. If MDJobFactory is given, options.metadata is mandatory, and any trajectoryparser will be ignored.
    '''
    # type hint: more specific than Investigation.Result
    result: Result

    @dataclass
    class Options:
        metadata: MDMetadata = None
        '''Description and options for the MD simulation. If MDMetadata is set to None, no MD is started.'''
        initial_geometry: Geometry = None
        '''pre-filled initial box'''
        initial_composition: Iterable[tuple[Species|Geometry, int]] = None
        '''number of structure/species to put into the simulation box for each structure/species (only if initial_geometry is not provided)'''
        packmolpath: str = None
        '''path to packmol exe'''
        bond_initial_threshold: float = 0.5
        '''In the first frame, bonds with bond orders below are regarded as non-existent.'''
        bond_breaking_threshold: float = 0.3
        '''Bonds are regarded as breaking if their bond order drops below this value.'''
        bond_forming_threshold: float = 0.8
        '''Bonds are regarded as forming if their bond order rises above this value.'''
        molecule_stable_time: float = 3
        '''For recrossing. Minimum lifetime in fs to mark molecules as stable.
        Stable molecules can serve as reactants and products, unstable molecules are regarded as intermediates.'''
        reaction_path_margin: int = 20
        '''For reaction paths. Number of geometries to save as reaction path before and after a reaction event.'''
        calculate_nvt_rate_coeffs: bool = True
        '''toggle the computation of canonical ensemble rate coefficients (NVT)'''
        confidence: float = 0.9
        '''confidence interval for the rate coefficient error bounds (0...1)'''
        start: float = 0.0
        '''time of the trajectory to start the rate coefficient analysis from'''



    @dataclass
    class Result(Investigation.Result):
        species: set[Species] = None
        '''set of detected species'''
        reactions: set[Reaction] = None
        '''set of detected reactions'''
        geometries: Mapping[Reaction| Species, Geometry] = None
        '''Geometries of species and transistion states in a dictionary with species and reactions as keys'''
        reaction_paths: Mapping[Reaction, list[TSGeometry]] = None
        '''Geometries of reaction paths in a dictionary with reactions as keys'''
        reactions_by_time: Mapping[float, list[Reaction]] = None
        '''dictionary of reactions sorted by time of occurence'''
        nvtrates: Mapping[Reaction, tuple[float, float, float, int]] = None
        '''rate constat, lower bound, upper bound and number of occurances for
        each reaction [(cm^3/mol)^(n-1) 1/s] (see Kröger et al. J. Chem. Theory Comput. 2017
        https://doi.org/10.1021/acs.jctc.7b00524)'''

    def __init__(self,
                 options: Options,
                 trajectoryparser: TrajectoryParser = None,
                 mdjobfactory: MDJobFactory = None):
        super().__init__()

        # arguments
        self.trajectory_parser = trajectoryparser
        self.mdjobfactory = mdjobfactory
        self.options: MDReactionSamplingInvestigation.Options = options

        # temporary variables
        self._initial_composition: Mapping[Species, int] = None
        self.timestep = None
        self.volume = None
        self.initial_geometry = None
        self.reactions_by_time = None

        # results
        self.result = self.Result()

        # start
        self.check_options()

    def check_options(self):
        """
        Sanity check on the given options. Also, a descision whether to run an MD or take a finished trajectory.
        When running a MD, either the initial geometry must be given or the info how to create it via a MDBoxJob.
        """
        # decision whether to run MD or just take a finished trajectory
        # when running a MD, either the initial geometry is given or the info how to create it via a MDBoxJob.

        if self.mdjobfactory is None:
            # then use a finished trajectory

            # trajectoryparser must be there
            if self.trajectory_parser is None:
                raise ValueError('Neither an MDJobFactory nor a trajectory parser was provided.')

            # next step is reaction sampling using self.trajectoryparser
            self.add_step(self.reaction_sampling)

        else:
            # then start an MD with the provided metadata and initial_geometry

            # metadata is mandatory then
            if self.options.metadata is None:
                raise ValueError('An MDJobFactory was given, but no MD metadata was provided.')
            if self.options.metadata.box_type != BoxType.ORTHOGONAL:
                raise ValueError('This investigation can only handle orthogonal boxes.')
            if self.options.metadata.barostat is not None:
                raise ValueError('This investigation does not support barostats.') # currently only constant volume simulations!

            if self.options.initial_geometry is None:
                # then start a MDBoxJob to get the initial_geometry

                # options must contain this info
                if self.options.packmolpath is None:
                    raise ValueError('A MDBoxJob was requested, but no packmol path was provided.')
                if self.options.initial_composition is None:
                    raise ValueError('A MDBoxJob was requested, but no initial species were provided.')
                if self.options.metadata.box_vectors is None:
                    raise ValueError('A MDBoxJob was requested, but no lattice vectors were provided.')
                if len(self.options.metadata.box_vectors) != 3:
                    raise NotImplementedError('This investigation can only handle cubic boxes.')

                # next step is to make a box using self.options.metadata etc
                self.add_step(self.make_mdbox)

            else:
                # then just use the initial_geometry from the options
                # self.mdjobfactory != None
                # self.options.initial_geometry != None

                # next step is to get and run the job from self.mdjobfactory
                self.add_step(self.run_md)

    def make_mdbox(self):
        """
        Run the MD box job, if requested.
        """
        species_geometries = [
            Geometry.from_inchi(mol.inchi)
                if isinstance(mol, Species)
                else mol    # assume geometry, if not species
            for mol, count in self.options.initial_composition]

        assert self.options.metadata.box_type == BoxType.ORTHOGONAL

        # box is defined by two corners diagonal to each other. The first one
        # is the origin, the second one is the origin shifted by the box vectors
        near_corner = (np.array(self.options.metadata.box_origin)
                        if self.options.metadata.box_origin is not None
                        else np.zeros(3))
        far_corner = near_corner + np.sum(self.options.metadata.box_vectors, axis=1)
        box_dim = (*near_corner, *far_corner)

        mdboxjobfactory = MDBoxJobFactory(self.options.packmolpath)
        mdboxjob = mdboxjobfactory.create(
            'packmol',
            species_geometries,
            [count for _, count in self.options.initial_composition],
            box_dim,
        )
        self.add_step(self.run_md)
        self.wait_for_and_submit(mdboxjob)

    def run_md(self, boxjob: MDBoxJob = None):
        """
        Run the MD simulation.
        :param boxjob: optional, if a new simulation was requested, the Md box job will be passed here.
        """
        self.initial_geometry = self.options.initial_geometry
        # if a box job has run, use it to create an MD job
        if boxjob is not None:
            if boxjob.is_failed:
                self.fail('the MD box job was not successful')
            self.initial_geometry = boxjob.result.box

        mdjob = self.mdjobfactory.create(
            metadata=self.options.metadata,
            initial_geometry=self.initial_geometry,
            name='main_md_simulation',
        )

        self.add_step(self.reaction_sampling)
        self.wait_for_and_submit(mdjob)

    def reaction_sampling(self, mdjob: MDJob = None):
        """
        Do the analysis of the trajectory. Detect reactions and species, extract geometries for species and reactions.
        :param mdjob: optional, if the investigation started an MDJob it will be passed here.
        """

        # if an MD job has run, take the trajectory parser from there
        if mdjob is not None:
            if mdjob.is_failed:
                self.fail('the MD job was not successful')
            self.trajectory_parser = mdjob.result

        # parse the trajectory
        trajectory = self.trajectory_parser.parse()
        self.timestep = trajectory.metadata.timestep
        if trajectory.metadata.barostat is not None:
            raise ValueError('This investigation does not support barostats.')
        self.volume = trajectory.cell_volume(n=0)

        # detect reactions and extract geometries
        detector = ReactionDetector(trajectory,
                                    self.options.bond_initial_threshold,
                                    self.options.bond_breaking_threshold,
                                    self.options.bond_forming_threshold,
                                    self.options.molecule_stable_time,
                                    self.options.reaction_path_margin)
        detector.detect()

        # if the detection failed, exit and leave all results at None
        if detector.species is None:
            self.fail('The reaction detection could not find any species.')

        self._initial_composition = dict(Counter(detector.initial_species))
        self.reactions_by_time = detector.reactions_by_time

        self.result.species = detector.species
        self.result.reactions = detector.reactions
        self.result.reactions_by_time = detector.reactions_by_time
        self.result.reaction_paths = detector.reaction_paths
        self.result.geometries = detector.geometries

        # decide whether to calculate NVT rate coefficients
        if self.options.calculate_nvt_rate_coeffs:
            self.add_step(self.mdrates)
        else:
            # finished
            self.succeed()

    def mdrates(self):
        """
        Estimate Arrhenius parameters for the detected reactions.
        """
        # compute and save rate coefficients
        nvtrates = NVTRateConstants(self._initial_composition,
                                    self.reactions_by_time,
                                    self.timestep,
                                    self.volume,
                                    self.options.confidence,
                                    self.options.start)
        nvtrates.compute()
        self.result.nvtrates = nvtrates.compact_result()

        # jump to end
        self.succeed()

class MDReactionSamplingCLI(CommandLineInterface, ABC):
    """base class for the CLI commands of the MDReactionSamplingInvestigation"""
    CONFIG_TYPE = 'toml'

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        super().add_cmd_args(parser)
        # TODO CHEMKIN output + Species dict
        # parser.add_argument(
        #     '-ock', '--output-chemkin',
        #     type=Path, action='store', dest='o_chemkin',
        #     help='path to which the chemkin output should be  stored, e.g., '
        #          'mech.chemkin')
        # parser.add_argument(
        #     '-oinchi', '--output-inchi',
        #     type=Path, action='store', dest='o_inchi',
        #     help='file in which the InChIs of the discovered  species should be'
        #     ' stored, e.g. species.json')
        parser.add_argument(
            '-ojson', '--output-json',
            type=Path, action='store', dest='o_json',
            help='file in which the reaction paths should be stored. '
                 'The file will contain a field "species" with the InChIs of the discovered species, '
                 'a field "reactions" with the reactions, a field "reaction_times" with the times of reaction events '
                 'in femto seconds and the (zero-based) id of the observed reactions in the list, '
                 'and a field "nvt_rates" with the rate constant, a lower and upper bound and the number of observed '
                 'events for each reaction. Note: Since not all time steps are written to the output file, '
                 'all reactions that occur within the output interval are listed for a single time step.')
        parser.add_argument(
            '-ocsv', '--output-csv',
            type=Path, action='store', dest='o_csv', default='out.csv',
            metavar='FILE',
            help='Creates two files FILE_events.csv and FILE_reactions.csv [default: %(default)s -> out_events.csv, out_reactions.csv]. The latter contains the rows reaction_id, reverse_id, reactants, products, "k [(cm^3/mol)^(n-1) 1/s]", k_low, k_high, number_of_events. The former contains the rows step, and reaction_id. reaction_id contains a unique number for each type of reaction (as determined by the products and reactants). reverse_id contains the id of the reverse reaction, reactants and products contain a list of InChIs each. "k [(cm^3/mol)^(n-1) 1/s]", k_low, and k_high contain the calculated Arrhenius rate based on the MD simulation, a lower bound, and an upper bound, respectively. number_of_events contains the total number of observed events for this type of reaction. step contains the point in the trajectory where the reaction with the given id was observed. Note that, the columns step and reaction_id in the _events.csv file are not unique, if multiple reactions were observed between two steps or if a reaction occurred multiple times.')

        # since config is already in the parent class, we need to access the
        # action to change the default
        config_action = next(a for a in parser._actions if a.dest == 'config')
        config_action.default = 'config.toml'

    def check_cmd_args(self, cmd_args: argparse.Namespace):
        super().check_cmd_args(cmd_args)
        if cmd_args.o_csv.is_dir():
            raise IllegalCmdArgsError(f'{cmd_args.o_csv} is a directory. '
                                      'Provide a file path.')
        if cmd_args.o_json is not None and cmd_args.o_json.is_dir():
            raise IllegalCmdArgsError(f'{cmd_args.o_json} is a directory. '
                                      'Provide a file path.')
        if cmd_args.o_csv.suffix.lower() != '.json':
            logging.warning('The output file should have a .json suffix.')

    def _create_options(self, config: dict, cmd_args: argparse.Namespace):
        ''':return: MDReactionSamplingInvestigation.Options object'''
        # translation user input to field names of dataclass
        aliases = {
            'md': 'metadata',
            'metadata': {
                'box_size': 'box_vectors',
                'pbc': 'periodic_boundary_conditions',
                'thermostat': {}, # for storing __type__ later
                'barostat': {},
            }
        }

        # checking for the required options is done by the investigaiton, hence,
        # here we mainly deal with the translation of the toml file into the
        # dataclass
        if 'md' in config:
            if 'integration_method' in config['md']:
                try:
                    # translate dict values with MDIntegrator enum values
                    config['md']['integration_method'] = MDIntegrator(
                        config['md']['integration_method'])
                except ValueError as err:
                    raise IllegalConfigError(
                        f'{config["md"]["integration_method"]} is not a valid '
                        f'integration method. Choose from: {", ".join([i.value for i in MDIntegrator])}'
                    ) from err

            if 'thermostat' in config['md']:
                if 'type' not in config['md']['thermostat']:
                    raise IllegalConfigError('The thermostat type is missing in'
                                             ' the config file.')
                tname: str = config['md']['thermostat']['type'].lower()

                try:
                    aliases['metadata']['thermostat']['__type__']\
                                = THERMOSTATS[tname]
                # if key is not in THERMOSTATS we do not support it
                except KeyError as err:
                    raise IllegalConfigError(
                        f'Unknown thermostat type: {tname}. Allowed strings '
                        f'are: {", ".join(THERMOSTATS.keys())}'
                    ) from err

            if 'barostat' in config['md']:
                if 'type' not in config['md']['barostat']:
                    raise IllegalConfigError('The barostat type is missing in'
                                             ' the config file.')
                bname: str = config['md']['barostat']['type'].lower()
                try:
                    aliases['metadata']['barostat']['__type__']\
                                = BAROSTATS[bname]
                except KeyError as err:
                    raise IllegalConfigError(
                        f'Unknown barostat type: {bname}. Allowed strings '
                        f'are: {", ".join(BAROSTATS.keys())}'
                    ) from err

        try:
            opts = dict2dataclass(config,
                                  MDReactionSamplingInvestigation.Options,
                                  aliases=aliases)
        except TypeConversionError as err:
            raise IllegalConfigError(
                'Error while reading the config file: '
                f'Option {err.args[0]} has wrong type {err.args[2]}. Expected'
                f' type: {err.args[1]}'
            ) from err
        # value errors are most likely user errors, so we raise a UserError
        except ValueError as err:
            raise IllegalConfigError(
                f'Error while reading the config file: {err}'
            )
        except KeyError as err:
            raise IllegalConfigError(
                'Error while reading the config file: '
                f'Option {err.args[0]} is missing in the config file.'
            ) from err

        return opts

    def _result2json_dict(self, result: MDReactionSamplingInvestigation.Result)\
            -> dict:
        """convert the result of the investigation to a dictionary that can
        then be serialized to a JSON file
        """
        out = {}
        rxns_list: list[Reaction] = []    # reactions in the order of detection
        id_by_rxn = dict()
        rxn_times = defaultdict(list)  # reaction ids (as in rxns_list) by time
        rxn_by_time = (result.reactions_by_time
                       if result.reactions_by_time is not None
                       else {})
        species = list(result.species) if result.species else []
                        # use list to get consistent order

        for time, rxns in rxn_by_time.items():
            for r in rxns:
                if r not in id_by_rxn:
                    id_by_rxn[r] = len(id_by_rxn)
                    rxns_list.append(r)

                rxn_times[time].append(id_by_rxn[r])

        out['species'] = [s.inchi for s in species]
        out['reactions'] = [(list(species.index(s) for s in r.reactants),
                             list(species.index(s) for s in r.products))
                             for r in rxns_list]
        out['reaction_times'] = rxn_times
        if result.nvtrates is not None:
            out['nvt_rates'] = [result.nvtrates[r] for r in rxns_list]

        return out

    def _result2csv_lists(self,
            result: MDReactionSamplingInvestigation.Result)\
            -> tuple[list[tuple[int, int, str, str, float, float, float, int]],
                     list[tuple[int, int]]]:
        """create data structures for writing csv files"""
        if result.reactions is None:
            return [], []

        id_by_rxn = {rxn: i for i, rxn in enumerate(result.reactions)}
        rates = result.nvtrates if result.nvtrates is not None else {}
        rxn_rows = []
        events_rows = []

        for rxn in result.reactions:
            k, k_low, k_high, n = rates.get(rxn, (None, None, None, None))
            reverse_id = id_by_rxn.get(rxn.reverse(), "") # empty string if reverse reaction not detected
            row = (id_by_rxn[rxn],
                   reverse_id,
                   ';'.join(s.inchi for s in rxn.reactants),
                   ';'.join(s.inchi for s in rxn.products),
                   k, k_low, k_high, n)
            rxn_rows.append(row)

        for time, rxns in result.reactions_by_time.items():
            for rxn in rxns:
                events_rows.append((time, id_by_rxn[rxn]))

        return rxn_rows, events_rows

    def postprocessing(self, inves: MDReactionSamplingInvestigation,
                       cmd_args: argparse.Namespace):
        if inves.is_failed:
            logging.warning('The investigation failed. The output may be '
                            'incomplete!')

        if cmd_args.o_json is not None:
            json_path = unique_file(cmd_args.o_json)
            json_dict = self._result2json_dict(inves.result)

            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_dict, f, indent=2)

        csv_stem = cmd_args.o_csv.stem
        events_path = Path(f'{csv_stem}_events.csv')
        reactions_path = Path(f'{csv_stem}_reactions.csv')

        rxn_rows, events_rows = self._result2csv_lists(inves.result)

        with open(events_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')

            writer.writerow(("step", "reaction_id"))
            writer.writerows(events_rows)

        with open(reactions_path, 'w', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter=',', quotechar='"',
                                quoting=csv.QUOTE_NONNUMERIC, lineterminator='\n')

            writer.writerow(("reaction_id", "reverse_id", "reactants",
                             "products", "k [(cm^3/mol)^(n-1) 1/s]", "k_low",
                             "k_high", "number_of_events"))
            writer.writerows(rxn_rows)

class AnalyzeTrajCLI(MDReactionSamplingCLI):
    """CLI for the analysis of a trajectory (CTY 1.0 functionality)"""

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        super().add_cmd_args(parser)
        parser.add_argument(
            '-t', '--trajectory',
            type=Path,
            nargs = '+',
            action='store',
            dest='trajectory',
            required=True,
            help='trajectory to analyze. Please suppy either one *.rkf file from AMS or a combination of bond.dmp and custom.dmp files from LAMMPS.')

    def check_cmd_args(self, cmd_args: argparse.Namespace):
        super().check_cmd_args(cmd_args)

        traj_path: list = cmd_args.trajectory

        #assert the file exists and is a path object
        for path in traj_path:
            if not path.exists():
                raise IllegalCmdArgsError(f'File not found: {path.as_posix()}')
            if path.suffix not in ['.rkf', '.dmp']:
                raise IllegalCmdArgsError(f'Unsupported file type: {path.suffix}')

        if traj_path[0].suffix == '.rkf':
            assert len(traj_path) == 1, 'please only supply one AMS trajectory at a time'
        elif len(traj_path) == 2:
            assert traj_path[0].suffix == '.dmp' and traj_path[1].suffix == '.dmp', \
            'bond.dmp and custom.dump files are required. The order of the files does not matter.'
            required_files = ['bond.dmp', 'custom.dmp']
            for required_file in required_files:
                if required_file not in [file.name for file in traj_path]:
                    raise IllegalCmdArgsError(f'File {required_file} is missing. Check correct spelling. Supplied files are {", ".join([file.name for file in traj_path])}.')

        else:
            raise IllegalCmdArgsError("For ams simulations please specify a single .rkf trajectory file."
                                      "For lammps simulations please specify a bond.dmp and a custom.dmp file.")


    def _create_traj_parser(self, cmd_args: argparse.Namespace,
                            opts: MDReactionSamplingInvestigation.Options= None,
                            config: dict = None,)\
            -> TrajectoryParser:
        traj_path: list = cmd_args.trajectory

        # check if the program is specified in the config file
        if 'program' not in config['md']:
            raise IllegalConfigError('Please specify the program used to generate the trajectory in the config.toml file.\
                                      Currently supported programs are ams and lammps.')
        program: Literal['ams', 'lammps']  = config['md']['program']

        #AMS rkf files
        if program == "ams":
            return AMSTrajectoryParser(traj_path[0])
        # lammps dump files
        elif program == "lammps":
            # check if config has lammps section
            if 'lammps' not in config['md']:
                raise IllegalConfigError('No lammps section in the config file. Please specify the lammps section in the config.toml file.')

            # checks if required data is present
            if opts.metadata is None:
                raise IllegalConfigError('MD metadata is required for lammps simulations. Metadata is created based on the config.toml file.')
            required_metadata = ['number_of_steps', 'box_vectors', 'periodic_boundary_conditions', 'sampling_frequency', 'timestep']
            missing_metadata = [key for key in required_metadata if opts.metadata.__dict__.get(key) is None]
            if missing_metadata:
                raise IllegalConfigError(f'MD Metadata is missing the following data: {", ".join(missing_metadata)}. Metadata is created based on the config.toml file.')

            # either use atom types or atom type mapping from the config
            if 'atom_types' not in config['md']['lammps']:
                assert config['md']['lammps']['atom_type_mapping'] is not None, 'Config does not contain atom types nor atom_type_mapping,\
                                                                                one of which must me specified.'
                atom_type_mapping = config['md']['lammps']['atom_type_mapping']
                atom_types = None
            else:
                atom_type_mapping = None
                atom_types = tuple([PTOE[type] for type in config['md']['lammps']['atom_types']])

            custom_dump_path = traj_path[0] if traj_path[0].name == 'custom.dmp' else traj_path[1]
            bond_path = traj_path[0] if traj_path[0].name == 'bond.dmp' else traj_path[1]

            traj_parser = LammpsTrajParser(bond_path=bond_path, custom_dump_path=custom_dump_path, metadata = opts.metadata,
                                           atom_types=atom_types, atom_type_mapping=atom_type_mapping)
            return traj_parser
        else:
            raise NotImplementedError(f'Program {program} is not supported. Check config.toml.')


    def create_investigation(self, _: InvestigationContext,
                            config: dict,
                            cmd_args: argparse.Namespace)\
                            -> MDReactionSamplingInvestigation:
        opts = self._create_options(config, cmd_args)
        self._traj_parser = self._create_traj_parser(cmd_args, config=config, opts=opts)

        try:
            return MDReactionSamplingInvestigation(
                            options=opts,
                            trajectoryparser=self._traj_parser)
        # when an option does not pass the check, a ValueError is raised
        except ValueError as err:
            raise IllegalConfigError(
                f'Error while checking the configuration: {err.args[0]}'
            ) from err

class RunMDCLI(MDReactionSamplingCLI):

    def add_cmd_args(self, parser: argparse.ArgumentParser):
        super().add_cmd_args(parser)
        group = parser.add_mutually_exclusive_group(required=True)
        group.add_argument(
            '-g', '--geometry',
            type=str,
            nargs=1,
            action='store',
            metavar='FILE',
            dest='geometry',
            help='Initial geometry of the box. (*.xyz)')
        group.add_argument(
            '-c', '--composition',
            type=str,
            action='store',
            nargs='*',
            metavar='MOL1 COUNT1',
            dest='box',
            help='Initial composition of the box. For each molecular structure the count of molecules that should be put into the box must be given. The structure can be defined by an InChI or an *.xyz file, e.g. -c "InChI=1S/O2/c1-2" 10 ./pentane.xyz 1. When using this argument, add -- at the end of the list to avoid reading in the workspace path as additional molecule.')

    def check_cmd_args(self, cmd_args: argparse.Namespace):
        super().check_cmd_args(cmd_args)

        self.__extract_geometries_from_cmd_args(cmd_args)

    def __extract_geometries_from_cmd_args(self, cmd_args: argparse.Namespace)\
            -> tuple[Geometry, list[tuple[Species, int]]]:
        """If --box was set, self.__inital_composition will be a list of
        tuples with the molecular structure and the count of molecules that
        should be put into the box. If --geometry was set,
        self.__initial_geometry will be the initial geometry of the box."""
        if hasattr(cmd_args, 'box') and cmd_args.box is not None:
            self.__inital_composition = []
            self.__initial_geometry = None
            if len(cmd_args.box)%2:
                raise IllegalCmdArgsError(
                        'Number of arguments for --composition must be even. '
                        'Provide a count for each molecular '
                        'structure. For supplying the initial starting geometry'
                        ' directly use --geometry.')

            for mol, count in zip(*[iter(cmd_args.box)]*2, strict=True):
                count: str
                mol: str = mol.strip()

                if re.match(r'^InChI=1S/.*', mol):
                    try:
                        mol = Species.from_inchi(mol)
                    except InchiReadWriteError as err:
                        raise IllegalCmdArgsError(
                            f'Invalid InChI: {mol}'
                        ) from err
                else:
                    p = Path(mol)
                    if p.suffix != '.xyz':
                        raise IllegalCmdArgsError(
                                f'Not a *.xyz file: {p}')
                    elif not p.exists():
                        raise IllegalCmdArgsError(
                                f'File not found: {p}')
                    else:
                        mol = Geometry.from_xyz_file(p, comment=False)

                try:
                    count = int(count)
                except ValueError as err:
                    raise IllegalCmdArgsError(
                        'Molecular structure counts must be integers.'
                    ) from err

                self.__inital_composition.append((mol, count))
        else:  # --geometry set
            try:
                self.__initial_geometry = Geometry.from_xyz_file(
                                                *cmd_args.geometry,
                                                comment=False)
            except FileNotFoundError as err:
                raise IllegalCmdArgsError(
                    f'File not found: {cmd_args.geometry}'
                ) from err
            except InvalidXYZFileError as err:
                raise IllegalCmdArgsError(
                    f'Invalid XYZ file "{cmd_args.geometry}": {err}'
                ) from err
            except Exception as err:
                # runtime error is not a user error and will lead to more
                # verbose error output
                raise IllegalCmdArgsError(
                    f'Error while reading the XYZ file: {err}'
                ) from err

            self.__inital_composition = None

    def __create_mdjob_factory(self, cmd_args: argparse.Namespace,
                               config: dict) -> MDJobFactory:
        if 'md' not in config:
            raise IllegalConfigError('No md section in the config file.')
        if 'program' not in config['md']:
            raise IllegalConfigError('MD program not specified in config file.')

        if str(config['md']['program']).lower() == 'lammps':
            if 'lammps' not in config['md']:
                raise IllegalConfigError('No lammps section in the config '
                                         'file.')

            try:
                n_cpus = config['md']['lammps']['n_cpus']
                runtime = config['md']['lammps']['runtime']
                n_tasks = config['md']['lammps']['n_tasks']
                memory = config['md']['lammps']['memory']
            except KeyError as err:
                raise IllegalConfigError(
                    f'Missing job parameter: md.lammps.{err.args[0]}'
                ) from err

            try:
                n_cpus = int(n_cpus)
            except ValueError as err:
                raise IllegalConfigError(
                    'Number of CPUs must be an integer.'
                ) from err
            try:
                n_tasks = int(n_tasks)
            except ValueError as err:
                raise IllegalConfigError(
                    'Number of tasks must be an integer.'
                ) from err
            if not bool(re.match(string=runtime, pattern=r'^\d+:\d+(?::\d+)?$')):
                raise IllegalConfigError(
                    r"Runtime must be provided in HH:MM[:SS] format."
                )
            else:
                runtime = runtime.split(':')
                seconds = int(runtime[2]) if len(runtime) == 3 else 0
                minutes = int(runtime[1])
                runtime = timedelta(hours=int(runtime[0]),minutes=minutes,
                                    seconds=seconds)

            memory = Memory(amount=memory, unit=Memory.UNIT_MB)

            lmp = Lammps(config['md']['lammps']['executable'])
            return LammpsReaxFFJobFactory(
                        reaxff_path=config['md']['lammps']['reaxff'],
                        lammps=lmp,
                        n_cpus=n_cpus,
                        runtime=runtime,
                        n_tasks=n_tasks,
                        memory=memory,
                        )

        elif config['md']['program'] == 'ams':
            if 'ams' not in config['md']:
                raise IllegalConfigError('No ams section in the config file.')

            raise NotImplementedError('AMS is not yet supported.')
            # TODO implement
        else:
            raise IllegalConfigError(
                f'Unknown MD program: {config["md"]["program"]}. '
                'Allowed strings are: "lammps", "ams"'
            )

    def create_investigation(self, _: InvestigationContext,
                            config: dict,
                            cmd_args: argparse.Namespace)\
                            -> MDReactionSamplingInvestigation:
        md_factory = self.__create_mdjob_factory(cmd_args, config)
        opts = self._create_options(config, cmd_args)

        if self.__inital_composition is not None:
            opts.initial_composition = self.__inital_composition
        elif self.__initial_geometry is not None:
            opts.initial_geometry = self.__initial_geometry
        else:
            # this should never happen -> probably a bug and not a user error
            raise RuntimeError('Neither initial composition nor initial geometry'
                               ' was set.')

        try:
            return MDReactionSamplingInvestigation(
                            options=opts,
                            mdjobfactory=md_factory)
        # when an option does not pass the check, a ValueError is raised
        except ValueError as err:
            raise IllegalConfigError(
                f'Error while checking the configuration: {err.args[0]}'
            ) from err
