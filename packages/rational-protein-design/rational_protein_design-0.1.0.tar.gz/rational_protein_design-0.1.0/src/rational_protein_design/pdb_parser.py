import os
from Bio.PDB import PDBParser

class PDBParserWrapper:
    def __init__(self, pdb_file):
        self.parser = PDBParser(QUIET=True, PERMISSIVE=False)
        self.structure, self.pdb_id = self.parse_pdb_file(pdb_file)

    def parse_pdb_file(self, pdb_file):
        structure = self.parser.get_structure('structure', pdb_file)
        pdb_filename = os.path.basename(pdb_file)
        pdb_id = os.path.splitext(pdb_filename)[0]
        return structure, pdb_id

    def get_chain(self, chain_id):
        return self.structure[0][chain_id]

    def get_target_residues(self, chain, start_residue, end_residue):
        return [residue for residue in chain if start_residue <= residue.get_id()[1] <= end_residue]
