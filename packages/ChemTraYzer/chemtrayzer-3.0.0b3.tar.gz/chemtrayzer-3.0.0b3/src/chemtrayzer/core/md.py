"""Molecular Dynamics

This module contains classes and functions used to analys molcular dynamics
simulations.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from itertools import combinations
from os import PathLike
from typing import Iterable

import numpy as np

from chemtrayzer.core.coords import ChainOfStates, Geometry
from chemtrayzer.core.graph import MolGraph
from chemtrayzer.core.lot import LevelOfTheory
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element
from chemtrayzer.engine.jobsystem import Job

################################################################################
# MD metadata
################################################################################


class MDIntegrator(Enum):
    VELOCITY_VERLET = "velocity Verlet"
    LEAPFROG = "leapfrog"


################################################################################
# MD metadata > thermostat and barostat
################################################################################
@dataclass
class MDThermostat:
    """base class for different thermostats"""

    tau: float
    """coupling time constant [fs]"""


class BerendsenTStat(MDThermostat):
    """Berendsend thermostat (usually only used for equlibiration)"""


@dataclass
class NoseHooverTStat(MDThermostat):
    """chained Nosé-Hoover thermostat"""

    chain_length: int = 3


class VelocityRescalingTStat(MDThermostat):
    """Berendsen thermostat with an added stochasitc term that enusres that the
    correct ensemble is sampled (Bussi-Donadio-Parrinello thermostat)."""


@dataclass
class MDBarostat:
    """Base class for barostats used in MD simulations"""

    tau: float
    """coupling time constant [fs]"""


class BerendsenPStat(MDBarostat):
    """Berendsen barostat"""


class MTKPStat(MDBarostat):
    """Martyna-Tobias-Klein barostat"""


THERMOSTATS = {
    "berendsen": BerendsenTStat,
    "nose-hoover": NoseHooverTStat,
    "nosé-hoover": NoseHooverTStat,
    "velocity rescaling": VelocityRescalingTStat,
}
"""thermostat classes mapped to string representations

Used when translating user input or config files into Python objects. This table
should ensure a consistent naming scheme for the user and the code. Lowercase
strings are used to allow for case-insensitive input with `str.lower()`.
"""

BAROSTATS = {"berendsen": BerendsenPStat}
"""barostat classes mapped to string representations"""


################################################################################
# MD metadata > simulation box box
################################################################################


class BoxType(Enum):
    ORTHOGONAL = auto()
    """rectangular cuboid"""
    TRICLINIC = auto()
    """parallelepiped"""

    @classmethod
    def from_box_vectors(cls, box_vectors: np.dnarray) -> BoxType:
        """determines the box type from the box vectors

        :param box_vectors: 3x3 matrix whose columns contain the box vectors
        :return: BoxType
        """
        if all(np.isclose(np.dot(v1, v2), 0) for v1, v2
               in combinations(box_vectors.T, 2)):
            return cls.ORTHOGONAL
        else:
            return cls.TRICLINIC



@dataclass
class BoxMetadata:
    """
    Contains all MD meta data. No large data like output coordinates.

    :param box_vectors: for orthogonal boxes, the input may be a tuple of the three box lengths which will be converted to a 3x3 matrix
    """

    box_vectors: np.ndarray = None
    """3x3 matrix whose columns contian the box vectors (i.e. those vectors
    that span the box/cell volume)"""
    box_origin: tuple[float, float, float] = None
    r"""origin of the simulation box. Without PBC, a point :math:`\vec{r}`  is "inside" the box, iff :math:`\vec{r} = \vec{r}_0 + a\,\vec{a} + b\,\vec{b} + c\,\vec{c}` where :math:`\vec{r}_0` is the box origin, :math:`\vec{a}, \vec{b}, \vec{c}` are the box vectors and :math:`a,b,c \in (0,1)`"""
    box_type: BoxType = BoxType.ORTHOGONAL
    """shape of the box"""
    periodic_boundary_conditions: tuple[bool, bool, bool] = (
        None  # (False, False, False)
    )
    """whether periodic boundary conditions are/were used for the x,y and z
    direction"""

    def __post_init__(self):
        if self.box_vectors is not None:
            self.box_vectors = np.array(self.box_vectors)
            if self.box_type == BoxType.ORTHOGONAL:
                if self.box_vectors.shape == (3,):
                    self.box_vectors = np.diag(self.box_vectors)
                elif self.box_vectors.shape == (3, 3):
                    # check for diagonality; theoretically, all diagonalizable
                    # matrices should define an orthogonal box, but in practice
                    # we want the first vector to be the x-axis, the second to
                    # be the y-axis and the third to be the z-axis
                    def is_diagonal(v: np.ndarray) -> bool:
                        return np.count_nonzero(v - np.diag(np.diagonal(v))) == 0

                    if not is_diagonal(self.box_vectors):
                        raise ValueError(
                            "Box vectors must be a diagonal matrix for "
                            "orthogonal boxes"
                        )
                else:
                    raise ValueError(
                        "Box vectors must be an array of length 3 "
                        "or a 3x3 array for orthogonal boxes"
                    )
            elif self.box_type == BoxType.TRICLINIC:
                if self.box_vectors.shape != (3, 3):
                    raise ValueError(
                        "Box vectors must be a 3x3 matrix for " "triclinic boxes"
                    )


@dataclass
class MDMetadata(BoxMetadata):
    level_of_theory: LevelOfTheory = None
    """potential energy method used in the simulation"""
    number_of_steps: int = None
    """number of timesteps"""
    timestep: float = None
    """size of a single timestep in femto seconds"""
    integration_method: MDIntegrator = None
    """integration method"""
    sampling_frequency: int = None
    """number of timesteps after which the next frame is written to disk during
    the simulation"""
    temperature: float = None
    """simulation temperature in Kelvin, if constant-T simulation"""
    thermostat: MDThermostat = None
    """thermostat used during the simulation"""
    pressure: float = None
    """simulation pressure in Pascal, if pressure was held constant"""
    barostat: MDBarostat = None
    """barostat used during simulation"""
    seed: int = None
    """seed used to generate initial velocity distribution. If seed is None, no
    velocities will be generated"""
    path: str = ""

    def __str__(self, width=30):
        s = "Content of MD meta data:\n"
        s += f'{"level of theory"    :{width}} : {self.level_of_theory}\n'
        s += f'{"number of steps"    :{width}} : {self.number_of_steps} steps\n'
        s += f'{"timestep"           :{width}} : {self.timestep} fs\n'
        s += f'{"integration method" :{width}} : {self.integration_method}\n'
        s += f'{"sampling frequency" :{width}} : {self.sampling_frequency} steps\n'
        s += f'{"temperature"        :{width}} : {self.temperature:.2f} K\n'
        s += f'{"pressure"           :{width}} : {self.pressure:.2f} Pa\n'
        return s

    def __post_init__(self):
        super().__post_init__()

        """some checks on the provided data"""
        if self.seed is not None and self.temperature is None:
            raise ValueError("When a seed is given, a temperature must be set.")

        if self.temperature is None != self.thermostat is None:
            raise ValueError(
                "If a thermostat is set, a temperature must be "
                "defined and vice versa"
            )

        if self.pressure is None != self.barostat is None:
            raise ValueError(
                "If a barostat is set, a pressure must be " "defined and vice versa"
            )


################################################################################
# MD molecule & rate constants
################################################################################


class MDMolecule:
    """
    Molecule representation as seen in a molecular dynamics simulation.

    :param start_frame: first frame of the molecule's occurence in MD
    :param graph: molecular graph in MolGraph format
    :param name: some descriptive string name
    :param end_frame: last frame of the molecule's occurence in MD
    :ivar predecessors: List of MDMolecules, reactants of the reaction that created this MDMolecule
    :ivar successors: List of MDMolecules, products of the reaction that consumed this MDMolecule
    """

    def __init__(self, start_frame: int, graph: MolGraph, name: str = ""):
        # IDs
        self._internal_id = id(self)
        self._name = name
        # molecular graph
        self.graph = graph
        # frames
        self.start_frame = start_frame
        # molecule history
        self.predecessors: list[MDMolecule] = []
        self.successors: list[MDMolecule] = []

    def __repr__(self):
        return f"#{self.internal_id} @{self.start_frame}"

    def __str__(self):
        text = ""
        text += f'MD Molecule #{self.internal_id} "{self.name}"\n'
        text += f"from: {self.start_frame}\n"
        text += f"to: {self.end_frame()}\n"
        return text

    @property
    def internal_id(self) -> int:
        """
        An object-unique integer to distinguish between MDMolecule objects.
        """
        return self._internal_id

    @internal_id.setter
    def internal_id(self, value: int):
        self._internal_id = value

    @property
    def name(self) -> str:
        """
        A placeholder for a name.
        """
        return self._name

    @name.setter
    def name(self, value: str):
        self._name = value

    def atoms(self) -> tuple[int]:
        """
        The integer atom IDs as set during construction. In general, those are not consecutive.
        """
        return self.graph.atoms

    def end_frame(self) -> float:
        """
        The frame number at which the molecule cease to exist in a simulation. Returns float('inf') when the molecule persists.
        """
        return (
            min([successor.start_frame for successor in self.successors])
            if self.successors
            else float("inf")
        )


@dataclass
class RateConstantRecord:
    """
    A helper class for storing info about 1 reaction.
    :param flux: list of directions, +1 for forward, -1 for backward, 0 otherwise
    :param rate: rate constant in cm3, mol, s
    :param events: number of reactive events
    :param integral: concentration integral
    :param upper_k: upper bound for rate constant
    :param lower_k: lower bound for rate constant
    :param rateB: reverse rate constant
    :param eventsB: number of reverse reactive events
    :param integralB: concentration integral for reverse reaction
    :param upper_kB: upper bound for reverse rate constant
    :param lower_kB: lower bound for reverse rate constant
    """

    flux: list = None
    rate: int = 0
    events: int = 0
    integral: int = 0
    upper_k: float = 0.0
    lower_k: float = 0.0
    rateB: int = 0
    eventsB: int = 0
    integralB: int = 0
    upper_kB: float = 0.0
    lower_kB: float = 0.0


################################################################################
# trajectory
################################################################################


class Trajectory(ChainOfStates):
    """
    Container for contigous atom trajectories of a molecular dynamics simulation
    with a constant number of atoms.

    .. note::

        While box_vectors, box_origin, graphs and coords can be set
        indepentently from each other, it is the responsibility of the caller,
        that they must have the same length along the first axis, i.e., the axis
        representing the frame index

    :param metadata:
    :param atom_types:
    :param coords:
    :param box_vectors: if None, the box vectors from metadata are used (only if
                        no barostat is used)
    :param box_origin: if None, the box origin from metadata is used
    :param first_timestep:
    """

    metadata: MDMetadata
    """container for MD settings like number of steps, etc."""
    box_vectors: np.ndarray
    """n_frames x 3 x 3 array containing the box vectors (in each column/along
    second axis) for each frame
    """
    box_origin: np.ndarray
    """n_frames x 3 array containing the origin of the box
    """
    first_timestep: int
    """id of the first timestep in case this object contains only a part of the
    trajectory
    """
    charges: np.ndarray = None
    graphs: list[MolGraph] = None
    """connectivities for each frame. The atom/node ids are considered to be the
    same as in `coords` and `atom_types`
    """

    def __init__(
        self,
        *,
        metadata: MDMetadata,
        atom_types: tuple[Element],
        coords: Iterable[Iterable[Iterable[float]]],
        box_vectors: np.ndarray = None,
        box_origin: np.ndarray = None,
        graphs: list[MolGraph] = None,
        first_timestep: int = 0,
    ):
        self.metadata: MDMetadata = metadata

        if box_vectors is None:
            if metadata.barostat is None:
                # brodcasting creates a readonly view with the correct size, but
                # does not copy the values -> it looks like a n_frame x 3 x 3
                # array but stores only 9 numbers
                self.box_vectors = np.broadcast_to(
                    metadata.box_vectors, (len(coords), 3, 3)
                )
            else:
                raise ValueError(
                    "box_vectors must be provided if a barostat is " "used"
                )
        else:
            box_vectors = np.array(box_vectors)
            if box_vectors.shape != (len(coords), 3, 3):
                raise ValueError("box_vectors must have the shape n_frames x 3 x 3")
            self.box_vectors = box_vectors

        if box_origin is None:
            self.box_origin = np.broadcast_to(metadata.box_origin, (len(coords), 3))
        else:
            box_origin = np.array(box_origin)
            if box_origin.shape != (len(coords), 3):
                raise ValueError("box_origin must have the shape n_frames x 3")
            self.box_origin = box_origin

        self.first_timestep = first_timestep
        self.graphs = graphs

        super().__init__(atom_types=atom_types, coords_list=coords)

    def __str__(self):
        """
        Prints some information about the trajectory.

        :return: str
        """
        text = "CTY3 Trajectory\n"
        text += f"{self.n_frames()} frames * {self.metadata.timestep} fs/frame = {self.length()} fs\n"
        if self.graphs is not None:
            text += "has connectivity\n"
        if self.charges is not None:
            text += "has charges\n"
        text += str(self.metadata)
        return text

    def __getitem__(self, n: int):
        """
        Returns the geometry of the specified frame.

        :param n: frame number
        :type n: int
        :return: Geometry
        """
        return self.get_geometry(n)

    def length(self):
        """
        Returns the length of the trajectory in femtoseconds.

        :return: length of the trajectory in femtoseconds
        """
        if self.metadata.timestep is None:
            return 0
        return self.metadata.timestep * (self.n_frames() - 1)

    def cell_volume(self, n: int | slice):
        """
        :param n: frame number(s) at which to return the cell volume
        :return: the cell volume of the trajectory [Angstrom^3]
        """
        return np.abs(np.linalg.det(self.box_vectors[n]))


class TrajectoryParser(ABC):
    """
    base class for trajectory parsers
    """

    @abstractmethod
    def parse(self, n_steps: int = -1) -> Trajectory:
        """
        parses a piece (or all) of the trajectory

        :param n_steps: Read at most this many steps from the file and
                        remember how many steps have been read. A subsequent
                        call to this function should continue from the first
                        step, that has not been read yet. By default (-1),
                        the whole trajectory is read
        :return: piece of the trajectory that has been read. The trajectory
                 may be empty, if it has been read, completely"""

@dataclass
class XYZTrajectoryParser(TrajectoryParser):
    """
    Trajectory parser for  xyz files 
    """

    filename: PathLike
    metadata: MDMetadata
    
    def __post_init__(self):
        self._pos = 0
        with open(self.filename, "r", encoding="utf-8") as xyz_file:
            self._n_atoms = int(xyz_file.readline())
            _ = xyz_file.readline()
            self.atom_types = tuple(PTOE[xyz_file.readline().split()[0]] for _ in range(self._n_atoms))

    def parse(self, n_steps):
        if self._pos == None:
            raise StopIteration()
            
        with open(self.filename, "r", encoding="utf-8") as xyz_file:
            xyz_file.seek(self._pos, 0) 
            traj = []
            for step in range(n_steps):
                n_atoms, _ = xyz_file.readline(), xyz_file.readline()
                    
                if n_atoms.strip() == "":
                    self._pos = None
                    break
                yd = [[float(coord) for coord in  xyz_file.readline().split()[1:4]] 
                           for line in range(self._n_atoms)]
                traj.append(yd)
                self._pos = xyz_file.tell()

        return Trajectory(atom_types=self.atom_types, coords=np.array(traj), metadata=self.metadata)



################################################################################
# MD job
################################################################################
class MDJob(Job):
    """
    Job for running a molecular dynamics simulation.
    """

    result: Result

    @dataclass
    class Result(Job.Result, TrajectoryParser):
        """Container for storing MD-Output, and parser."""


class MDJobFactory(ABC):
    """
    Base Class for MDJob factories.
    """

    @abstractmethod
    def create(
        self,
        metadata: MDMetadata,
        initial_geometry: Geometry,
        name: str = None,
    ) -> MDJob:
        """
        create a MDJob
        :param metadata: options and settings for MD
        :param initial_geometry: initial box geometry
        :param name: optional name
        """
