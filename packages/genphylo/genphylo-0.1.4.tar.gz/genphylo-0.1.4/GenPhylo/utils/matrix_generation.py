import os
import tarfile
import json
import networkx as nx
from Bio import Phylo
from GenPhylo.model.mathmodel import *
from GenPhylo.utils.generate_root_distribution import generate_root_distribution
from GenPhylo.utils.rename_nodes import rename_nodes
from GenPhylo.utils.generate_transition_matrices import generate_transition_matrices
from GenPhylo.utils.save_transition_matrices import save_transition_matrices
from GenPhylo.utils.generate_alignments import generate_alignments

def matrix_generation(tree, length, t, lengths, case, root_distr, name):
    """
    Main function to generate transition matrices and alignments.
    """
    if root_distr == "random":
        node_distribution = {"Root": generate_root_distribution()}
    else:
        # Parse a given string separating numbers given by commas and puting them in a 1x4 vector
        node_distribution = np.array(json.loads(root_distr))
        # Check this vector sums up to 1
        assert sum(node_distribution) == 1, "Root distribution does not sum up to 1"
        node_distribution = {"Root": node_distribution}
    path_t = tree
    tree_file = open(path_t, "r")
    tree = tree_file.read()
    tree = Phylo.read(StringIO(tree), "newick")
    rename_nodes(tree)
    # Write the tree in our format to latter save it at the top of the matrix file
    newick_with_labels = StringIO()
    Phylo.write(tree, newick_with_labels, "newick", format_branch_length='%0.2f')
    newick_with_labels_str = newick_with_labels.getvalue()
    net = Phylo.to_networkx(tree)
    edges = generate_transition_matrices(net, node_distribution)
    save_transition_matrices(edges, name, newick_with_labels_str)
    return generate_alignments(net, node_distribution, edges, length, t, case, lengths, name)