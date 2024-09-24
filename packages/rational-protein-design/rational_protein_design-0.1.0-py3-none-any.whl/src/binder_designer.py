import random
from Bio import SeqIO
from .pdb_parser import PDBParserWrapper
from .neighbor_finder import NeighborFinder
from .sequence_extractor import SequenceExtractor

class BinderDesigner:
    def __init__(self, pdb_file, chain_id, target_residues_range, neighbor_chain_id, N, num_seq, max_distance=20.0, increment=0.5, max_attempts=None):
        self.pdb_file = pdb_file
        self.chain_id = chain_id
        self.target_residues_range = target_residues_range
        self.neighbor_chain_id = neighbor_chain_id
        self.N = N
        self.num_seq = num_seq
        self.max_distance = max_distance
        self.increment = increment
        self.max_attempts = max_attempts if max_attempts else 10 * num_seq

    def extract_proximal_sequence(self):
        parser = PDBParserWrapper(self.pdb_file)
        target_chain = parser.get_chain(self.chain_id)
        neighbor_chain = parser.get_chain(self.neighbor_chain_id)

        target_residues = parser.get_target_residues(target_chain, *self.target_residues_range)
        target_atoms = Selection.unfold_entities(target_residues, 'A')

        distance_threshold = random.uniform(1.0, self.max_distance / 2)
        neighbor_resids_list = []

        while distance_threshold <= self.max_distance:
            neighbor_residues = NeighborFinder.find_neighbor_residues(target_atoms, neighbor_chain, distance_threshold)
            neighbor_residues -= set(target_residues)
            neighbor_resids = sorted(set(residue.get_id() for residue in neighbor_residues))

            if neighbor_resids:
                resseq_ranges = NeighborFinder.get_contiguous_residue_ids(neighbor_resids)
                neighbor_resids_list.extend(resseq_ranges)

            distance_threshold += self.increment

        if neighbor_resids_list:
            selected_range = random.choice(neighbor_resids_list)
            min_residue_id, max_residue_id = selected_range
            sequence_residues = [residue for residue in neighbor_chain if min_residue_id <= residue.get_id() <= max_residue_id]

            sequence_residues = SequenceExtractor.adjust_sequence_length(sequence_residues, neighbor_chain, self.N)
            if sequence_residues:
                return SequenceExtractor.create_sequence_record(neighbor_chain, sequence_residues, parser.pdb_id, self.neighbor_chain_id)
        return None

    def design_binder(self, output_fasta):
        seq_records = []
        unique_sequences = set()
        attempts = 0

        while len(seq_records) < self.num_seq and attempts < self.max_attempts:
            seq_record = self.extract_proximal_sequence()
            attempts += 1
            if seq_record:
                sequence_str = str(seq_record.seq)
                if sequence_str not in unique_sequences:
                    unique_sequences.add(sequence_str)
                    seq_records.append(seq_record)

        SeqIO.write(seq_records, output_fasta, 'fasta')
        print(f"{len(seq_records)} unique sequences saved to {output_fasta}")
