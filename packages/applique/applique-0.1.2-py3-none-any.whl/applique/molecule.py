from typing import List
import rdkit
from rdkit.Chem import AllChem


class Molecule:
    """
    Simple molecule class that extends RDKit molecules
    """

    def from_canonical_smiles(self, can_smiles: str) -> None:
        raise NotImplementedError

    def from_mol(self, file_path: str) -> None:
        self.rdmol = rdkit.Chem.rdmolfiles.MolFromMolFile(file_path)
        return self

    def embed(self, rdmol=None):
        """make emebedding in RDKit

        Args:
            rdmol (_type_, optional): rdmol object. Defaults to None.

        Returns:
            _type_: Mol Object
        """
        mol = self._check_mol(rdmol=rdmol)
        mol = rdkit.Chem.rdmolops.AddHs(mol)
        assert type(mol) != None
        AllChem.EmbedMolecule(mol)
        AllChem.MMFFOptimizeMolecule(mol)
        self.rdmol = mol
        return mol

    def struct2D(self, rdmol=None) -> List[float]:
        """Gets 2D coordinates

        Args:
            rdmol (_type_, optional): RDMol object

        Returns:
            List[float]: Coordinates 3D but only in 2D
        """
        mol = self.embed(rdmol=rdmol)

        rdkit.Chem.rdDepictor.Compute2DCoords(mol)
        coordinates = []

        for i in range(len(mol.GetAtoms())):
            pos = mol.GetConformer().GetAtomPosition(i)
            coordinates.append(list(pos))
        self.coordinates2D = coordinates

        return coordinates

    def struct3D(self, rdmol=None) -> List[List[float]]:
        """Gets 2D coordinates

        Args:
            rdmol (_type_, optional): RDMol object

        Returns:
            List[float]: Coordinates 3D but only in 2D
        """

        mol = self.embed(rdmol=rdmol)
        coordinates = []

        for i in range(len(mol.GetAtoms())):
            pos = mol.GetConformer().GetAtomPosition(i)
            coordinates.append(list(pos))
        self.coordinates3D = coordinates

        return coordinates

    def _check_mol(self, rdmol):
        """
        Reused snipptet to either use the stored rdmol or a new one
        """

        if rdmol is None:
            mol = self.rdmol
        else:
            mol = rdmol
        return mol
