def rename_nodes(tree):
    """
    Renames the nodes and leaves of the phylogenetic tree.
    """
    for idx, clade in enumerate(tree.get_nonterminals()):
        clade.name = "Node_" + str(idx) if idx > 0 else "Root"
    for idx, clade in enumerate(tree.get_terminals()):
        clade.name = "Leaf_" + clade.name