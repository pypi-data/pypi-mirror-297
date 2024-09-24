# tests/test_binder_designer.py

import unittest
from rational_protein_design.binder_designer import BinderDesigner
from unittest.mock import patch, MagicMock

class TestBinderDesigner(unittest.TestCase):
    
    @patch('rational_protein_design.binder_designer.PDBParserWrapper')
    def test_design_binder(self, mock_parser_wrapper):
        # Mock the PDBParserWrapper and its methods
        mock_parser = MagicMock()
        mock_parser.get_chain.return_value = MagicMock()
        mock_parser.get_target_residues.return_value = []
        mock_parser.pdb_id = "mock_pdb"
        mock_parser_wrapper.return_value = mock_parser

        # Create an instance of BinderDesigner
        designer = BinderDesigner(
            pdb_file="mock_pdb_file.pdb",
            chain_id="D",
            target_residues_range=(166, 183),
            neighbor_chain_id="I",
            N=80,
            num_seq=10
        )
        
        # Mock the extract_proximal_sequence method
        designer.extract_proximal_sequence = MagicMock(return_value=None)

        # Since extract_proximal_sequence returns None, no sequences will be written
        output_fasta = "tests/test_data/temp_output.fasta"
        designer.design_binder(output_fasta)
        
        # Check that the method was called the expected number of times
        self.assertEqual(designer.extract_proximal_sequence.call_count, designer.max_attempts)

if __name__ == '__main__':
    unittest.main()
