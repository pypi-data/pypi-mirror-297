#
# highly inspired in partially copied from https://github.com/jensengroup/xyz2mol
# Jensen Group
# Jan H. Jensen Research Group of the Department of Chemistry, University of Copenhagen
# License: MIT License (see at end of file)
#
# This code is based on the work of DOI: 10.1002/bkcs.10334
# Yeonjoon Kim and Woo Youn Kim
# "Universal Structure Conversion Method for Organic Molecules:
# From Atomic Connectivity to Three-Dimensional Geometry"
# Bull. Korean Chem. Soc.
# 2015, Vol. 36, 1769-1777
from __future__ import annotations

import copy
import itertools
import sys
from collections import defaultdict
from typing import TYPE_CHECKING, List, Optional
import warnings

import networkx as nx
import rdkit
from rdkit import Chem

from chemtrayzer.core.coords import Geometry
from chemtrayzer.core.periodic_table import Element

if TYPE_CHECKING:
    from chemtrayzer.core.graph import MolGraph

__all__ = ['graph2mol']


atomic_valence = defaultdict(list)
atomic_valence[1] = [1]
atomic_valence[5] = [3,4]
atomic_valence[6] = [4]
atomic_valence[7] = [3,4]
atomic_valence[8] = [2,1,3]
atomic_valence[9] = [1]
atomic_valence[14] = [4]
atomic_valence[15] = [5,3] #[5,4,3]
atomic_valence[16] = [6,3,2] #[6,4,2]
atomic_valence[17] = [1]
atomic_valence[32] = [4]
atomic_valence[35] = [1]
atomic_valence[53] = [1]

atomic_valence_electrons = {}
atomic_valence_electrons[1] = 1
atomic_valence_electrons[5] = 3
atomic_valence_electrons[6] = 4
atomic_valence_electrons[7] = 5
atomic_valence_electrons[8] = 6
atomic_valence_electrons[9] = 7
atomic_valence_electrons[14] = 4
atomic_valence_electrons[15] = 5
atomic_valence_electrons[16] = 6
atomic_valence_electrons[17] = 7
atomic_valence_electrons[32] = 4
atomic_valence_electrons[35] = 7
atomic_valence_electrons[53] = 7

bondTypeDict = {0.5: Chem.BondType.HYDROGEN, # to be drawn as a dotted line (looks better than other options)
                0: Chem.BondType.UNSPECIFIED,
                1: Chem.BondType.SINGLE,
                2: Chem.BondType.DOUBLE,
                3: Chem.BondType.TRIPLE,
                4: Chem.BondType.QUADRUPLE,
                5: Chem.BondType.QUINTUPLE,
                6: Chem.BondType.HEXTUPLE,
                1.5: Chem.BondType.ONEANDAHALF,
                2.5: Chem.BondType.TWOANDAHALF,
                3.5: Chem.BondType.THREEANDAHALF,
                4.5: Chem.BondType.FOURANDAHALF,
                5.5: Chem.BondType.FIVEANDAHALF,
                "AROMATIC": Chem.BondType.AROMATIC,
                "IONIC": Chem.BondType.IONIC,
                "HYDROGEN": Chem.BondType.HYDROGEN,
                "THREECENTER": Chem.BondType.THREECENTER,
                "DATIVEONE": Chem.BondType.DATIVEONE,
                "DATIVE": Chem.BondType.DATIVE,
                "DATIVEL": Chem.BondType.DATIVEL,
                "DATIVER": Chem.BondType.DATIVER,
                "OTHER": Chem.BondType.OTHER,
                "ZERO": Chem.BondType.ZERO}



def graph2mol(mol_graph:MolGraph, bond_orders=False, allow_charged_fragments=False,
              charge:int = 0, geos:Optional[List[Geometry]] = None,
              ) -> rdkit.Chem.rdchem.Mol:
    """
        Creates a RDKit mol object using the connectivity of the mol graph.
        Conformers can be added to the mol object from Geometries.
        Bond orders can be assigned automatically using the algorithm from
        DOI: 10.1002/bkcs.10334
        Yeonjoon Kim and Woo Youn Kim
        "Universal Structure Conversion Method for Organic Molecules:
        From Atomic Connectivity to Three-Dimensional Geometry"
        Bull. Korean Chem. Soc.
        2015, Vol. 36, 1769-1777
        :param mol_graph: Molecular graph to take the connectivity from
        :type mol_graph: MolGraph
        :param generate_bond_orders: should bond orders be guessed or default to SINGLE
        :type generate_bond_orders: bool
        :param allow_charged_fragments: If false radicals are formed and if True
                                    ions are preferred, defaults to False.
                                    bond_orders has to be set to true to be able to
                                    assign charges to fragments.
        :type allow_charged_fragments: bool, optional
        :param charge: charge of the whole molecule, defaults to 0, only possible if
                       allow_charged_fragments is True, because only rdkit allows only
                       atoms to be charged and the charge of the molecule is calculated
                       based on them.
        :type charge: int, optional
        :return: RDKit molecule
        :rtype: rdkit.Chem.rdchem.Mol
    """

    n_atoms = mol_graph.n_atoms
    AC = mol_graph.connectivity_matrix()
    atom_types_strings = [atom.atomic_nr for atom in mol_graph.atom_types]

    mol = Chem.RWMol()#mol)
    for atom_type in mol_graph.atom_types:
        mol.AddAtom(Chem.Atom(atom_type.symbol))
    for atom in mol.GetAtoms():
        atom.SetNoImplicit(True)

    if bond_orders is True:
    # convert AC matrix to bond order (BO) matrix
        BO_matrix, atomic_valence_electrons = \
            _AC2BO(AC, atom_types_strings, charge,
                   allow_charged_fragments=allow_charged_fragments, use_graph=True)
        BO_valences = list(BO_matrix.sum(axis=1))
    else:
        BO_matrix = AC

    for i in range(n_atoms):
        for j in range(i + 1, n_atoms):
            bo = BO_matrix[i, j]
            if (bo == 0):
                continue
            rdkit_bond_type = bondTypeDict.get(bo)#, Chem.BondType.SINGLE)
            mol.AddBond(i, j, rdkit_bond_type)

    if bond_orders is True:
        if allow_charged_fragments:
            mol = _set_atomic_charges(mol, atom_types_strings, atomic_valence_electrons,
            BO_valences, BO_matrix, charge)
        else:
            mol = _set_atomic_radicals(mol, atom_types_strings,
                                       atomic_valence_electrons, BO_valences)

    if geos is not None:
        for geo in geos:
            conf = Chem.Conformer(mol.GetNumAtoms())
            for i,(x,y,z) in enumerate(geo.coords):
                conf.SetAtomPosition(i,(x,y,z))
            mol.AddConformer(conf)
    mol = mol.GetMol()

    if Chem.GetFormalCharge(mol) != charge:
        raise RuntimeError("Error during creation of mol object, charge is wrong!")

    for atom in mol.GetAtoms():
        atom.SetNoImplicit(True)
    return mol



    # ToDo: _BO2mol returns an arbitrary resonance form. Let's make the rest
    #mols = rdchem.ResonanceMolSupplier(mol, Chem.UNCONSTRAINED_CATIONS, Chem.UNCONSTRAINED_ANIONS)
    #mols = [mol for mol in mols]


    # Check for stereocenters and chiral centers
    #if embed_chiral:
    #    for new_mol in new_mols:
    #        _chiral_stereo_check(new_mol)

    #return rd_mol

def _get_UA(maxValence_list, valence_list):
    UA = []
    DU = []
    for i, (maxValence, valence) in enumerate(zip(maxValence_list, valence_list)):
        if not maxValence - valence > 0:
            continue
        UA.append(i)
        DU.append(maxValence - valence)
    return UA, DU

def _get_BO(AC, UA, DU, valences, UA_pairs, use_graph=True):
    BO = AC.copy()
    DU_save = []

    while DU_save != DU:
        for i, j in UA_pairs:
            BO[i, j] += 1
            BO[j, i] += 1

        BO_valence = list(BO.sum(axis=1))
        DU_save = copy.copy(DU)
        UA, DU = _get_UA(valences, BO_valence)
        UA_pairs = _get_UA_pairs(UA, AC, use_graph=use_graph)[0]

    return BO

def _valences_not_too_large(BO, valences):
    """
    """
    number_of_bonds_list = BO.sum(axis=1)
    for valence, number_of_bonds in zip(valences, number_of_bonds_list):
        if number_of_bonds > valence:
            return False

    return True

def _charge_is_OK(BO, AC, charge, DU, atomic_valence_electrons, atoms, valences,
                 allow_charged_fragments=True):
    # total charge
    Q = 0

    # charge fragment list
    q_list = []

    if allow_charged_fragments:

        BO_valences = list(BO.sum(axis=1))
        for i, atom in enumerate(atoms):
            q = _get_atomic_charge(atom, atomic_valence_electrons[atom], BO_valences[i])
            Q += q
            if atom == 6:
                number_of_single_bonds_to_C = list(BO[i, :]).count(1)
                if number_of_single_bonds_to_C == 2 and BO_valences[i] == 2:
                    Q += 1
                    q = 2
                if number_of_single_bonds_to_C == 3 and Q + 1 < charge:
                    Q += 2
                    q = 1

            if q != 0:
                q_list.append(q)

    return (charge == Q)

def _BO_is_OK(BO, AC, charge, DU, atomic_valence_electrons, atoms, valences,
    allow_charged_fragments=True):
    """
    Sanity of bond-orders

    args:
        BO -
        AC -
        charge -
        DU -


    optional
        allow_charges_fragments -


    returns:
        boolean - true of molecule is OK, false if not
    """

    if not _valences_not_too_large(BO, valences):
        return False

    check_sum = (BO - AC).sum() == sum(DU)
    check_charge = _charge_is_OK(BO, AC, charge, DU, atomic_valence_electrons, atoms, valences,
                                allow_charged_fragments)

    if check_charge and check_sum:
        return True

    return False

def _get_atomic_charge(atom, atomic_valence_electrons, BO_valence):
    """
    """

    if atom == 1:
        charge = 1 - BO_valence
    elif atom == 5:
        charge = 3 - BO_valence
    elif atom == 15 and BO_valence == 5:
        charge = 0
    elif atom == 16 and BO_valence == 6:
        charge = 0
    else:
        charge = atomic_valence_electrons - 8 + BO_valence

    return charge

def _BO2mol(mol, BO_matrix, atoms, atomic_valence_electrons,
           mol_charge, allow_charged_fragments=True):
    """
    based on code written by Paolo Toscani

    From bond order, atoms, valence structure and total charge, generate an
    rdkit molecule.

    args:
        mol - rdkit molecule
        BO_matrix - bond order matrix of molecule
        atoms - list of integer atomic symbols
        atomic_valence_electrons -
        mol_charge - total charge of molecule

    optional:
        allow_charged_fragments - bool - allow charged fragments

    returns
        mol - updated rdkit molecule with bond connectivity

    """

    l = len(atoms)
    BO_valences = list(BO_matrix.sum(axis=1))

    rwMol = Chem.RWMol(mol)



    for i in range(l):
        for j in range(i + 1, l):
            bo = int(round(BO_matrix[i, j]))
            if (bo == 0):
                continue
            bt = bondTypeDict.get(bo)#), Chem.BondType.SINGLE)
            rwMol.AddBond(i, j, bt)

    mol = rwMol.GetMol()

    if allow_charged_fragments:
        mol = _set_atomic_charges(mol, atoms, atomic_valence_electrons,
            BO_valences, BO_matrix, mol_charge)
    else:
        mol = _set_atomic_radicals(mol, atoms, atomic_valence_electrons, BO_valences)

    return mol

def _set_atomic_charges(mol, atoms, atomic_valence_electrons,
                       BO_valences, BO_matrix, mol_charge):
    """
    """
    q = 0
    for i, atom in enumerate(atoms):
        a = mol.GetAtomWithIdx(i)
        charge = _get_atomic_charge(atom, atomic_valence_electrons[atom], BO_valences[i])
        q += charge
        if atom == 6:
            number_of_single_bonds_to_C = list(BO_matrix[i, :]).count(1)
            if number_of_single_bonds_to_C == 2 and BO_valences[i] == 2:
                q += 1
                charge = 0
            if number_of_single_bonds_to_C == 3 and q + 1 < mol_charge:
                q += 2
                charge = 1

        if (abs(charge) > 0):
            a.SetFormalCharge(int(charge))

    #mol = clean_charges(mol)

    return mol

def _set_atomic_radicals(mol, atoms, atomic_valence_electrons, BO_valences):
    """

    The number of radical electrons = absolute atomic charge

    """
    for i, atom in enumerate(atoms):
        a = mol.GetAtomWithIdx(i)
        charge = _get_atomic_charge(
            atom,
            atomic_valence_electrons[atom],
            BO_valences[i])

        if (abs(charge) > 0):
            a.SetNumRadicalElectrons(abs(int(charge)))

    return mol

def _get_bonds(UA, AC):
    """

    """
    bonds = []

    for k, i in enumerate(UA):
        for j in UA[k + 1:]:
            if AC[i, j] == 1:
                bonds.append(tuple(sorted([i, j])))

    return bonds

def _get_UA_pairs(UA, AC, use_graph=True):
    """

    """

    bonds = _get_bonds(UA, AC)

    if len(bonds) == 0:
        return [()]

    if use_graph:
        G = nx.Graph()
        G.add_edges_from(bonds)
        UA_pairs = [list(nx.max_weight_matching(G))]
        return UA_pairs

    max_atoms_in_combo = 0
    UA_pairs = [()]
    for combo in list(itertools.combinations(bonds, int(len(UA) / 2))):
        flat_list = [item for sublist in combo for item in sublist]
        atoms_in_combo = len(set(flat_list))
        if atoms_in_combo > max_atoms_in_combo:
            max_atoms_in_combo = atoms_in_combo
            UA_pairs = [combo]

        elif atoms_in_combo == max_atoms_in_combo:
            UA_pairs.append(combo)

    return UA_pairs

def _AC2BO(AC, atoms, charge, allow_charged_fragments=True, use_graph=True):
    """

    implemenation of algorithm shown in Figure 2

    UA: unsaturated atoms

    DU: degree of unsaturation (u matrix in Figure)

    best_BO: Bcurr in Figure

    """

    global atomic_valence
    global atomic_valence_electrons

    # make a list of valences, e.g. for CO: [[4],[2,1]]
    valences_list_of_lists = []
    AC_valence = list(AC.sum(axis=1))

    for i,(atomicNum,valence) in enumerate(zip(atoms,AC_valence)):
        # valence can't be smaller than number of neighbourgs
        possible_valence = [x for x in atomic_valence[atomicNum] if x >= valence]
        if not possible_valence:
            warnings.warn(f'Valence of atom {i},is {valence}, which bigger than allowed max {max(atomic_valence[atomicNum])}. Continuing')
            #sys.exit()
        valences_list_of_lists.append(possible_valence)

    # convert [[4],[2,1]] to [[4,2],[4,1]]
    valences_list = itertools.product(*valences_list_of_lists)

    best_BO = AC.copy()

    for valences in valences_list:

        UA, DU_from_AC = _get_UA(valences, AC_valence)

        check_len = (len(UA) == 0)
        if check_len:
            check_bo = _BO_is_OK(AC, AC, charge, DU_from_AC,
                atomic_valence_electrons, atoms, valences,
                allow_charged_fragments=allow_charged_fragments)
        else:
            check_bo = None

        if check_len and check_bo:
            return AC, atomic_valence_electrons

        UA_pairs_list = _get_UA_pairs(UA, AC, use_graph=use_graph)
        for UA_pairs in UA_pairs_list:
            BO = _get_BO(AC, UA, DU_from_AC, valences, UA_pairs, use_graph=use_graph)
            status = _BO_is_OK(BO, AC, charge, DU_from_AC,
                        atomic_valence_electrons, atoms, valences,
                        allow_charged_fragments=allow_charged_fragments)
            charge_OK = _charge_is_OK(BO, AC, charge, DU_from_AC, atomic_valence_electrons, atoms, valences,
                                     allow_charged_fragments=allow_charged_fragments)

            if status:
                return BO, atomic_valence_electrons
            elif BO.sum() >= best_BO.sum() and _valences_not_too_large(BO, valences) and charge_OK:
                best_BO = BO.copy()

    return best_BO, atomic_valence_electrons

def _AC2mol(mol, AC, atoms, charge, allow_charged_fragments=True,
           use_graph=True):

    # convert AC matrix to bond order (BO) matrix
    BO, atomic_valence_electrons = _AC2BO(
        AC,
        atoms,
        charge,
        allow_charged_fragments=allow_charged_fragments,
        use_graph=use_graph)

    # add BO connectivity and charge info to mol object
    mol = _BO2mol(
        mol,
        BO,
        atoms,
        atomic_valence_electrons,
        charge,
        allow_charged_fragments=allow_charged_fragments)

    # If charge is not correct don't return mol
    if Chem.GetFormalCharge(mol) != charge:
        return []
    return mol
    # ToDo: _BO2mol returns an arbitrary resonance form. Let's make the rest
    #mols = rdchem.ResonanceMolSupplier(mol, Chem.UNCONSTRAINED_CATIONS, Chem.UNCONSTRAINED_ANIONS)
    #mols = [mol for mol in mols]

def _get_proto_mol(atom_types: List[Element]):
    pass
    #mol = Chem.MolFromSmarts("[#" + str(atom_types[0].symbol) + "]")
    #rwMol = Chem.RWMol()#mol)
    #for i in range(len(atom_types)):
    #    a = Chem.Atom(atom_types[i].symbol)
    #    rwMol.AddAtom(a)#

    #mol = rwMol.GetMol()

    #return mol

def _chiral_stereo_check(mol):
    """
    Find and embed chiral information into the model based on the coordinates

    args:
        mol - rdkit molecule, with embeded conformer

    """
    Chem.SanitizeMol(mol)
    Chem.DetectBondStereochemistry(mol, -1)
    Chem.AssignStereochemistry(mol, flagPossibleStereoCenters=True, force=True)
    Chem.AssignAtomChiralTagsFromStructure(mol, -1)

    return


#MIT License

#Copyright (c) 2018 Jensen Group

#Permission is hereby granted, free of charge, to any person obtaining a copy
#of this software and associated documentation files (the "Software"), to deal
#in the Software without restriction, including without limitation the rights
#to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#copies of the Software, and to permit persons to whom the Software is
#furnished to do so, subject to the following conditions:

#The above copyright notice and this permission notice shall be included in all
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#SOFTWARE.
