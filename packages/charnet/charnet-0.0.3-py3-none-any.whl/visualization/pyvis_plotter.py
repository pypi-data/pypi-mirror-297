import networkx as nx
from pyvis.network import Network
import matplotlib.colors as mcolors


def plot_graph_pyvis(graph):
    if not isinstance(graph, (nx.Graph, nx.DiGraph)):
        raise ValueError("Input must be a NetworkX Graph or DiGraph object")

    # Determine if the graph is directed
    is_directed = isinstance(graph, nx.DiGraph)

    # Create a Pyvis network graph
    g = Network(height="800px", width="100%", bgcolor="#222222", font_color="white", notebook=True, directed=is_directed)
    g.toggle_physics(True)
    g.force_atlas_2based()

    # Convert colors to hex
    def to_hex(color):
        return mcolors.to_hex(color)

    # Normalize edge weights
    edge_weights = [data['weight'] for _, _, data in graph.edges(data=True)]
    if edge_weights:
        min_weight, max_weight = min(edge_weights), max(edge_weights)
        weight_range = max_weight - min_weight
        normalized_weights = {
            (u, v): (data['weight'] - min_weight) / weight_range * 10 + 1 if weight_range > 0 else 1
            for u, v, data in graph.edges(data=True)
        }
    else:
        normalized_weights = {}

    # Normalize node sizes
    node_counts = [data['count'] for _, data in graph.nodes(data=True)]
    if node_counts:
        min_count, max_count = min(node_counts), max(node_counts)
        count_range = max_count - min_count
        normalized_sizes = {
            node: (data['count'] - min_count) / count_range * 30 + 10 if count_range > 0 else 10
            for node, data in graph.nodes(data=True)
        }
    else:
        normalized_sizes = {}

    # Add nodes with labels based on their count and normalized sizes
    for node, data in graph.nodes(data=True):
        g.add_node(
            node,
            label=f"{node}: {data['count']}",
            color=to_hex(data.get('color', '#FFFFFF')),  # Default to white if color not specified
            title=f"Count: {data['count']}",
            size=normalized_sizes.get(node, 10)
        )

    # Add edges with normalized weights and labels
    for u, v, data in graph.edges(data=True):
        edge_data = {
            'value': normalized_weights.get((u, v), 1),
            'color': to_hex(data.get('color', '#FFFFFF')),  # Default to white if color not specified
            'title': f"Weight: {data['weight']}",
            'label': str(data['weight'])
        }
        g.add_edge(u, v, **edge_data)

    # Show the graph
    g.show("nx.html")