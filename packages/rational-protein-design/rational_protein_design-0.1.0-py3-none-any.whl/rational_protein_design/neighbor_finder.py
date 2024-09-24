# src/rational_protein_design/neighbor_finder.py

from Bio.PDB import NeighborSearch, Selection

class NeighborFinder:
    @staticmethod
    def find_neighbor_residues(target_atoms, neighbor_chain, distance_threshold):
        ns = NeighborSearch(list(neighbor_chain.get_atoms()))
        neighbor_residues = set()
        for atom in target_atoms:
            neighbors = ns.search(atom.get_coord(), distance_threshold, level='R')
            neighbor_residues.update(neighbors)
        return neighbor_residues

    @staticmethod
    def get_contiguous_residue_ids(residue_ids):
        residue_ids = sorted(residue_ids, key=lambda x: (x[1], x[2]))
        ranges = []
        start = prev = residue_ids[0]
        for residue_id in residue_ids[1:]:
            # Check for contiguous residues considering insertion codes
            if residue_id[1] == prev[1] + 1 and residue_id[2] == prev[2]:
                prev = residue_id
            else:
                ranges.append((start, prev))
                start = prev = residue_id
        ranges.append((start, prev))
        return ranges
