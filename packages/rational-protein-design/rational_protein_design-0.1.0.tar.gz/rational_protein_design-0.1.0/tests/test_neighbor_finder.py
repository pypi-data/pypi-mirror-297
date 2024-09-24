# tests/test_neighbor_finder.py

import unittest
from Bio.PDB import Atom, Residue, Chain, Model, Structure
from rational_protein_design.neighbor_finder import NeighborFinder

class TestNeighborFinder(unittest.TestCase):
    
    def setUp(self):
        # Set up a mock structure for testing
        self.structure = Structure.Structure("mock_structure")
        self.model = Model.Model(0)
        self.structure.add(self.model)
        self.chain = Chain.Chain("A")
        self.model.add(self.chain)
        
        # Create mock residues and atoms
        self.residue1 = Residue.Residue((' ', 1, ' '), 'ALA', ' ')
        self.atom1 = Atom.Atom('CA', [0.0, 0.0, 0.0], 1.0, 1.0, ' ', 'CA', 1)
        self.residue1.add(self.atom1)
        
        self.residue2 = Residue.Residue((' ', 2, ' '), 'GLY', ' ')
        self.atom2 = Atom.Atom('CA', [1.0, 1.0, 1.0], 1.0, 1.0, ' ', 'CA', 2)
        self.residue2.add(self.atom2)
        
        self.chain.add(self.residue1)
        self.chain.add(self.residue2)
        
    def test_find_neighbor_residues(self):
        # Find neighbor residues within a distance threshold
        target_atoms = [self.atom1]
        neighbor_residues = NeighborFinder.find_neighbor_residues(target_atoms, self.chain, distance_threshold=2.0)

        # Corrected assertion based on calculated distances
        self.assertEqual(len(neighbor_residues), 2)
        self.assertIn(self.residue1, neighbor_residues)
        self.assertIn(self.residue2, neighbor_residues)

    def test_no_neighbors_within_distance(self):
        # Set distance threshold too low to find neighbors
        target_atoms = [self.atom1]
        neighbor_residues = NeighborFinder.find_neighbor_residues(target_atoms, self.chain, distance_threshold=0.5)

        # Only the residue containing atom1 should be found
        self.assertEqual(len(neighbor_residues), 1)
        self.assertIn(self.residue1, neighbor_residues)

if __name__ == '__main__':
    unittest.main()
