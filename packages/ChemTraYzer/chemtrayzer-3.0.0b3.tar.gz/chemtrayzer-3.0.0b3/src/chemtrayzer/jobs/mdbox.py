'''
This module contains classes to generate simulation boxes for MD simulations.
'''


from dataclasses import dataclass
import os
from abc import ABCMeta
from datetime import timedelta
from pathlib import PurePath
from typing import Iterable, Tuple

from chemtrayzer.core.coords import Geometry, InvalidXYZFileError
from chemtrayzer.engine.jobsystem import Job, JobTemplate, Memory


class MDBoxJob(Job, metaclass=ABCMeta):
    r'''
    Abstract class for jobs creating simple MD boxes.

    :param name: string - name of job
    :param geometries: geometry of species added to the box
    :param count: number of molecules for each geometry which should be added to
                  the box
    :param box_dim: tuple of six integers (x1, y1, z1, x2, y2, z2) which define
                    the two points spanning the box
    :param result: dictionary with keys 'box' for storing the generated geometry
                   and 'reason' for holding the reason for a possible failure
    :type result: dict
    :param \**kwargs: standard arguments to configure a Job (e.g. n_cpus)
    :type result: Geometry
    '''
    @dataclass
    class Result(Job.Result):
        '''result of a PackmolJob'''
        box: Geometry
        """packed box"""

    def __init__(self, geometries : Iterable[Geometry],
            count : Iterable[int], box_dim : Tuple[int], **kwargs) -> None:
        super().__init__(**kwargs)

        self.count = count
        self.geometries = geometries
        self.box_dim = box_dim
        self.result = None


class MDBoxJobFactory:
    '''Factory for jobs of type MDBoxJob

    :param packmol: path to packmol executable (mandatory argument b/c Packmol
                    is the only program currently supported for this type of
                    job)
    :param account: SLURM account to use for MDBoxJobs (this setting overrides
                    the account specified in the job system)
    '''

    def __init__(self, packmol : os.PathLike, account : str = None) -> None:
        self._packmol = PurePath(packmol)
        self._account = account


    def create(self, name, geometries : Iterable[Geometry],
            count : Iterable[int], box_dim : Tuple[int],
            metadata: object = None) -> MDBoxJob:
        '''
        :param name: string - name of job
        :param geometries: geometry of species added to the box
        :param count: number of molecules for each geometry which should be added to
                    the box
        :param box_dim: tuple of six integers (x1, y1, z1, x2, y2, z2) which define
                        the two points spanning the box
        :param metadata: any metadata you may want to add to the job
        '''
        job = PackmolJob(geometries, count, box_dim, executable = self._packmol,
            tol= 2,     # default tolerance (may be changed later)
            name=name,
            account = self._account,
            n_tasks = 1,    # a packmol jobs does not need a lot of ressources
            n_cpus = 1,
            memory = Memory(1, unit=Memory.UNIT_GB), # enough for most box sizes
            runtime = timedelta(minutes=15), # packmol usually only runs seconds
        )

        return job


class PackmolJob(MDBoxJob):
    r'''
    Create simple MD boxes using Packmol.

    :param name: string - name of job
    :param geometries: geometry of species added to the box
    :param count: number of molecules for each geometry which should be added to
                  the box
    :param box_dim: tuple of six integers (x1, y1, z1, x2, y2, z2) which define
                    the two points spanning the box
    :param executable: path to Packmol executable
    :param tol: minimum distance between atoms of different molecules in
                Angstrom
    :param result: dictionary with keys 'box' for storing the generated geometry
                   and 'reason' for holding the reason for a possible failure
    :type result: dict
    :param \**kwargs: standard arguments to configure a Job (e.g. n_cpus)
    :type result: Geometry
    '''

    _CMD_TMPL = '${executable} < packmol.inp'
    _INPUT_TMPLS = {
        'packmol.inp': '''\
tolerance ${tol}

filetype xyz

output mixture.xyz

${_tmpl_struct_def}'''
    }

    def __init__(self, geometries: Iterable[Geometry],
            count: Iterable[int], box_dim : Tuple[float],
            executable : os.PathLike, tol : float = 2.0,
            account=None, metadata: object = None, **kwargs) -> None:
        super().__init__(geometries, count, box_dim, **kwargs)

        if len(self.box_dim) != 6:
            raise ValueError('box_dim needs to contain six coordiantes')

        self.tol = tol
        self.executable = executable

        self._template = JobTemplate(self, self._CMD_TMPL, self._INPUT_TMPLS)


    def gen_input(self, path):
        self._template.gen_input(path)  # for packmol.inp

        for i, geo in enumerate(self.geometries):
            geo.to_xyz(os.path.join(path, f'geo{i}.xyz'))

    @property
    def command(self):
        return self._template.command

    @property
    def _tmpl_struct_def(self) -> str:
        '''assembles structure definition of input file'''

        box_def = ' '.join([f'{coord:f}' for coord in self.box_dim])

        return '\n'.join([
            f'structure geo{i}.xyz\n  number {count}\n'
            f'  inside box {box_def}\nend structure\n'
            for i, (count, geo) in enumerate(zip(self.count, self.geometries))
        ])


    def parse_result(self, path):
        try:
            self.result = self.Result(
                box = Geometry.from_xyz_file(os.path.join(path, 'mixture.xyz'))
            )
            self.succeed()
        except (InvalidXYZFileError, FileNotFoundError) as e:
            self.fail(e)
