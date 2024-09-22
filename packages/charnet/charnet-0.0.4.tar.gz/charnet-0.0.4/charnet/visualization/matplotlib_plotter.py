from matplotlib import pyplot as plt
import networkx as nx


def plot_graph_matplotlib(graph):
    # Given a graph, plot it with nodes colored by count and edges colored by weight
    pos = {node: (data['x'], data['y']) for node, data in graph.nodes(data=True)}
    node_colors = [data['color'] for node, data in graph.nodes(data=True)]
    edge_labels = {(u, v): data['weight'] for u, v, data in graph.edges(data=True)}
    edge_colors = {(u, v): data['color'] for u, v, data in graph.edges(data=True)}

    is_directed = isinstance(graph, nx.DiGraph)

    # only for directed graphs
    double_edges = []
    if is_directed:
        double_edges = [(u, v) for u, v in graph.edges if graph.has_edge(v, u)]
        double_edges = double_edges + [(v, u) for u, v in double_edges]
    double_edges_colors = [edge_colors[edge] for edge in double_edges]

    pos_edges = pos.copy()

    # Increase figure size
    plt.figure(figsize=(12, 9))

    single_edges = [edge for edge in graph.edges if edge not in double_edges]
    single_edges_colors = [edge_colors[edge] for edge in single_edges]

    if is_directed:
        for u, v in double_edges:
            offset = 0.1
            pos_edges[(u, v)] = (pos[u][0] + offset, pos[u][1] + offset)
            pos_edges[(v, u)] = (pos[v][0] - offset, pos[v][1] - offset)

    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors)

    # Draw edges
    if is_directed:
        # Draw edges with arrows for directed graphs
        nx.draw_networkx_edges(graph, pos, edgelist=single_edges, edge_color=single_edges_colors,
                               alpha=0.5, arrows=True)
        nx.draw_networkx_edges(graph, pos_edges, edgelist=double_edges, edge_color=double_edges_colors,
                               connectionstyle='arc3,rad=0.2', alpha=0.5, arrows=True)
    else:
        # Draw edges without arrows for undirected graphs
        nx.draw_networkx_edges(graph, pos, edge_color=list(edge_colors.values()), alpha=0.5)

    # Draw labels
    nx.draw_networkx_labels(graph, pos, font_size=12)

    # Draw edge labels
    ax = plt.gca()
    for (u, v), label in edge_labels.items():
        x = (pos[u][0] + pos[v][0]) / 2
        y = (pos[u][1] + pos[v][1]) / 2
        dx = pos[v][0] - pos[u][0]
        dy = pos[v][1] - pos[u][1]

        if is_directed and (u, v) in double_edges:
            offset_x = dy * 0.1
            offset_y = -dx * 0.1
        else:
            offset_x = 0
            offset_y = 0

        ax.annotate(round(label, 2), xy=(x + offset_x, y + offset_y),
                    textcoords='offset points', xytext=(0, 0),
                    ha='center', va='center', fontsize=10,
                    color=edge_colors[(u, v)],
                    bbox=dict(facecolor='white', alpha=0.0, edgecolor='none'))

    plt.axis('off')
    plt.tight_layout()
    plt.show()
