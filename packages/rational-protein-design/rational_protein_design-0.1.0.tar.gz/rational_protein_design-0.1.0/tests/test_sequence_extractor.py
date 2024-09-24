# tests/test_sequence_extractor.py

import unittest
from rational_protein_design.sequence_extractor import SequenceExtractor
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
from Bio.PDB import Residue

class TestSequenceExtractor(unittest.TestCase):
    def test_create_sequence_record(self):
        # Create mock Residue objects
        residue1 = Residue.Residue((' ', 1, ' '), 'MET', ' ')
        residue2 = Residue.Residue((' ', 2, ' '), 'ALA', ' ')
        sequence_residues = [residue1, residue2]
        pdb_id = "mock_pdb"
        neighbor_chain_id = "B"

        # Generate the sequence record
        record = SequenceExtractor.create_sequence_record(sequence_residues, pdb_id, neighbor_chain_id)

        # Verify that the sequence is correct
        self.assertEqual(str(record.seq), "MA")  # Corrected sequence
        self.assertEqual(record.id, "mock_pdb_chainB_resseq_1-2")  # Corrected ID format

if __name__ == '__main__':
    unittest.main()
