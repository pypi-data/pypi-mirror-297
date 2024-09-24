from Bio.SeqUtils import seq1
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import random

class SequenceExtractor:
    @staticmethod
    def create_sequence_record(neighbor_chain, sequence_residues, pdb_id, neighbor_chain_id):
        sequence = ''.join([seq1(residue.get_resname()) for residue in sequence_residues])
        residue_ids = [residue.get_id() for residue in sequence_residues]

        min_residue_id = residue_ids[0]
        max_residue_id = residue_ids[-1]

        min_resseq, min_icode = min_residue_id[1], min_residue_id[2].strip()
        max_resseq, max_icode = max_residue_id[1], max_residue_id[2].strip()

        min_icode = min_icode if min_icode else ''
        max_icode = max_icode if max_icode else ''

        seq_id = f"{pdb_id}_chain{neighbor_chain_id}_resseq_{min_resseq}{min_icode}-{max_resseq}{max_icode}"
        return SeqRecord(Seq(sequence), id=seq_id, description="")

    @staticmethod
    def adjust_sequence_length(sequence_residues, neighbor_chain, N):
        if len(sequence_residues) == N:
            return sequence_residues
        elif len(sequence_residues) > N:
            excess = len(sequence_residues) - N
            start = random.randint(0, excess)
            return sequence_residues[start:start + N]

        extended_sequence = SequenceExtractor.extend_sequence(sequence_residues, neighbor_chain, N)
        return extended_sequence if extended_sequence else None

    @staticmethod
    def extend_sequence(sequence_residues, neighbor_chain, N):
        residues_needed = N - len(sequence_residues)
        residue_ids = [residue.get_id() for residue in sequence_residues]
        min_residue_id = min(residue_ids)
        max_residue_id = max(residue_ids)

        left_residues = [residue for residue in neighbor_chain if residue.get_id() < min_residue_id]
        right_residues = [residue for residue in neighbor_chain if residue.get_id() > max_residue_id]

        left_residues.sort(key=lambda r: r.get_id(), reverse=True)
        right_residues.sort(key=lambda r: r.get_id())

        added_residues = []

        while residues_needed > 0 and (left_residues or right_residues):
            if left_residues and right_residues:
                side = random.choice(['left', 'right'])
            elif left_residues:
                side = 'left'
            elif right_residues:
                side = 'right'

            if side == 'left' and left_residues:
                added_residues.insert(0, left_residues.pop(0))
                residues_needed -= 1
            elif side == 'right' and right_residues:
                added_residues.append(right_residues.pop(0))
                residues_needed -= 1

        final_sequence = added_residues + sequence_residues
        return final_sequence if len(final_sequence) == N else None
