import numpy as np

def generate_sequences(M, seq):
    """
    Given the sequence seq of the ancestor node and the transition matrix M,
    returns the sequence of the descendant node
    """
    nucleotide_map = {'A': 0, 'G': 1, 'C': 2, 'T': 3}
    row_indices = np.array([nucleotide_map[s] for s in seq])
    new_seq = ''.join(np.random.choice(['A', 'G', 'C', 'T'], p=M[row_indices[i], :]) for i in range(len(seq)))
    return new_seq
