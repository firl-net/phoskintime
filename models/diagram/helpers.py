from graphviz import Digraph
from itertools import combinations
from config.constants import OUT_DIR


def powerset(iterable):
    """
    Return the list of all subsets (as frozensets) of the given iterable.

    Args:
        iterable: An iterable (e.g., list, set) to generate subsets from.
    Returns:
        A list of frozensets representing all subsets of the input iterable.
    """
    s = list(iterable)
    all_subsets = []
    for r in range(len(s) + 1):
        for combo in combinations(s, r):
            all_subsets.append(frozenset(combo))
    return all_subsets


def state_label(state):
    """
    Convert a set of phosphorylation sites into a node label.

    Args:
        state: A frozenset representing the phosphorylation state.
    Returns:
        A string representing the label for the node.
    """
    if not state:
        return "P"
    sorted_sites = sorted(state, key=lambda x: int(x))
    return "P" + ''.join(sorted_sites)


def create_random_diagram(x, num_sites, output_filename):
    """
    Create a random phosphorylation diagram.

    Args:
        x: Placeholder parameter, not used in this function.
        num_sites: The number of phosphorylation sites.
        output_filename: The name of the output file for the diagram.

    """
    dot = Digraph(engine='neato')
    dot.attr(rankdir='LR')
    total_states = 2 ** num_sites + 2
    width = max(8, total_states * 0.4)
    height = max(4, total_states * 0.15)
    nodesep = min(0.5 + 0.05 * num_sites, 1.5)
    ranksep = min(0.6 + 0.05 * num_sites, 1.5)
    dot.attr(size=f"{width},{height}!", nodesep=str(nodesep), ranksep=str(ranksep))
    # Global graph attributes: title and overall styling.
    dot.attr(label="Random", labelloc="t", fontsize="15",
             fontname="Helvetica", fontcolor="black")
    dot.attr('graph', bgcolor="white", dpi='300')

    # Global node and edge attributes for a modern, clean look.
    dot.attr('node', shape='ellipse', style='filled,rounded', fontname='Helvetica',
             fontsize='12', fixedsize='false')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # --- mRNA (R) Production and Degradation ---
    dot.node('NULL_R', 'φ', shape='plaintext', fontcolor='gray')
    dot.node('R', 'R', style='filled', fillcolor='lightcoral', fontcolor='white')
    dot.edge('NULL_R', 'R', label='A', color='red', fontcolor='red', penwidth='2')
    dot.edge('R', 'NULL_R', label='B', color='forestgreen', fontcolor='forestgreen', penwidth='2')

    # --- Protein (P) and its phosphorylation states ---
    dot.node('NULL_P', 'φ', shape='plaintext', fontcolor='gray')
    sites = [str(i) for i in range(1, num_sites + 1)]
    all_states = powerset(sites)

    # Create nodes for each phosphorylation state with custom colors.
    state_nodes = {}
    for state in all_states:
        label = state_label(state)
        state_nodes[state] = label
        if label == "P":
            dot.node(label, label, fillcolor='dodgerblue', fontcolor='white')
        else:
            dot.node(label, label, fillcolor='turquoise3', fontcolor='black')
        # Create corresponding NULL node for degradation of this state.
        dot.node('NULL_' + label, 'φ', shape='plaintext', fontcolor='gray')

    # --- Production of protein P ---
    dot.edge('R', state_nodes[frozenset()], label='C', color='goldenrod', fontcolor='goldenrod', penwidth='2')

    # --- Phosphorylation transitions (Addition) ---
    all_sites_set = set(sites)
    for state in all_states:
        current_label = state_nodes[state]
        missing_sites = all_sites_set - state
        for site in missing_sites:
            new_state = state.union({site})
            new_label = state_nodes[new_state]
            dot.edge(current_label, new_label, label='S' + site, color='mediumvioletred',
                     fontcolor='mediumvioletred', style='bold', penwidth='1.5')

    # --- Dephosphorylation transitions (Removal) ---
    for state in all_states:
        if state:  # Only states with at least one phosphorylation can dephosphorylate.
            current_label = state_nodes[state]
            for site in state:
                new_state = state.difference({site})
                new_label = state_nodes[new_state]
                dot.edge(current_label, new_label, label='1', color='slateblue',
                         fontcolor='slateblue', style='dashed', penwidth='1.5')

    # --- Degradation transitions for all protein states ---
    for state in all_states:
        label = state_nodes[state]
        deg_label = 'D' if label == "P" else 'D' + label[1:]
        dot.edge(label, 'NULL_' + label, label=deg_label, color='dimgray',
                 fontcolor='dimgray', style='dotted', penwidth='1.5')

    dot.render(f"{OUT_DIR}/{output_filename}", format='png', cleanup=True)


def create_distributive_diagram(x, num_sites, output_filename):
    """
    Create a distributive phosphorylation diagram.

    Args:
        x: Placeholder parameter, not used in this function.
        num_sites: The number of phosphorylation sites.
        output_filename: The name of the output file for the diagram.

    """
    dot = Digraph(engine='neato')
    dot.attr(rankdir='LR')
    dot.attr(label="Distributive", labelloc="t", fontsize="15",
             fontname="Helvetica", fontcolor="black")
    dot.attr('graph', bgcolor="white", dpi='300')
    dot.attr('node', shape='ellipse', style='filled,rounded', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # --- mRNA (R) and its null state ---
    dot.node('NULL_R', 'φ', shape='plaintext', fontcolor='gray')
    dot.node('R', 'R', style='filled', fillcolor='lightcoral', fontcolor='white')
    dot.edge('NULL_R', 'R', label='A', color='red', fontcolor='red', penwidth='2')
    dot.edge('R', 'NULL_R', label='B', color='forestgreen', fontcolor='forestgreen', penwidth='2')

    # --- Protein (P) and its null state ---
    dot.node('NULL_P', 'φ', shape='plaintext', fontcolor='gray')
    dot.node('P', 'P', style='filled', fillcolor='dodgerblue', fontcolor='white')
    dot.edge('R', 'P', label='C', color='goldenrod', fontcolor='goldenrod', penwidth='2')
    dot.edge('P', 'NULL_P', label='D', color='dimgray', fontcolor='dimgray', penwidth='2')

    # --- Phosphorylation sites ---
    for i in range(1, num_sites + 1):
        p_node = f'P{i}'
        null_p_node = f'NULL_P{i}'
        dot.node(p_node, p_node, style='filled', fillcolor='turquoise3', fontcolor='black')
        dot.node(null_p_node, 'φ', shape='plaintext', fontcolor='gray')
        dot.edge('P', p_node, label=f'S{i}', color='mediumvioletred', fontcolor='mediumvioletred',
                 style='bold', penwidth='1.5')
        dot.edge(p_node, 'P', label='1', color='slateblue', fontcolor='slateblue',
                 style='dashed', penwidth='1.5')
        dot.edge(p_node, null_p_node, label=f'D{i}', color='dimgray', fontcolor='dimgray',
                 style='dotted', penwidth='1.5')

    dot.render(f"{OUT_DIR}/{output_filename}", format='png', cleanup=True)


def create_successive_model(x, num_sites, output_filename):
    """
    Create a successive phosphorylation diagram.

    Args:
        x: Placeholder parameter, not used in this function.
        num_sites: The number of phosphorylation sites.
        output_filename: The name of the output file for the diagram.
    """
    dot = Digraph(engine='neato')
    dot.attr(rankdir='LR')
    dot.attr(label="Successive", labelloc="t", fontsize="15",
             fontname='Helvetica', fontcolor='black')
    dot.attr('graph', bgcolor="white", dpi='300')
    dot.attr('node', shape='ellipse', style='filled,rounded', fontname='Helvetica', fontsize='12')
    dot.attr('edge', fontname='Helvetica', fontsize='10')

    # --- mRNA (R) Production and Degradation ---
    dot.node('NULL_R', 'φ', shape='plaintext', fontcolor='gray')
    dot.node('R', 'R', style='filled', fillcolor='lightcoral', fontcolor='white')
    dot.edge('NULL_R', 'R', label='A', color='red', fontcolor='red', penwidth='2')
    dot.edge('R', 'NULL_R', label='B', color='forestgreen', fontcolor='forestgreen', penwidth='2')

    # --- Protein (P) and its null state ---
    dot.node('NULL_P', 'φ', shape='plaintext', fontcolor='gray')
    dot.node('P', 'P', style='filled', fillcolor='dodgerblue', fontcolor='white')
    dot.edge('R', 'P', label='C', color='goldenrod', fontcolor='goldenrod', penwidth='2')
    dot.edge('P', 'NULL_P', label='D', color='dimgray', fontcolor='dimgray', penwidth='2')

    # --- Successive Phosphorylation States ---
    for i in range(1, num_sites + 1):
        state = f'P{i}'
        null_state = f'NULL_P{i}'
        dot.node(state, state, style='filled', fillcolor='turquoise3', fontcolor='black')
        dot.node(null_state, 'φ', shape='plaintext', fontcolor='gray')
    # First phosphorylation: P -> P1
    if num_sites >= 1:
        dot.edge('P', 'P1', label='S1', color='mediumvioletred', fontcolor='mediumvioletred',
                 style='bold', penwidth='1.5')
    # Subsequent phosphorylations: P{i-1} -> P{i}
    for i in range(2, num_sites + 1):
        dot.edge(f'P{i - 1}', f'P{i}', label=f'S{i}', color='mediumvioletred', fontcolor='mediumvioletred',
                 style='bold', penwidth='1.5')
    # Dephosphorylation (reverse reactions)
    if num_sites >= 1:
        dot.edge('P1', 'P', label='1', color='slateblue', fontcolor='slateblue', style='dashed', penwidth='1.5')
    for i in range(2, num_sites + 1):
        dot.edge(f'P{i}', f'P{i - 1}', label='1', color='slateblue', fontcolor='slateblue',
                 style='dashed', penwidth='1.5')
    # Degradation for phosphorylated states
    for i in range(1, num_sites + 1):
        dot.edge(f'P{i}', f'NULL_P{i}', label=f'D{i}', color='dimgray', fontcolor='dimgray',
                 style='dotted', penwidth='1.5')

    dot.render(f"{OUT_DIR}/{output_filename}", format='png', cleanup=True)
