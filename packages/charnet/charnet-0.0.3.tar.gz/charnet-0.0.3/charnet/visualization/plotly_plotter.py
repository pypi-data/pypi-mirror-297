import plotly.graph_objects as go
import matplotlib.colors as mcolors
import networkx as nx


def plot_graph_plotly(graph):
    # Function to convert normalized color to hex
    def to_hex(color):
        return mcolors.to_hex(color)

    # Determine if the graph is directed
    is_directed = isinstance(graph, nx.DiGraph)

    # Given a graph, plot it with nodes colored by count and edges colored by weight
    node_x = [data['x'] for node, data in graph.nodes(data=True)]
    node_y = [data['y'] for node, data in graph.nodes(data=True)]
    node_text = [f"{node} (Count: {data['count']})" for node, data in graph.nodes(data=True)]
    node_color = [data['count'] for node, data in graph.nodes(data=True)]

    node_trace = go.Scatter(
        x=node_x,
        y=node_y,
        mode='markers',
        text=node_text,
        hoverinfo='text',
        marker=dict(
            size=[min(data['count'] * 2, 20) for node, data in graph.nodes(data=True)],
            color=node_color,
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(
                thickness=15,
                title='Node Count',
                xanchor='left',
                titleside='right'
            )
        )
    )

    edge_x = []
    edge_y = []
    edge_colors = []
    for edge in graph.edges(data=True):
        x0, y0 = graph.nodes[edge[0]]['x'], graph.nodes[edge[0]]['y']
        x1, y1 = graph.nodes[edge[1]]['x'], graph.nodes[edge[1]]['y']
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
        edge_colors.append(to_hex(edge[2]['color']))

    edge_trace = go.Scatter(
        x=edge_x,
        y=edge_y,
        line=dict(width=0.5, color='#888'),
        hoverinfo='none',
        mode='lines'
    )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        title='Dialogue Graph',
                        titlefont=dict(size=16),
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)
                    )
                    )

    # Add arrow annotations for edges with the respective colors
    if is_directed:
        for i, (u, v, data) in enumerate(graph.edges(data=True)):
            x0, y0 = graph.nodes[u]['x'], graph.nodes[u]['y']
            x1, y1 = graph.nodes[v]['x'], graph.nodes[v]['y']
            fig.add_annotation(
                ax=x0,
                ay=y0,
                axref='x',
                ayref='y',
                x=x1,
                y=y1,
                xref='x',
                yref='y',
                showarrow=True,
                arrowhead=2,
                arrowsize=1,
                arrowwidth=1,
                arrowcolor=edge_colors[i]
            )
    else:
        # For undirected graphs, we'll use lines instead of arrows
        for i, (u, v, data) in enumerate(graph.edges(data=True)):
            x0, y0 = graph.nodes[u]['x'], graph.nodes[u]['y']
            x1, y1 = graph.nodes[v]['x'], graph.nodes[v]['y']
            fig.add_trace(go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode='lines',
                line=dict(color=edge_colors[i], width=1),
                hoverinfo='none'
            ))

    # Add edge labels
    edge_labels = {(u, v): data['weight'] for u, v, data in graph.edges(data=True)}
    for (u, v), label in edge_labels.items():
        x = (graph.nodes[u]['x'] + graph.nodes[v]['x']) / 2
        y = (graph.nodes[u]['y'] + graph.nodes[v]['y']) / 2
        fig.add_annotation(
            x=x,
            y=y,
            text=str(round(label, 2)),
            showarrow=False,
            font=dict(size=10, color='#888')
        )

    fig.show()
