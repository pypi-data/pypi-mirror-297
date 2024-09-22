import gravis as gv
import matplotlib.colors as mcolors


def plot_graph_gravis(graph):
    temp_graph = graph.copy()
    for node in graph.nodes:
        temp_graph.nodes[node]['color'] = mcolors.to_hex(graph.nodes[node]['color'])
    for u, v, data in graph.edges(data=True):
        temp_graph[u][v]['color'] = mcolors.to_hex(data['color'])
        temp_graph[u][v]['label'] = data['weight']
    g = gv.d3(temp_graph,
              edge_size_data_source='weight',
              use_edge_size_normalization=True,
              show_details_toggle_button=True,
              node_hover_neighborhood=True,
              show_menu=True)
    g.display()
