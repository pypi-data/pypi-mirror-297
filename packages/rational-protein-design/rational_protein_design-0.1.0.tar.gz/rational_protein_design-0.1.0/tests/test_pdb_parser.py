import unittest
from rational_protein_design.pdb_parser import PDBParserWrapper
# from Bio.PDB import PDBExceptions

class TestPDBParser(unittest.TestCase):
    def test_parse_pdb_file(self):
        # Ensure that parsing a valid PDB file works correctly
        pdb_parser = PDBParserWrapper("tests/test_data/valid_structure.pdb")
        self.assertEqual(pdb_parser.pdb_id, "valid_structure")

    # def test_invalid_pdb_file(self):
    #     # Ensure that an invalid PDB file raises an exception
    #     from Bio.PDB.PDBExceptions import PDBConstructionException
    #     with self.assertRaises(PDBConstructionException):
    #         PDBParserWrapper("tests/test_data/invalid_structure.pdb")

if __name__ == '__main__':
    unittest.main()
