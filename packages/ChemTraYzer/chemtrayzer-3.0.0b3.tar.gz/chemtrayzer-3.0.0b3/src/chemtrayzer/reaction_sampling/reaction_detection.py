import warnings
import logging
from collections import defaultdict
from typing import Dict, List, Set, Union
from chemtrayzer.core.graph import DirectedGraph, MolGraph

import networkx as nx
import numpy as np

from numpy import pi, arccos, clip, dot, all
from numpy.linalg import norm
from scipy.optimize import leastsq
from scipy.special import lambertw, gammaincc

import chemtrayzer.core.md
from chemtrayzer.core import chemid
from chemtrayzer.core.chemid import Species, Reaction
from chemtrayzer.core.coords import Geometry, TSGeometry
from chemtrayzer.core.md import BoxType, RateConstantRecord
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE


###############################################################################
# CTY Reaction Detection
###############################################################################


class ReactionDetector:
    """
        Class for detecting and extracting reactions and their geometries from a MD trajectory
        :param trajectory: CTY3 Trajectory object
        :type trajectory: chemtrayzer.core.md.Trajectory
        :param bond_initial_threshold: bonds with orders above this value are considered existing in the first frame of the trajectory
        :type bond_initial_threshold: float
        :param bond_breaking_threshold: bonds with orders decreasing below this value are considered breaking
        :type bond_breaking_threshold: float
        :param bond_forming_threshold: bonds with orders increasing above this value are considered forming
        :type bond_forming_threshold: float
        :param molecule_stable_time: detected molecules with lifetimes below this value are considered unstable intermediates in a reaction and are never reported as products
        :type molecule_stable_time: float
        :ivar mdmolecules: internally used list of detected molecules. Molecules have type MDMolecule, and are a container for the molecular graph and an unique id
        :ivar mdreactions: internally used list of detected reactions. Reactions are a 2-tuple of tuples of MDMolecules, reactants and products.
        :ivar initial_composition: the list of MDMolecules in the first frame of the trajectory
        :ivar reactions: set of detected reactions.
        :ivar species: set of detected species.
        :ivar geometries: geometries of the detected species and TS guesses, accessible with the species/reaction as key, and a list of geometries as value.
        :ivar reaction_paths: chain of geometries for reactions, accessible with the reaction as key, and a list of geometry lists as value.
        :ivar reactions_by_time: detected reactions ordered by time of the event. each time can have a list of reactions.
    """
    def __init__(self,
                 trajectory: chemtrayzer.core.md.Trajectory,
                 bond_initial_threshold: float = 0.5,
                 bond_breaking_threshold: float = 0.3,
                 bond_forming_threshold: float = 0.8,
                 molecule_stable_time: float = 3,
                 reaction_path_margin = 20):
        # sanity check
        if trajectory.metadata.box_type != BoxType.ORTHOGONAL:
            raise NotImplementedError('Only orthogonal boxes are supported.')

        self.trajectory = trajectory
        self.bond_initial_threshold = bond_initial_threshold
        self.bond_breaking_threshold = bond_breaking_threshold
        self.bond_forming_threshold = bond_forming_threshold
        self.molecule_stable_frames = molecule_stable_time / trajectory.metadata.timestep
        self.reaction_path_margin = reaction_path_margin
        # containers for detected stuff
        self.mdmolecules = None
        self.initial_composition = None
        self.initial_species = None
        self.mdreactions = None
        self.mdmolecule_network = None
        self.reactions: Set[chemid.Reaction] = set()
        self.species: Set[chemid.Species] = set()
        # key: Species or Reaction
        self.geometries: Dict[Union[chemid.Species, chemid.Reaction], List[Geometry]] = defaultdict(list)
        self.reaction_paths: Dict[chemid.Reaction, List[List[TSGeometry]]] = defaultdict(list)
        # key: timestep
        self.reactions_by_time: Dict[float, List[chemid.Reaction]] = defaultdict(list)

    def print_reactions(self, smiles=False):
        """
            Print a list of detected reactions to standard output.
            :param smiles: print SMILES instead of default IDs when True
            :type smiles: bool
        """
        print(self.reaction_list_message(smiles=smiles))

    def reaction_list_message(self, smiles=False):
        """
        compiles a textblock of the detected reactions, ordered by timestep
        :param smiles: write molecules as SMILES if True, otherwise use InChI-Keys
        :type smiles: bool
        """
        if not self.reactions_by_time:
            message = 'No reactions were found.\n'
        else:
            message = 'These reactions were found:\n  time[fs]: Reaction\n'
            for time_in_fs, reaction_list in sorted(self.reactions_by_time.items()):
                for reaction in sorted(reaction_list):
                    if smiles:
                        message += f'{time_in_fs:10.2f}: '
                        message += ' + '.join(spec.smiles for spec in reaction.reactants)
                        message += ' -> '
                        message += ' + '.join(spec.smiles for spec in reaction.products)
                        message += '\n'
                    else:
                        message += f'{time_in_fs:10.2f}: '
                        message += ' + '.join(spec.id for spec in reaction.reactants)
                        message += ' -> '
                        message += ' + '.join(spec.id for spec in reaction.products)
                        message += '\n'
        return message

    def detect_mdreactions(self):
        """
            detect reactions and delete unstable intermediates
        """
        filtered_frames = get_frames_with_reactive_events(list_of_graphs=self.trajectory.graphs,
                                                          bond_initial_threshold=self.bond_initial_threshold,
                                                          bond_breaking_threshold=self.bond_breaking_threshold,
                                                          bond_forming_threshold=self.bond_forming_threshold)
        # sets: mdmolecules initial_composition
        self.create_mdmolecule_network(filtered_frames)
        # sets: mdmolecule_network mdreactions
        self.filter_unstable_intermediates()

    def get_geometry_and_graph_for_mdmolecule(self, mol, timestep=None):
        """
        Extract the geomertry and the graph of a MDMolecule from the trajectory.
        If no timestep is given, the middle step of a molecules lifetime is taken.
        Reconstructs (unbreaks) the molecule when it is broken by the boundary.
        :param mol: MDMolecule
        :type mol: MDMolecule
        :param timestep: the timestep
        :type timestep: int
        :return: Tuple[Geometry, Graph]
        """
        if timestep is None:
            timestep = (mol.start_frame + min(mol.end_frame(), self.trajectory.n_frames())) // 2
        sorted_ids = sorted(mol.atoms())
        mol_geometry = self.trajectory.get_geometry(timestep, sorted_ids)
        mol_geometry.unbreak_molecule(
                    tuple(np.diagonal(self.trajectory.metadata.box_vectors)),
                    self.trajectory.metadata.periodic_boundary_conditions,
                    zero_com=True)
        mol_graph = mol.graph.relabel_atoms(mapping=dict((old, new) for new, old in enumerate(sorted_ids)), copy=True)

        return mol_geometry, mol_graph

    def get_geometries_from_timesteps_and_atomids(self, timesteps, atomids):
        """
        Extract the geomertry of a Reaction from the trajectory for a give sequence of timesteps
        :param timesteps: a list of timesteps or one timestep to extract
        :type timesteps: list or int
        :return: List[TSGeometry]
        """
        if type(timesteps) == int:
            timesteps = [timesteps]

        sorted_ids = sorted(atomids)
        reaction_path = []
        for i in timesteps:
            geo = self.trajectory.get_geometry(i, sorted_ids)
            reaction_path.append(TSGeometry.from_geometry(geo, active=None))
        # shift all the frames by the same displacement
        shift = reaction_path[0].unbreak_molecule(
                    tuple(np.diagonal(self.trajectory.metadata.box_vectors)),
                    self.trajectory.metadata.periodic_boundary_conditions,
                    zero_com=True)
        if len(reaction_path) > 1:
            for geo in reaction_path[1:]:
                geo.coords += shift

        return reaction_path

    def detect(self, species_id_uses_graphs=True):
        """
        Process bonds from the trajectory, create a network of molecules,
        and return a list of detected Reactions with reactants/products/TS geometries and the frame number.
        """
        if self.mdreactions is None:
            self.detect_mdreactions()

        self.initial_species = []
        for mol in self.initial_composition:
            mol_geometry, mol_graph = self.get_geometry_and_graph_for_mdmolecule(mol)
            if species_id_uses_graphs:
                spec = chemid.Species.from_geometry_and_graph(mol_geometry, mol_graph)
            else:
                spec = chemid.Species.from_geometry(mol_geometry)
            self.species.add(spec)
            self.geometries[spec].append(mol_geometry)
            self.initial_species.append(spec)

        for reactants, products in self.mdreactions:
            reactant_species = []
            product_species = []
            reax_ids = []
            # create Species from graphs and geometries
            for mol in reactants:
                # here, atom ids (nodes) in mol_graph start from 0 again!
                mol_geometry, mol_graph = self.get_geometry_and_graph_for_mdmolecule(mol)
                if species_id_uses_graphs:
                    spec = chemid.Species.from_geometry_and_graph(mol_geometry, mol_graph)
                else:
                    spec = chemid.Species.from_geometry(mol_geometry)
                self.species.add(spec)
                reactant_species.append(spec)
            for mol in products:
                # here, atom ids (nodes) in mol_graph start from 0 again!
                mol_geometry, mol_graph = self.get_geometry_and_graph_for_mdmolecule(mol)
                if species_id_uses_graphs:
                    spec = chemid.Species.from_geometry_and_graph(mol_geometry, mol_graph)
                else:
                    spec = chemid.Species.from_geometry(mol_geometry)
                self.species.add(spec)
                # append molecule geometry
                self.geometries[spec].append(mol_geometry)
                product_species.append(spec)
                # remember atom ids, numbers are from the frame
                reax_ids += mol.atoms()

            # filter recrossing reactions like A+B -> A+B
            reactant_species.sort()
            product_species.sort()
            if reactant_species == product_species:
                continue

            # create Reaction from Species
            reax = chemid.Reaction(reactant_species, product_species)
            reax_timestep = max(p.start_frame for p in products)

            # extract a TS geometry
            ts_geo = self.trajectory.get_geometry(reax_timestep, reax_ids)
            ts_geo.unbreak_molecule(
                    tuple(np.diagonal(self.trajectory.metadata.box_vectors)),
                    self.trajectory.metadata.periodic_boundary_conditions,
                    zero_com=True)
            # store molecule geometries and a reaction path for reactions around the TS
            self.geometries[reax].append(ts_geo)
            path_start = max(0, reax_timestep - self.reaction_path_margin)
            path_end = min(self.trajectory.n_frames(), reax_timestep + self.reaction_path_margin)
            reaction_timesteps = list(range(path_start, path_end))
            reaction_path = self.get_geometries_from_timesteps_and_atomids(reaction_timesteps, reax_ids)
            self.reaction_paths[reax].append(reaction_path)

            # use the correct timestep here, not the frame number.
            # then it is easy to determine the time (in fs) the reaction happened: time = simulated_timestep * integration_step
            simulated_timestep = self.trajectory.first_timestep + reax_timestep * self.trajectory.metadata.sampling_frequency
            time_in_fs = simulated_timestep * self.trajectory.metadata.timestep
            self.reactions_by_time[time_in_fs].append(reax)
            self.reactions.add(reax)

    def create_mdmolecule_network(self, filtered_frames: list):
        """
        From list of MD frames, create MDMolecules and link them to each other wherever elementary reactions change them.
        :param filtered_frames: List of timewise ordered MD graphs (frames) that contain edge (bond) changes.
        :type filtered_frames: list[int, networkx.Graph, list[tuple, ...], list[tuple, ...]]
        """
        self.mdmolecules = []
        atom_to_mol_dict = {}
        initial_frame_number, initial_graph, _, _, = filtered_frames[0]

        # handle first frame
        self.initial_composition = []
        for component in initial_graph.connected_components():
            subgraph = initial_graph.subgraph(component)
            ctymol = chemtrayzer.core.md.MDMolecule(initial_frame_number, subgraph)
            for mol_atom_index in subgraph.atoms:
                atom_to_mol_dict[mol_atom_index] = ctymol
            self.initial_composition.append(ctymol)
        self.mdmolecules += self.initial_composition

        # loop through the frames with bond-changing events
        # and create new objects of MDMolecules
        # MDMmolecules have pointers to their previous and following
        for (frame_number, next_graph, added, removed) in filtered_frames[1:]:
            changed_edges = added + removed
            used_atom_ids = set()
            for (atom_id_1, atom_id_2) in changed_edges:
                # molecules already found?
                if atom_id_1 in used_atom_ids and atom_id_2 in used_atom_ids:
                    continue

                # reactants
                reactant_1 = atom_to_mol_dict[atom_id_1]
                reactant_2 = atom_to_mol_dict[atom_id_2]
                reactants = (reactant_1,)
                set_of_reactant_atom_ids = set(reactant_1.atoms())
                if reactant_1.internal_id != reactant_2.internal_id:
                    reactants += (reactant_2,)
                    set_of_reactant_atom_ids.update(reactant_2.atoms())

                # products
                product_1 = get_mdmolecule_from_atom_id(next_graph, atom_id_1, frame_number)
                products = (product_1,)
                if not product_1.graph.has_atom(atom_id_2):
                    products += (get_mdmolecule_from_atom_id(next_graph, atom_id_2, frame_number),)
                set_of_product_atom_ids = set()
                for mol in products:
                    set_of_product_atom_ids.update(mol.atoms())

                # merging of events
                sym_diff = set_of_reactant_atom_ids.symmetric_difference(set_of_product_atom_ids)
                while sym_diff:
                    atom_id = sym_diff.pop()
                    if atom_id not in set_of_reactant_atom_ids:
                        new_mol = atom_to_mol_dict[atom_id]
                        reactants += (new_mol,)
                        set_of_reactant_atom_ids.update(new_mol.atoms())
                        sym_diff = set_of_reactant_atom_ids.symmetric_difference(set_of_product_atom_ids)
                    if atom_id not in set_of_product_atom_ids:
                        new_mol = get_mdmolecule_from_atom_id(next_graph, atom_id, frame_number)
                        products += (new_mol,)
                        set_of_product_atom_ids.update(new_mol.atoms())
                        sym_diff = set_of_reactant_atom_ids.symmetric_difference(set_of_product_atom_ids)

                # update the set of handled atoms
                used_atom_ids.update(set_of_reactant_atom_ids)

                # connections between molecules
                for product in products:
                    # product.predecessors = []
                    for reactant in reactants:
                        product.predecessors.append(reactant)
                        reactant.successors.append(product)

                # update atom to molecule dictionary
                for product in products:
                    for atom_id in product.atoms():
                        atom_to_mol_dict[atom_id] = product

                # add to return list
                self.mdmolecules += products

    def filter_unstable_intermediates(self):
        """
        Removes detected molecules (MDMolecules) that live shorter than the molecule_stable_time.
        Those will be considered unstable intermediates and will never be reported as products of a reaction.
        If a reaction has unstable intermediates, subsequent elementary reaction steps are added until stable products are formed.
        """
        # check
        if self.mdmolecules is None:
            logging.warning('Unable to filter for unstable intermediates because the MDMolecule list is empty.')
        else:

            self.mdmolecule_network = DirectedGraph()
            for mol in self.mdmolecules:
                self.mdmolecule_network.add_node((mol, mol.internal_id))
            for mol in self.mdmolecules:
                if not mol.predecessors:
                    for successor in mol.successors:
                        self.mdmolecule_network.add_edge((mol, -mol.internal_id), (successor, successor.internal_id))
                else:
                    if (mol.end_frame() - mol.start_frame) < self.molecule_stable_frames:
                        # unstable: add connection to next products in line
                        for successor in mol.successors:
                            self.mdmolecule_network.add_edge((mol, mol.internal_id), (successor, successor.internal_id))
                    else:
                        # stable: create new entry node with negative id and add connection to next products in line
                        for successor in mol.successors:
                            self.mdmolecule_network.add_edge((mol, -mol.internal_id), (successor, successor.internal_id))

            self.mdreactions = []
            for nodeset in self.mdmolecule_network.connected_components():
                molnet = self.mdmolecule_network.subgraph(nodeset)
                if len(molnet) < 2:
                    continue

                # here, intermediates will have non-zero in/out degree
                reactants = tuple([mol for (mol, _), indegree in molnet.in_degree() if indegree == 0])
                products = tuple([mol for (mol, _), outdegree in molnet.out_degree() if outdegree == 0])

                self.mdreactions.append((reactants, products))

    def get_initial_species_numbers(self):
        """
            Turns the list of initial species into a dictionary with their respective numbers
        :return: A dictionary with initial species as key and their initial count as value
        """
        if self.initial_species is None:
            return None
        return {species: self.initial_species.count(species) for species in set(self.initial_species)}

    def write_mdmolecule_network(self, filename: str = "molecule_network.gml"):
        """
        Writes each detected reaction as a network of molecules into one GML file.
        :param filename: name of the output
        :type filename: str
        """
        if self.mdmolecule_network is None:
            pass
        else:
            nx.write_gml(self.mdmolecule_network, filename, stringizer=lambda x: repr(x[0]))

    def print_mdmolecules(self):
        """
        debug function for printing out the detected molecules (as MDMolecules)
        """
        for mol in self.mdmolecules:
            print(f'({mol.predecessors}) -> {repr(mol)} -> ({mol.successors}) lifetime:{mol.end_frame() - mol.start_frame}')

    def print_mdreactions(self):
        """
        debug function for printing out the detected reactions (as MDReactions)
        """
        for reaction in self.mdreactions:
            print('one reaction', reaction)

def get_mdmolecule_from_atom_id(graph, atom_id, frame_number) -> chemtrayzer.core.md.MDMolecule:
    """
    small helper function that creates a MDMolecule from a networkX subgraph. The MDMolecule contains the atom with the given atom_id
    :param graph: Connectivity graph of one whole MD frame
    :type graph: networkx Graph
    :param atom_id: number of the atom in the MD frame
    :type atom_id: int
    :param frame_number: timestep number of the MD frame, to be stored in the MDMolecule
    :type frame_number: int
    :return: MDMolecule
    """
    component = graph.node_connected_component(atom_id)
    subgraph = graph.subgraph(component)
    mdmol = chemtrayzer.core.md.MDMolecule(frame_number, subgraph)
    return mdmol


def convert_box_dim_format(lattice_vectors):
    '''
    takes in lattice vectors for a single frame and returns their lengths,
    and angles in Degree as an array.
    :param lattice_vectors: 3x3 Matrix of latice vectors, in units of Angström.
    '''

    a = norm(lattice_vectors[0])
    b = norm(lattice_vectors[1])
    c = norm(lattice_vectors[2])
    alpha =180/pi * arccos(clip(dot(lattice_vectors[0], lattice_vectors[1]), -1.0, 1.0))
    beta = 180/pi * arccos(clip(dot(lattice_vectors[1], lattice_vectors[2]), -1.0, 1.0))
    gamma =180/pi * arccos(clip(dot(lattice_vectors[2], lattice_vectors[0]), -1.0, 1.0))

    return [a, b, c, alpha, beta, gamma]


def isBarrierless(Reac):
    '''
    TS optimizations are useless for barrieless
    reactions. The present function checks if a
    reaction is barrierless (true) or not (false).

    The check is very weak to avoid treating
    reactions as barrierless which are not.

 	:param Reac:    chemtrayzer reaction object
    :return:        true if barrierless, false if not
    '''

    #check spin multiplicity
    spin = [[], []]
    for r in Reac.reactants:
        spin[0].append(r.guessed_spin())
    for p in Reac.products:
        spin[1].append(p.guessed_spin())


    nr = len(spin[0])
    np = len(spin[1])
    if nr != np:
        if (sorted(spin[0]) == [2, 2] or sorted(spin[1]) == [2, 2]) and (sorted(spin[1]) == [1] or sorted(spin[0]) == [1]):
            return True
        elif (sorted(spin[0]) == [2, 3] or sorted(spin[1]) == [2, 3]) and (sorted(spin[1]) == [2] or sorted(spin[0]) == [2]):
            return True
        elif (sorted(spin[0]) == [3, 3] or sorted(spin[1]) == [3, 3]) and (sorted(spin[1]) == [3] or sorted(spin[0]) == [3]):
            return True
        elif (sorted(spin[0]) == [2, 2, 3] or sorted(spin[1]) == [2, 2, 3]) and (sorted(spin[1]) == [1] or sorted(spin[0]) == [1]):
            return True
    return False


def get_frames_with_reactive_events(list_of_graphs, bond_initial_threshold=0.5, bond_breaking_threshold=0.3, bond_forming_threshold=0.8):
    '''
    Loops through the frames and gets those which have different connectivity than the one before.
    Connectivity changes are subject to thresholds:
    Bonds vanish when their order drops below bond_breaking_threshold, and appear when their order rises above bond_forming_threshold.

    :param bond_initial_threshold:
    :type bond_initial_threshold:
    :param list_of_graphs: list of cty graphs
    :type list_of_graphs: list of cty graphs
    :param bond_breaking_threshold: default 0.3
    :type bond_breaking_threshold: float
    :param bond_forming_threshold: default 0.8
    :type bond_forming_threshold: float
    :return: List of Tuples: frame number, list of added bonds, list of removed bonds
    '''
    if not (bond_forming_threshold >= bond_initial_threshold >= bond_breaking_threshold):
        raise ValueError(f'forming threshold must be larger than initial threshold, which must be larger than breaking threshold: {bond_forming_threshold} > {bond_initial_threshold} > {bond_breaking_threshold}')

    if not list_of_graphs:
        logging.error('List of graphs in get_frames_with_reactive_events may not be empty')
        raise ValueError

    if len(list_of_graphs) == 1:
        return [(0, list_of_graphs[0].copy(), [], [])]

    current_graph = list_of_graphs[0].copy()
    for u, v in current_graph.bonds:
        bond_order = current_graph.get_bond_attribute(u, v, 'bond_order')
        if bond_order < bond_initial_threshold:
            current_graph.remove_bond(u, v)
        # else:
        #     data['bond_order'] = 1
    return_list = [(0, current_graph.copy(), [], [])]

    for i, graph in enumerate(list_of_graphs[:-1]):

        next_graph = list_of_graphs[i + 1]
        edge_union_from_both_graphs = set(graph.bonds) | set(next_graph.bonds)

        added_edges_list = []
        removed_edges_list = []
        # changed_edges_list = []

        for bond in edge_union_from_both_graphs:

            bo_current = graph.get_bond_attribute(*bond, attr='bond_order') if graph.has_bond(*bond) else 0
            bo_next = next_graph.get_bond_attribute(*bond, attr='bond_order') if next_graph.has_bond(*bond) else 0

            # hysteresis-like event detection
            # bond forms
            # covers also double bond/triple/etc bond forming
            if bo_current <= bond_forming_threshold < bo_next and bond not in current_graph.bonds:
                added_edges_list.append(bond)
                bo_guess = 1 + int(bo_next - bond_forming_threshold)
                current_graph.add_bond(bond[0], bond[1], bond_order=bo_guess)

            # bond breaks
            elif bo_current >= bond_breaking_threshold > bo_next and bond in current_graph.bonds:
                removed_edges_list.append(bond)
                current_graph.remove_bond(bond[0], bond[1])

            # single to double bond
            elif (bo_current <= 1 + bond_forming_threshold < bo_next and
                  current_graph.get_bond_attribute(*bond, 'bond_order') == 1):
                current_graph.set_bond_attribute(*bond, 'bond_order', 2)

            # double to single bond
            elif (bo_current >= 1 + bond_breaking_threshold > bo_next and
                  current_graph.get_bond_attribute(*bond, 'bond_order') == 2):
                current_graph.set_bond_attribute(*bond, 'bond_order', 1)

            # triple bond and higher
            elif 2 + bond_forming_threshold < bo_next:
                current_graph.set_bond_attribute(*bond, 'bond_order', 1 + int(bo_next - bond_forming_threshold))

        # event detected (leave out changed edges)
        if added_edges_list or removed_edges_list:
            return_list.append((i + 1, current_graph.copy(), added_edges_list, removed_edges_list))

    if not return_list:
        return [(0, None, [], [])]
    else:
        return return_list


class NVTRateConstants:
    """
        Computes rate constants and bounds for a set of reactions.
        See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
    :param initial_composition: dictionary of intial species and their numbers
    :param reactions_by_step: dictionary of all reactions with simulation step as key and list of reactions as value
    :param timestep: the used timestep in fs
    :param volume: the volume of the NVT simulation
    :param confidence: confidence level for the rate constant bounds (0..1)
    :param start: Offset to start the rate constant computation from. Needs to be smaller than the time of the first reaction. In fs.
    """
    def __init__(self, initial_composition: Dict[Species, int], reactions_by_time: Dict[float, List[Reaction]], timestep: float, volume: float, confidence: float = 0.9, start: float = 0.0, end: float = -1.0):
        self.ntime = None
        self.volume = volume
        self.timestep = timestep
        self.start = start
        self.end = end
        self.initial_composition = initial_composition

        # catch the case when no reactions where detected and an empty dict was passed
        if len(reactions_by_time) == 0:
            raise ValueError('No reactions to analyze. reactions_by_time is empty.')
        self.reactions_by_time = reactions_by_time
        # confidence for rate constant bounds
        self.confidence = confidence
        # container of points in time where data (reactions)
        self.time = []
        self.ntime = 0

        # factors
        # 1/(vol*NA*1E-24) : [molecules/A3] to [mol/cm3]
        self.fc = 10 / (6.022 * self.volume)
        # 1/femtosecond to 1/s
        self.ft = 1E15

        self.spex, self.reax = dict(), dict()
        # fill containers
        self.init_time_list()
        self.init_species_numbers()

    def compute(self):
        """
            Main method of reaction rate computation.
        :return:
        """
        if not self.time:
            print('No reactions to analyze.')
            return

        # species numbers over time
        self.calculate_species_concentrations()

        # reaction flux
        self.calculate_reaction_concentrations()

        # rate constants and bounds
        self.calculate_rate_coefficients()

        return

    def init_time_list(self):
        """
            Initializes the list of steps and the list of times for the computation.
        """
        list_of_times = sorted(self.reactions_by_time)

        # check user input
        if self.start >= list_of_times[0]:
            logging.warning(f'Reactions must happen after the starting time step ({self.start} fs). The start time was reset to before the first reaction ({list_of_times[0]-self.timestep}).')
            self.start = list_of_times[0]-self.timestep
        if self.end == -1:
            self.end = list_of_times[-1]
        if self.end < self.start:
            logging.warning(f'End time ({self.end} fs) must be larger than the start time. The end time was reset to the last reaction ({list_of_times[-1]} fs)')
            self.end = list_of_times[-1]

        # select reactions to include in analysis
        self.time = [self.start] + [t for t in list_of_times if self.start < t <= self.end]
        if self.end not in self.time:
            self.time = self.time + [self.end]
        self.ntime = len(self.time)

    def init_species_numbers(self):
        """
            Initializes the numbers of each species at time zero.
        """
        # initial molecules
        for species, n in self.initial_composition.items():
            self.spex[species] = [n] * self.ntime
        # later occuring molecules
        for timestep, reactions in self.reactions_by_time.items():
            for reaction in reactions:
                for species in set(reaction.reactants + reaction.products):
                    if species not in self.spex:
                        self.spex[species] = [0] * self.ntime

    def calculate_species_concentrations(self):
        """
            Reenacts the reactive events and notes down the number of species each time step.
        """
        # conversion of reaction history to species concentrations (self.spex)
        for i, t in enumerate(self.time):
            for reaction in self.reactions_by_time[t]:
                for reactant in reaction.reactants:
                    # list of flow of species per time stamp (sparse list, mostly zero)
                    if reactant not in self.spex:
                        # initialize list
                        self.spex[reactant] = [0] * self.ntime
                    # count down the reactant concentration, because they are consumed
                    self.spex[reactant][i] -= 1
                    # set concentration at future time stamps
                    for j in range(i + 1, self.ntime):
                        self.spex[reactant][j] = self.spex[reactant][i]

                # same for products
                for product in reaction.products:
                    if product not in self.spex:
                        self.spex[product] = [0] * self.ntime
                    self.spex[product][i] += 1
                    for j in range(i + 1, self.ntime):
                        self.spex[product][j] = self.spex[product][i]

    def calculate_reaction_concentrations(self):
        """
            Reenacts the reactive events.
        """
        # conversion of reaction history to reaction flux (self.reax)
        for i, t in enumerate(self.time):
            for reaction in self.reactions_by_time[t]:
                reverse_reaction = reaction.reverse()
                # make sure only forward xor backward reaction is registered
                # first come first serve
                # if this results in negative reaction flux, the flux will be inverted later on
                if reaction in self.reax:
                    self.reax[reaction].flux[i] += 1
                elif reverse_reaction in self.reax:
                    self.reax[reverse_reaction].flux[i] -= 1
                else:
                    # initialize
                    numbers = [0] * self.ntime
                    self.reax[reaction] = RateConstantRecord(flux=numbers)
                    self.reax[reaction].flux[i] += 1

        # inversion of reactions with negative net flux
        hashes_to_delete = []
        for reaction in self.reax:
            if sum(self.reax[reaction].flux) < 0:
                hashes_to_delete.append(reaction)
        for reaction in hashes_to_delete:
            reverse_reaction = reaction.reverse()
            self.reax[reverse_reaction] = self.reax.pop(reaction)
            self.reax[reverse_reaction].flux = [-1 * f for f in self.reax[reverse_reaction].flux]

    def calculate_rate_coefficients(self):
        """
            Computes for each reaction (forward and backward) the concentration integrals, rate constants, and bounds estimates.
            For more details, see J. Chem. Theory Comput. 2015, 11, 2517−2524, DOI: 10.1021/acs.jctc.5b00201 and
            J. Chem. Theory Comput. 2017, 13, 3955−3960, DOI: 10.1021/acs.jctc.7b00524

            From the definition of the rate coefficient k of a sample reaction B + C => D,

            d/dt [D] = k * [B][C]

            we can derive

            [D] - [D]_0 = k * Integral( [B][C], dt )

            where [D] - [D]_0 is the concentration increase of D through this reaction channel.
            Then, in terms of discrete reaction events, we can write

            [D] - [D]_0 = k * Sum( [B]_i * [C]_i * t_i , i=1..M)

            where M is the number of reaction events, t_i and [X]_i are the time resp. reactant concentrations between two events
            With [X] = N_x/N_0/V, where N_x is the number of X-molecules, N_0 is 6.022e23/mol, and V is the volume, we can write

            N_d/N_0/V - N_d_0/N_0/V = k * Sum( N_b_i/N_0/V * N_c_i/N_0/V * t_i , i=1..M)
                (N_d - N_d_0)/N_0/V = k * Sum( N_b_i       * N_c_i       * t_i , i=1..M) / (N_0*V)^2

            The count increase of molecule D through this reaction channel, N_D - N_D_0 = N_f, is exactly the number of forward reactions
            of the form B + C => D, (the backward reactions D => B + C are counted separately).

            So, the rate coefficient for B + C => D can be computed with

            k = N_f / Sum( N_b_i * N_c_i * t_i , i=1..M) * (N_0*V)^(r-1)

            where r is the number of reactants (here, r=2).

        """
        for reaction in self.reax:
            # compute sum of "number integrals" intA = sum(i=0..ntime)[ t(i+1)-t(i) * N_1 * N_2 * ... ]
            # where N_1, N_2, ... are numbes of reactants of a given reaction, and t(i+1)-t(i) is a time interval where those numbers are constant
            # Because V=const this can be turned into the concentration integral by multiplying with self.fc
            # A=reactants/forward B=products/backward
            A = reaction.reactants
            B = reaction.products
            nA = len(A) - 1
            nB = len(B) - 1
            intA = 0.0
            intB = 0.0
            pos = 0
            neg = 0
            for i in range(self.ntime - 1):
                dt = self.time[i + 1] - self.time[i]

                # concentration correction if two species of the same kind take part in the reaction
                corrA = {species: A.count(species) - 1 for species in A}
                corrB = {species: B.count(species) - 1 for species in B}

                # consumption of reactants
                tmpA = 1
                for species in A:
                    tmpA *= max(self.spex[species][i] - corrA[species], 0)
                    corrA[species] -= 1
                intA += tmpA * dt
                if self.reax[reaction].flux[i+1] > 0:
                    pos += self.reax[reaction].flux[i+1]

                # production of products
                tmpB = 1
                for species in B:
                    tmpB *= max(self.spex[species][i] - corrB[species], 0)
                    corrB[species] -= 1
                intB += tmpB * dt
                if self.reax[reaction].flux[i+1] < 0:
                    neg -= self.reax[reaction].flux[i+1]

            # estimate uncertainties
            # concentration integrals need be >0 else error
            if intA > 0:
                # k bounds estimation based on Poisson distribution
                # see DOI: 10.1021/acs.jctc.7b00524
                # in case of no event, an upper estimate is still possible.
                # for X=0.9 the following empiric approximations apply:
                #  lambda_lo = N - N^0.6
                #  lambda_up = N + N^0.6 + 2
                #  with kup = lambda_up/int and N = pos (or neg)
                #  tested with X=0.8 and X=0.95 as well
                if pos == 0:
                    kup = estNoReacBound(f=intA, X=self.confidence)
                    klo = 0.0
                else:
                    kup_0 = (2 + pos + pos ** 0.6) / intA
                    kup = leastsq(func=estRateBounds, x0=kup_0, args=(intA, pos, self.confidence))[0][0]
                    klo = float(np.real(-pos / intA * lmbW(lambda_up=kup * intA, N=pos)))
                self.reax[reaction].events = pos
                self.reax[reaction].upper_k = kup * self.ft / (self.fc ** nA)
                self.reax[reaction].lower_k = klo * self.ft / (self.fc ** nA)
                self.reax[reaction].rate = pos / intA * self.ft / (self.fc ** nA)
            if intB > 0:
                if neg == 0:
                    kup = estNoReacBound(f=intB, X=self.confidence)
                    klo = 0.0
                else:
                    kup_0 = (2 + neg + neg ** 0.6) / intB
                    kup = leastsq(func=estRateBounds, x0=kup_0, args=(intB, neg, self.confidence))[0][0]
                    klo = float(np.real(-neg / intB * lmbW(lambda_up=kup * intB, N=neg)))
                self.reax[reaction].eventsB = neg
                self.reax[reaction].upper_kB = kup * self.ft / (self.fc ** nB)
                self.reax[reaction].lower_kB = klo * self.ft / (self.fc ** nB)
                self.reax[reaction].rateB = neg / intB * self.ft / (self.fc ** nB)

    def get_rates(self, reaction: Reaction):
        """
            Returns rate constants of one specified reaction, or None if the reaction has no data. Units are cm3, mol and s.
        :param reaction: Reaction object of a reaction.
        :return: tuple of rate constant, lower bound, upper bound, number of events
        :rtype: Tuple[float, float, float, int]
        """
        forward_is_in_here = True
        ayreaction = None
        try:
            ayreaction = self.reax[reaction]
        except KeyError:
            reverse_reaction = reaction.reverse()
            forward_is_in_here = False
            try:
                ayreaction = self.reax[reverse_reaction]
            except KeyError:
                rstr = ' -> '.join(' + '.join([species.smiles for species in species]) for species in [reaction.reactants, reaction.products])
                warnings.warn(f'Reaction "{rstr}" not found in Rate Calculator')
        if ayreaction is None:
            return 0.0, 0.0, 0.0, 0
        else:
            if forward_is_in_here:
                k, k_low, k_up, n = ayreaction.rate, ayreaction.lower_k, ayreaction.upper_k, ayreaction.events
            else:
                k, k_low, k_up, n = ayreaction.rateB, ayreaction.lower_kB, ayreaction.upper_kB, ayreaction.eventsB
            return k, k_low, k_up, n

    def write_data(self, species_filename, rates_filename):
        """
            Write species numbers and reaction rate constants into two csv files.
        :param species_filename:
        :param rates_filename:
        """
        # . write species concentrations
        # writer = open(species_filename, 'w')
        with open(species_filename, 'w') as f:
            smiles_str = ','.join(species.smiles for species in self.spex)
            f.write(f't [fs],{smiles_str}\n')
            for i, t in enumerate(self.time):
                numbers_str = ','.join(str(self.spex[species][i]) for species in self.spex)
                f.write(f'{t},{numbers_str}\n')
            f.close()

        # write rate constats for each reaction forward and backward
        with open(rates_filename, 'w') as f:
            f.write('reaction_id,reactant_SMILES,product_SMILES,k,k_lower,k_upper,#events\n')
            for reaction, ayr in self.reax.items():
                smiles_reactants = '.'.join(species.smiles for species in reaction.reactants)
                smiles_products = '.'.join(species.smiles for species in reaction.products)
                reverse = reaction.reverse()
                f.write(f'{reaction.id},{smiles_reactants},{smiles_products},{ayr.rate:},{ayr.lower_k},{ayr.upper_k},{ayr.events}\n')
                f.write(f'{reverse.id},{smiles_products},{smiles_reactants},{ayr.rateB},{ayr.lower_kB},{ayr.upper_kB},{ayr.eventsB}\n')

        return

    def compact_result(self):
        """
            Return the rate data in a compact form as {reaction.id: (k, klo, kup, N)}
        :rtype: Dict[str, Tuple[float, float, float, int]]
        """
        compact_result = {}
        for reaction, ayr in self.reax.items():
            reverse = reaction.reverse()
            compact_result[reaction] = (ayr.rate, ayr.lower_k, ayr.upper_k, ayr.events)
            compact_result[reverse] = (ayr.rateB, ayr.lower_kB, ayr.upper_kB, ayr.eventsB)
        return compact_result


def lmbW(lambda_up, N):
    """
        Adapted Lambert W function for usage in the bounds computation for rate constants.
        See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
        Used in equation (13)
    :param lambda_up: upper limit of expected number of events
    :param N: actual number of events
    :return: lambda_low, the lower limit of expected number of events
    """
    return lambertw(np.round(-lambda_up * np.exp(-lambda_up / N) / N, 30), k=0)


def estRateBounds(k_up, f, N, X):
    """
        Helper function of the iterative computation of k_up, the upper rate constant of a given reaction.
        The function computes the difference between the explicitly specified confidence level X
        and the implicitly defined X via N and lambda (to be minimized by scipy.optimize.leastsq).
        See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
        Divide Equation (11) by Gamma(N+1) to get X = - gammaincc(N+1,lambda_up) + gammaincc(N+1,lambda_low)
    :param k_up: upper rate constant guess for given actual number of events
    :param f: reactants concentration integral (sum over product of volume, concentrations of reactants, and time interval)
    :param N: actual number of events
    :param X: specified confidence level (0..1)
    :return: difference of explicitly and implicitly defined X
    """
    return X + gammaincc(N + 1, k_up * f) - gammaincc(N + 1, np.real(-N * lmbW(lambda_up=k_up * f, N=N)))


def estNoReacBound(f, X):
    """
        Computes the upper bound of a rate constant for a reaction that was not observed.
        See J. Chem. Theory Comput. 2017, 13, 3955−3960, https://pubs.acs.org/doi/10.1021/acs.jctc.7b00524
        Derived from Equation (8) where lambda_low = 0
    :param f: reactants concentration integral (sum over product of volume, concentrations of reactants, and time interval)
    :param X: specified confidence level (0..1)
    :return: upper bound for rate constant
    """
    return -np.log(1 - X) / f
