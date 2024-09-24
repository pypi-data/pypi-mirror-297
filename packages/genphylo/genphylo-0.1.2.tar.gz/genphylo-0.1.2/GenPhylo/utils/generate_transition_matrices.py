from GenPhylo.model.mathmodel import *
import numpy as np

def DLC(matrix):
    B = True
    for j in range(matrix.shape[1]):
        max_index = np.argmax(matrix[:, j])
        if max_index != j:
            B = False
    return B

def compare_equal_matrices(matrix1, matrix2):
    """
    Compares two matrices element-wise.
    """
    for i in range(matrix1.shape[0]):
        for j in range(matrix1.shape[1]):
            if matrix1[i, j] != matrix2[i, j]:
                return False
    return True

def generate_transition_matrices(tree, node_distribution):
    """
    Generates transition matrices for each edge in the phylogenetic tree.
    """
    edges = []
    for edge in tree.edges():
        l = 4 * edge[1].branch_length  # (Lake'94)
        matrix = np.zeros((4,4))
        while compare_equal_matrices(matrix, np.zeros((4,4))):
            matrix = generate_random_matrix(node_distribution[edge[0].name], l)
        assert (np.sum(matrix) > 0)
        iter = 0 # threshold on the number of iterations for DLC matrices 
        while not DLC(matrix) and iter < 5:
            iter += 1
            #print("Checking DLC")
            matrix = generate_random_matrix(node_distribution[edge[0].name], l)
        if iter == 5:
            print("Warning: Could not generate a DLC matrix for edge: ", edge)
        new_edge = Edge(edge, matrix)
        edges.append(new_edge)
        node_distribution[edge[1].name] = np.matmul(node_distribution[edge[0].name], new_edge.transition_matrix)
        for i in range(4):
            assert (np.sum(new_edge.transition_matrix[i, :]) < 1.000000001 and np.sum(
                new_edge.transition_matrix[i, :]) > 0.999999999)
    return edges