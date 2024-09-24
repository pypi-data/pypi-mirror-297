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
        ranges = []
        start = residue_ids[0]
        prev = residue_ids[0]
        for residue_id in residue_ids[1:]:
            if residue_id[1] == prev[1] + 1 and residue_id[2] == ' ':
                prev = residue_id
            else:
                ranges.append((start, prev))
                start = residue_id
                prev = residue_id
        ranges.append((start, prev))
        return ranges
