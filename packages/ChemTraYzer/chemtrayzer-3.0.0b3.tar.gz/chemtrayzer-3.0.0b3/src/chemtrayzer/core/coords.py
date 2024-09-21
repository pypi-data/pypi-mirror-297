"""Molecular coordinates

This module contains classes for representing molecular systems and their
evolution as atomic coordinates.
"""

from __future__ import annotations

import operator
import re
from io import TextIOWrapper
from itertools import chain, repeat
from numbers import Number
from os import PathLike
from typing import (
    Any,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union,
    overload,
)

import numpy as np
import rdkit  # type: ignore
import scipy  # type: ignore
from rdkit import Chem  # type: ignore
from rdkit.Chem import AllChem  # type: ignore
from typing_extensions import Self

from chemtrayzer.core.constants import h_bar, k_B
from chemtrayzer.core.periodic_table import PERIODIC_TABLE as PTOE
from chemtrayzer.core.periodic_table import Element


def calc_distance_matrix(coords, box_size: Tuple[float, float, float] = (0, 0, 0),
                  periodic: str = 'xyz')-> np.ndarray:
    """
        calculates atom pairwise atom distances for large (periodic) system
        :param coords: cartesian coordinates of atoms
        :type coords: np.ndarray
        :param box_size: size of simulation box as tuple (x,y,z)
        :type box_size: Tuple(float, float, float)
        :param periodic: string with periodicity definition 'xyz','xy','xz','yz','x','y','z', optional
        :type periodic: str
        :returns: distance matrix and the metric dist(u=X[i], v=X[j])
    """

    period_dim = set() if not periodic else {{'x': 0, 'y': 1, 'z': 2}[d] for d in periodic}
    not_period_dim = {0, 1, 2} - period_dim
    n_atoms = np.shape(coords)[0]
    dist_nd_sq = np.zeros(n_atoms * (n_atoms - 1) // 2)  # to match the output of pdist

    for d in period_dim:
        pos_1d = coords[:, d][:, np.newaxis]  # shape (N, 1)
        dist_1d = scipy.spatial.distance.pdist(pos_1d)  # shape (N * (N - 1) // 2, )
        dist_1d[dist_1d > box_size[d] * 0.5] -= box_size[d]
        dist_nd_sq += np.square(dist_1d)  # d^2 = dx^2 + dy^2 + dz^2
    for d in not_period_dim:
        pos_1d = coords[:, d][:, np.newaxis]  # shape (N, 1)
        dist_1d = scipy.spatial.distance.pdist(pos_1d)  # shape (N * (N - 1) // 2, )
        dist_nd_sq += np.square(dist_1d)  # dx^2
    condensed_distance_matrix = np.sqrt(dist_nd_sq)  # d = sqrt(dx^2 + dy^2 + dz^2)
    distance_matrix = scipy.spatial.distance.squareform(condensed_distance_matrix)
    return distance_matrix

class InvalidXYZFileError(Exception):
    """Thrown when trying to read an xyz file with an unsupported format"""


class Geometry:
    """
    Represents a molecular geometry, i.e. the coordinates and type of one or
    more atoms.

    Equality for geometries is determined based on the atom types and coordinates.
    To check if two geometries are similar, use rmsd()

    Note: The hash function and == operator are not safe to use accross
    different maschines, because the endianess of the data is ignored.

    :param atom_types: list of strings containing symbol for each atom
    :type atom_types: Iterable[Element]
    :param coords: nAtomsx3 numpy array with cartesian coordinates
    :type coords: np.array
    """

    def __init__(self, atom_types: Iterable[str|int|Element] = None,
                 coords: np.ndarray = None):
        if atom_types is not None and coords is not None:
            self.atom_types = tuple([PTOE[type] for type in atom_types])
            self._check_coords_shape(coords)
            self.coords = np.array(coords)
            if self.n_atoms != np.shape(self.coords)[0]:
                raise ValueError("Number of atoms and coordinates do not match")
        else:
            self.coords = np.empty(shape=[0, 3])
            self.atom_types = tuple()


    @staticmethod
    def _check_coords_shape(coords) -> None:
        for atom_coord in coords:
            if len(atom_coord) != 3:
                raise ValueError("wrong cartesian coordinates input")
            for i in atom_coord:
                if not isinstance(i, Number):
                    raise ValueError(f"{i} wrong cartesian coordinates input")

    @property
    def n_atoms(self) -> int:
        return len(self.atom_types)

    def xyz_str(self, comment:Optional[str] = None) -> str:
        '''
        returns the xyz representation of this geometry as a string

        :param comment: comment for 2nd line of xyz file
        :return: xyz representation of this geometry
        '''
        xyz = str(self.n_atoms)+'\n'
        if comment is not None:
            xyz += comment+'\n'
        else:
            xyz += '\n'

        for type, coords in zip(self.atom_types, self.coords):
            xyz += f'{type.symbol:s} {coords[0]:.8f} {coords[1]:.8f} {coords[2]:.8f}\n'

        return xyz

    def to_xyz(self, path: PathLike, comment: Optional[str] = None, overwrite:bool=False) -> None:
        """
        Writes coordinates into an xyz file.

        :param path: path-like object that points to the xyz file
        :param comment: comment for 2nd line of xyz file
        :param overwrite: if True, replaces file contents, otherwise appends
        """
        mode = "w" if overwrite else "a"
        with open(path, mode, encoding="utf-8") as file:
            file.write(str(self.n_atoms) + "\n")
            if comment is not None:
                file.write(comment + "\n")
            else:
                file.write("\n")
            for type, coords in zip(self.atom_types, self.coords):
                file.write(
                    f"{type:s} {coords[0]:.8f} {coords[1]:.8f} {coords[2]:.8f}\n")

    @overload
    @classmethod
    def from_xyz_file(cls, path: PathLike, comment:Literal[False]) -> Geometry: ...

    @overload
    @classmethod
    def from_xyz_file(cls, path: PathLike, comment:Literal[True]) -> Tuple[Geometry, str]: ...

    @classmethod
    def from_xyz_file(cls, path: PathLike, comment:bool=False) -> Geometry | Tuple[Geometry, str]:
        """
        Creates a Geometry object from an xyz file

        returns: (obj : Geometry, comment : str)
        """

        with open(path, "r", encoding="utf-8") as xyz_file:
            return cls._from_opened_xyz_file(xyz_file, comment=comment)

    @overload
    @classmethod
    def _from_opened_xyz_file(cls, file: TextIOWrapper, comment:Literal[False]) -> Geometry: ...

    @overload
    @classmethod
    def _from_opened_xyz_file(cls, file: TextIOWrapper, comment:Literal[True]) -> Tuple[Geometry, str]: ...

    @overload
    @classmethod
    def _from_opened_xyz_file(cls, file: TextIOWrapper, comment:bool=False) -> Geometry | Tuple[Geometry, str]: ...

    @classmethod
    def _from_opened_xyz_file(cls, file: TextIOWrapper, comment:bool=False, ignore_additional_lines=False) -> Geometry | Tuple[Geometry, str]:
        """
        reads n_atoms atoms from file and creates Geometry object

        :param file: xyz file object where the pointer sits on the first line of the xyz section, i.e. the line with the number of atoms
        :return: Geometry object and comment section of xyz section
        """
        try:
            n_atoms = int(file.readline())  # 1st line contains num of atoms
        except ValueError as e:
            raise InvalidXYZFileError("First line not an integer.") from e

        comment_str = file.readline().strip()  # second line is comment

        atom_types = []
        coordinates = np.zeros((n_atoms, 3))
        n_atoms_read = 0
        lines_operator = operator.lt if ignore_additional_lines else operator.ne
        # use this construct instead of `for line in file` such that tell() is
        # not disabled as it is being used in `multiple_from_xyz`
        line = file.readline()
        while line:
            words = line.split()

            if words == []:  # terminate by empty line
                break

            atom_types.append(words[0])  # first word in line is atom name

            # next three words contain coordinates
            try:
                coordinates[n_atoms_read, :] = np.array(words[1:4])
            except ValueError as e:
                raise InvalidXYZFileError() from e

            # if more than 4 lines are given, the remaining are ignored.
            if lines_operator(len(words),4):
                raise InvalidXYZFileError("Unexpected number of columns.")

            # only read as many lines as specified
            n_atoms_read += 1
            if n_atoms_read >= n_atoms:
                break

            line = file.readline()

        if n_atoms_read != n_atoms:
            raise InvalidXYZFileError("Fewer atoms than specified.")
        if comment is True:
            return cls(atom_types, coordinates), comment_str
        elif comment is False:
            return cls(atom_types, coordinates)
        else:
            raise ValueError(f"comment is set to {type(comment)}: {comment} and should be a bool")


    @overload
    @classmethod
    def multiple_from_xyz_file(cls, path: PathLike, comment:Literal[False], max=np.inf) -> List[Geometry] : ...

    @overload
    @classmethod
    def multiple_from_xyz_file(cls, path: PathLike, comment:Literal[True], max=np.inf) -> Tuple[List[Geometry], List[str]]: ...

    @classmethod
    def multiple_from_xyz_file(
        cls, path: PathLike, comment:bool=False, max=np.inf,
    ) -> List[Geometry]  | Tuple[List[Geometry], List[str]]:
        """
        Creates several Geometry objects from a single xyz file which contains
        several sections each formatted like an xyz file (i.e. beginning with
        the number of atoms and a comment). This can be used to quickly read in
        CREST output.

        :param path: path to xyz file
        :param max: maximum number of objects that should be read/created
        :param returns: objs : list(Geometry), comments : list(str)
        :param comment: if True, the comment section of each xyz section is included, default: False
        """

        with open(path, "r", encoding="utf-8") as xyz_file:
            geos:List[Geometry] = []
            comments: List[str] = []
            while len(geos) <= max:
                geo, comment_str = cls._from_opened_xyz_file(xyz_file, comment=True)
                comments.append(comment_str)
                geos.append(geo)

                # peek ahead to check for empty lines
                pos = xyz_file.tell()
                if xyz_file.readline().strip() == "":
                    break
                xyz_file.seek(pos)
        if comment is True:
            return geos, comments
        elif comment is False:
            return geos
        else:
            raise ValueError(f"comment is set to {type(comment)}: {comment} and should be a bool")

    @classmethod
    def from_inchi(cls, inchi: str) -> Geometry:
        """
        generate a geometry from an InChI. Results may vary.

        :param inchi: InChI
        :return: generated geometry
        """
        from chemtrayzer.core.chemid import _rdkit_mol_from_inchi

        mol = _rdkit_mol_from_inchi(inchi)

        return cls._from_rdkit_mol(mol)

    @classmethod
    def _from_rdkit_mol(cls, mol: rdkit.Chem.Mol) -> Geometry:
        """This method is private because the dependency on RDKit should not be public"""
        # Compute 3D coordinates
        AllChem.EmbedMolecule(mol, randomSeed=42)  # Using a fixed random seed for reproducibility
        AllChem.MMFFOptimizeMolecule(mol)

        coords = np.zeros((mol.GetNumAtoms(), 3))
        atom_types = []

        for i, atom in enumerate(mol.GetAtoms()):
            pos = mol.GetConformer().GetAtomPosition(i)
            coords[i, 0] = pos.x
            coords[i, 1] = pos.y
            coords[i, 2] = pos.z
            atom_types.append(atom.GetAtomicNum())

        return Geometry(atom_types=atom_types, coords=coords)

    def to_sdf(
            self,
            path,
            name: str,
            comment: str = None,
            append: bool = True,
            associated_data: Dict[str, str] = None) -> None:
        """
        Creates an SDF file for this geometry.

        :param path: path where the SDF file should be created
        :param name: name of this geometry in the header block of the molfile
        :param comment: comment for this geometry in the header block
        :param append: if true and an SDF file already exists at path, this
                       geometry will be added to the end of the file
        :param associated_data: data that should be added to the data part of
                                the SDF file.
        """
        from chemtrayzer.core.chemid import _rdkit_mol_from_geometry

        rdkitmol = _rdkit_mol_from_geometry(self)

        mol_block = Chem.MolToMolBlock(rdkitmol)
        lines: List[str] = mol_block.splitlines()

        # check if name, comment, and data are in agreement with SD file standard
        if comment is None:
            comment = ""
        else:
            if "\n" in comment:
                raise ValueError("No new lines allowed in comment")
            if "$$$$" in comment:
                raise ValueError(
                    'SD file record separator "$$$$" not allowed in comment.'
                )
            if "$$$$" in name:
                raise ValueError('SD file record separator "$$$$" not allowed in name.')

        if associated_data is not None:
            for field_name, data in associated_data.items():
                if not re.match("^[A-Za-z][A-Za-z0-9_]+$", field_name):
                    raise ValueError(
                        f'Invalid field name "{field_name}":\nField '
                        "names must begin with an alphabetic character which can be"
                        " followed by alphanumeric characters and underscores"
                    )

                for line in data.splitlines():
                    reason = None
                    if line.startswith("$$$$"):
                        reason = (
                            'Lines cannot start with SD file record separator "$$$$".'
                        )
                    elif len(line) > 200:
                        reason = "Lines can contain only up to 200 characters."
                    elif line.strip() == "":  # blank lines terminate the data entry
                        reason = "Data cannot contain blank lines."
                    if reason is not None:
                        raise ValueError(
                            f'Illegal data for field "{field_name}":\n' f"{reason}"
                        )

            for field_name, data in associated_data.items():
                lines.append(f"> <{field_name}>")
                # remove possible leading and trailing new lines
                lines.append(data.strip())
                lines.append("")  # data entries are terminated by blank lines
        # add seperator
        lines.append("$$$$")

        # first line is the title, third one is the comment
        lines[0] = name
        lines[2] = comment

        mode = "a" if append else "x"

        with open(path, mode, encoding="utf-8") as file:
            # if the file is not empty we need to add a new line before adding
            # the content
            if append and file.tell() != 0:
                file.write("\n")

            file.write("\n".join(lines))

    @property
    def molecular_weight(self) -> float:
        """molecular weight of this geometry in amu"""
        mw = 0.0

        for elem in self.atom_types:
            mw += elem.mass

        return mw

    def split_fragments(self) -> List[Geometry]:
        from chemtrayzer.core.chemid import _rdkit_mol_from_geometry

        mol = _rdkit_mol_from_geometry(self)

        fragments = []

        for fragment in Chem.GetMolFrags(mol):
            atom_ids = [atom for atom in fragment]

            atom_types = [self.atom_types[atom_id] for atom_id in atom_ids]

            coords = [self.coords[atom_id] for atom_id in atom_ids]

            fragments.append(Geometry(atom_types, coords))

        return fragments

    def __hash__(self) -> int:
        return hash(self.coords.tobytes()) ^ hash(self.atom_types)

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o) and type(__o) is __class__

    def __len__(self) -> int:
        return len(self.atom_types)

    def align(self, other: Geometry, mass_weighted=False,
              align_atoms:Optional[Iterable[int]]=None) -> Self:
        """Aligns the geometry to another geometry by translating and rotating it.
        Operation is done in place.
        Atoms have to be in the same order in both geometries!

        :param other: Geometry the structure should be aligned to
        :type other: Geometry
        :param mass_weighted: if True,  with mass weighting
        :param align_atoms: list of atom indices that should be aligned by rotation.
                            If None, all atoms are used.
                            Useful to align not active atoms in reactions.
                            Default: None
        :type align_atoms: Iterable[int]
        """
        self.coords -= self.center_of_mass()
        self.coords += other.center_of_mass()

        weights = np.array([el.mass if mass_weighted else 1
                           for el in self.atom_types])
        if  align_atoms is not None:
            for atom in align_atoms:
                weights[atom] = 0

        rot_mat, _rmsd = scipy.spatial.transform.Rotation.align_vectors(other.coords, self.coords, weights=weights)
        self.coords = rot_mat.apply(self.coords)

        return self #Geometry(deepcopy(self.atom_types), new_coords) if copy else self

    def rmsd(self, other: Geometry, mass_weighted=False, rigid_rotation=False,
             center_of_mass=False, permute=False) -> float:
        """computes the root-mean-square distance to another geometry

        :param mass_weighted: if true, each coordinate is weighted by its atomic
                              mass instead of one
        :type mass_weighted: bool
        :param rigid_rotation: uses the Kabsh algorithm to align the two
                            geometries to get the minimal RMSD w.r.t. rotation
        :type rigid_rotation: bool
        :param center_of_mass: move the centers of mass of one geometry on the
                               the other before comparing
        :type center_of_mass: bool
        :param permute: take the minimal RMSD of all isomorphic mappings of the
                            graph representation of the two geometries
        :return: RMSD
        :rtype: float
        """

        if not self.n_atoms == other.n_atoms:
            raise ValueError("The number of atoms must be equal.")

        if permute is False:
            if not all([self_t == other_t for self_t, other_t in zip(self.atom_types, other.atom_types)]):
                raise ValueError("Atoms must be of the same type.")

        if permute is True:
            from chemtrayzer.core.graph import MolGraph

            self_graph = MolGraph.from_geometry(geo=self)
            other_graph = MolGraph.from_geometry(geo=other)
            rmsd_list = []
            for mapping in self_graph.get_isomorphic_mappings(other_graph):
                mapped_atom_types = [other.atom_types[mapping[i]] for i in range(self.n_atoms)]
                mapped_coords = np.array([other.coords[mapping[i]] for i in range(self.n_atoms)])
                mapped_other = Geometry(mapped_atom_types, mapped_coords)

                rmsd_list.append(self.rmsd(mapped_other,
                                           mass_weighted=mass_weighted,
                                           rigid_rotation=rigid_rotation,
                                           center_of_mass=center_of_mass,
                                           permute=False))
            if len(rmsd_list) == 0:
                raise ValueError("No isomorphic mapping found.")
            return min(rmsd_list)

        # rotated or translated coordinates are copied into this variable,
        # if requested
        other_coords = other.coords
        self_coords = self.coords

        if center_of_mass:
            other_coords = other_coords - other.center_of_mass()
            self_coords = self_coords - self.center_of_mass()

        masses = np.array([el.mass if mass_weighted else 1
                           for el in self.atom_types])

        if rigid_rotation:
            _, rmsd = scipy.spatial.transform.Rotation.align_vectors(
                    self_coords, other_coords, weights=masses)
        else:
            M = np.sum(masses)
            rmsd = np.sqrt(1/M*np.sum(np.sum((self_coords - other_coords) ** 2, axis=1) * masses))

        return rmsd

    def moment_of_inertia(self) -> Tuple[np.ndarray, np.ndarray]:
        """Computes the inertia tensor w.r.t. the geometries center of mass and
        returns its eigenvalues and the principal axes

        .. note::
            This method assumes that the unit of length for this object is
            Angstrom!

        :return: eigenvalues in ascending order in atomic
                 units [a_0^2 amu] and a 3x3 matrix where each column contains a
                 principal axis
        """
        masses = np.array([el.mass for el in self.atom_types])

        centered = self.coords - self.center_of_mass()
        # convert to Bohr radii
        a_0 = 1.88972612463  # [Angstrom]
        centered *= a_0

        # move origin to center of mass and mass weight the coordinates
        mass_weighted_coords = centered * np.sqrt(masses[:, np.newaxis])

        # construct moment of inertia tensor
        # after this element x,y of this matrix contains -\sum_i^N m_i x_i y_i
        # meaning that the off-diagonal entries are correct
        I = -mass_weighted_coords.T @ mass_weighted_coords

        # extract \sum_i^N m_i x_i^2   (same with y and z)
        mx2 = -I[0, 0]
        my2 = -I[1, 1]
        mz2 = -I[2, 2]

        # fill diagonal elements
        I[0, 0] = my2 + mz2
        I[1, 1] = mx2 + mz2
        I[2, 2] = mx2 + my2

        return np.linalg.eigh(I)  # eigenvalues, principal axis

    def rotational_constants(self) -> Tuple[float, float, float]:
        r"""
        :return: :math:`\frac{\bar h^2}{2 \text{MOI}}` where MOI are the
                 principal moments of inertia
        """
        return (h_bar**2) / (2 * self.moment_of_inertia()[0])

    def center_of_mass(self) -> np.ndarray:
        """returns the center of mass of the cartesian coordinates"""
        masses = np.array([atom.mass for atom in self.atom_types])

        return np.average(self.coords, axis=0, weights=masses)

    def wrap(
        self,
        box_size: Tuple[float, float, float],
        periodic_boundary_conditions: Tuple[bool, bool, bool] = (True, True, True),
    ):
        """applies the periodic boundary conditions to shift all atoms inside one predefined box
        center ist at 0, 0, 0"""

        half_box = np.array(
            [
                (box_size[i] / 2 if v else np.inf)
                for i, v in enumerate(periodic_boundary_conditions)
            ]
        )

        #self.coords = np.fmod(self.coords, half_box)
        half_box = np.array([box_size[i] / 2 for i in range(3)])

        for i, periodic in enumerate(periodic_boundary_conditions):
            if periodic is True:
                # Shift coordinates to ensure positive values before wrapping
                positive_shift = self.coords[:, i] + box_size[i]/2
                # Apply wrapping and then shift back
                self.coords[:, i] = (positive_shift % (box_size[i])) - box_size[i]/2
            # Non-periodic dimensions are left unchanged, so no else clause is needed

        return self.coords

    def unbreak_molecule(self,
                         box_size: Tuple[float, float, float],
                         periodic_boundary_conditions: Tuple[bool, bool, bool] = (True, True, True),
                         zero_com=False):
        '''
            Wrap back parts of the Geometry which have been split off due to periodic boundary conditions.
            This is mandatory to start a COM calculation or an optimization in another program.
            Returns the final displacement vector (n_atoms x 3) in case it is needed for other geometries.

            Set zero_com to True to center the Geometry around the center of mass.
            E.g.: [o  oO] --> oO[o    ] --> oO-o

            :param box_size: size of orthogonal simulation box as tuple (x,y,z)
            :param periodic_boundary_conditions: flags boundary condiditons as periodic or infinite
            :param zero_com: centers the atoms around their COM
            :returns: the final displacement vector
            :rtype: np.ndarray (n_atoms x 3)
        '''
        orig = self.coords.copy()

        # do per dimension i
        for i in [0, 1, 2]:
            if not periodic_boundary_conditions[i]:
                continue

            # box length + coordinates
            l = box_size[i]
            x = self.coords[:, i]
            # sort by value
            xs = np.sort(x)

            # find all gaps between atoms along dimension i
            dx = np.diff(xs, append=xs[0] + l)
            # [o  oO]  atom coord left of biggest gap
            #  ^
            z = xs[np.argmax(dx)]
            # oO[o    ]  shift all atoms which are right of the gap back one box length
            #  <-----|
            x[x > z] -= l

        if zero_com:
            #  [ oO-o ]  shift all atoms towards the origin
            # |--->
            self.coords -= self.center_of_mass()

        # return the displacment after-before
        return self.coords - orig

    def distance_matrix(
        self, box_size: Tuple[float, float, float] = (0, 0, 0), periodic: str = "xyz"
    ) -> np.ndarray:
        """
        calculates atom pairwise atom distances for large (periodic) system

        :param box_size: size of simulation box as touple (x,y,z)
        :type box_size: Tuple(float, float, float)
        :param periodic: string with periodicity definition 'xyz','xy','xz','yz','x','y','z', optional
        :type periodic: str
        :returns: distance matrix and the metric dist(u=X[i], v=X[j])
        """

        return calc_distance_matrix(self.coords, box_size, periodic)


class TSGeometry(Geometry):
    """
    Represents the geometry of a transition state and contains additional
    information like the active atoms

    :param atom_types: list of strings containing symbol for each atom
    :type atom_types: Iterable[Element]
    :param coords: nAtomsx3 numpy array with cartesian coordinates
    :type coords: np.array
    :param multiplicity: spin multiplicity
    :type multiplicity: float, optional
    :param active: list of zero-based ids of active (in the reaction) atoms
    """

    def __init__(
        self,
        atom_types: Iterable[str|int|Element],
        coords: np.array,
        multiplicity: float = None,
        active: Iterable[int] = None,
    ):
        super().__init__(atom_types, coords)

        if active is not None:
            self.active = tuple(active)
        else:
            self.active = tuple()

    def __hash__(self) -> int:
        return hash(self.coords.tobytes()) ^ hash(self.atom_types) ^ hash(self.active)

    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o) and type(__o) is __class__

    @classmethod
    def from_geometry(cls, geo: Geometry, active: List = None):
        """
        translates a Geometry into a TSGeometry by adding active atoms

        :param geo: Geometry
        :param active: List of IDs of active atoms in the geometry (start at 1).
        :return: TSGeometry object
        """
        return cls([t.atomic_nr for t in geo.atom_types], geo.coords, active=active)


class ChainOfStates:
    """
    Container for multiple geometries.

    :param geometries:List of geometries to create to use the coordinates and atom types from
    :type geometries: List[Geometries]
    :param atom_types: elements of the atoms in the correct order, Optional
    :type atom_types: Iterable[Element]
    :param coords: n_steps x n_atoms x 3 array containing atomic coordinates.
    :type coords: np.ndarray
    """

    atom_types: List[Element]
    """elements of the atoms in the correct order"""
    coords: np.ndarray
    """n_steps x n_atoms x 3 array containing atomic coordinates."""

    def __init__(
        self,
        *,
        geometries: Iterable[Geometry] = None,
        coords_list=None,
        atom_types: Iterable[Element|int|str] = None,
    ):
        if geometries is None and coords_list is None and atom_types is None:
            self.coords = None
            self.atom_types = None

        # populate from list of coordiantes and atom types
        elif geometries is None and (
            coords_list is not None and atom_types is not None
        ):
            self.atom_types = [PTOE[i] for i in atom_types]
            self.set_coords(coords_list)

        # populate from list og geomtries
        elif geometries is not None and (coords_list is None and atom_types is None):
            self.atom_types = geometries[0].atom_types

            if not all(geo.atom_types == self.atom_types for geo in geometries):
                raise ValueError("All geometries have to have the same " "atom_types")

            self.set_coords(geometries)

        # illegal combination of inputs
        else:
            raise ValueError(
                "Takes only one, either, geometries or " "coords_list and atom_types."
            )

    def set_coords(self, input: List[Union[Geometry, List[List[List[float]]]]]):
        """set the coordinates using a list of Geometries, or a list of lists"""
        if all(isinstance(i, Geometry) for i in input):
            self.coords = self._make_coords_from_geometries(input)
        else:
            self.coords = self._make_coords_from_coords_list(input)

    def _make_coords_from_geometries(self, geometries: Sequence[Geometry]) -> np.ndarray:
        self._check_geometries_shape_and_types(geometries)
        if getattr(self, "atom_types", None) and len(geometries[0].atom_types) != len(
            self.atom_types
        ):
            raise ValueError(
                "geometries should have the same number of atoms as the chain_of_states"
            )
        return np.array([geom.coords for geom in geometries])

    def _make_coords_from_coords_list(self, coords_list) -> np.ndarray:
        self._check_coords_list_shape(coords_list)
        if self.atom_types is not None and len(self.atom_types) != len(coords_list[0]):
            raise ValueError(
                "the coordinates should have the same number of atoms as in atom_types"
            )
        return np.array(coords_list)

    def set_atom_types(self, input: Union[Geometry, List[Element]]) -> None:
        """
        :param input: either a list of atom types or a geometry object
        """
        if self.n_atoms() > 0 and self.n_atoms() != len(input):
            raise ValueError(
                "set atom types need to have the same number of atoms as the coordinates"
            )
        if isinstance(input, Geometry):
            self.atom_types = input.atom_types
        elif all(isinstance(PTOE[i], Element) for i in input):
            self.atom_types = [PTOE[i] for i in input]
        else:
            raise ValueError("not valid atom types")

    def n_frames(self) -> int:
        """
        :returns: number of frames"""
        if getattr(self, "coords", None) is None:
            return 0
        return np.shape(self.coords)[0]

    def n_atoms(self) -> int:
        """
        :returns: number of atoms in the first frame
        """
        if getattr(self, "coords", None) is None:
            return 0
        return np.shape(self.coords)[1]

    def xyz_str(self, comments:List[str]=None,) -> str:
        xyz_str = ""
        comments = repeat("") if comments is None else chain(comments,repeat(""))
        for i, (comment, frame_coords) in enumerate(zip (comments, self.coords)):
            xyz_str += self.get_geometry(i).xyz_str(comment=comment)
        return xyz_str

    @staticmethod
    def _check_coords_list_shape(coords_list):
        for coords in coords_list:
            Geometry._check_coords_shape(coords)
            if len(coords) != len(coords_list[0]):
                raise ValueError("every frame should have the same number of atoms")

    @staticmethod
    def _check_geometries_shape_and_types(geometries: Iterable[Geometry]) -> None:
        """
        checks if number of atoms and atom_type is the same for all geometries
        coords shape and atom_types have been checked at creation of each geometry
        """
        if not all(
            geometry.n_atoms == geometries[0].n_atoms for geometry in geometries
        ):
            raise ValueError(
                "All geometries have to have the same number of atoms of the same atom_type"
            )
        if not all(
            len({atoms_with_same_index}) == 1
            for atoms_with_same_index in zip(
                *(geometry.atom_types for geometry in geometries)
            )
        ):
            raise ValueError(
                "All geometries have to have the same number of atoms of the same atom_type"
            )

    def get_geometry(self, frame: int, atoms: List[int] = None) -> Geometry:
        """
        """
        if atoms is None:
            return Geometry(atom_types=self.atom_types, coords=self.coords[frame])
        else:
            return Geometry(
                atom_types=[self.atom_types[atomid] for atomid in atoms], coords=self.coords[frame][atoms]
            )

    def insert(self, position:int, *, coords:Optional[Iterable]=None, coords_list:Optional[Iterable]=None, geom: Optional[Geometry] = None,
        geometries: Optional[Iterable[Geometry]] = None) -> None:
        """
        inserts the input geometry onto the given position.
        all following images are pushed back by the number of inserted frames.
        """
        num_inputs = sum(map(bool, (coords, coords_list, geom, geometries)))
        if num_inputs != 1:
            raise ValueError(f"one input is expected, but {num_inputs} where given ")
        if coords is not None:
            coords_to_insert = self._make_coords_from_coords_list([coords])
        elif coords_list is not None:
            coords_to_insert = self._make_coords_from_coords_list(coords_list)
        elif geom is not None:
            coords_to_insert = self._make_coords_from_geometries([geom])
        elif geometries is not None:
            coords_to_insert = self._make_coords_from_geometries(geometries)
        if position > self.n_frames():
            raise IndexError(
                f"can not add an image at position {position} for an object with {self.n_frames} frames"
            )
        elif position == self.n_frames():
            self.coords: np.ndarray = np.concatenate((self.coords, coords_to_insert))
        elif position == 0:
            self.coords: np.ndarray = np.concatenate((coords_to_insert, self.coords))
        else:
            self.coords: np.ndarray = np.concatenate(
                (
                    self.coords[0:position],
                    coords_to_insert,
                    self.coords[position : self.n_frames()],
                )
            )

    def append(self, *, coords:Optional[Iterable]=None, coords_list:Optional[Iterable]=None, geom: Optional[Geometry] = None,
        geometries: Optional[Iterable[Geometry]] = None) -> None:
        self.insert(self.n_frames(), coords_list=coords_list,
                    geom=geom, geometries=geometries)

    @classmethod
    def from_xyz_file(cls, filepath:PathLike, comment=False) -> ChainOfStates|Tuple[ChainOfStates, list[str]]:
        """
        Creates a Geometry object from an xyz file
        :returns: (obj : Chain_of_states, comment : str)
        """
        geometries, comments_str = Geometry.multiple_from_xyz_file(filepath, comment=True)
        chain_of_states = cls(geometries=geometries)
        if comment is True:
            return chain_of_states, comments_str
        return chain_of_states

    def to_xyz(self, filepath: PathLike, comments: Optional[Iterable[str]] = None, overwrite:bool=False) -> None:
        comments = comments if comments is not None else ()
        for i, (comment, frame_coords) in enumerate(
            zip(chain(comments, repeat("")), self.coords)):
            self.get_geometry(i).to_xyz(
                filepath,
                comment=comment,
                overwrite=True if i == 0 and overwrite else False)

    def to_allxyz(self, filepath: PathLike, comments: Optional[Iterable[str]] = None, overwrite:bool=False) -> None:
        comments = comments if comments is not None else ()
        for i, (comment, frame_coords) in enumerate(
            zip(chain(comments, repeat("")), self.coords)
        ):
            self.get_geometry(i).to_xyz(
                filepath,
                comment=comment,
                overwrite=True if i == 0 and overwrite else False,
            )
            with open(filepath, "a") as f:
                f.write(">\n")

    def __eq__(self, other:Any) -> bool:
        if not isinstance(other, ChainOfStates):
            raise ValueError(f"can not compare ChainOfStates with {type(other)}")
        return (self.atom_types == other.atom_types
                and np.allclose(self.coords, other.coords))
