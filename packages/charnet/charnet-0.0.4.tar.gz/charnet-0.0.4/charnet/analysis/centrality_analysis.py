import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
from itertools import groupby
from operator import attrgetter
from typing import Callable, Dict, Any
from ..charnet import CharNet


def centrality_analysis(cnet: CharNet,
                        centrality_func: Callable[[...], Dict[Any, Dict]],
                        *,
                        start=None,
                        end=None) -> pd.DataFrame:
    """
    Generic centrality analysis function.

    :param cnet: CharNet object
    :param centrality_func: NetworkX centrality function to use
    :param start: start position
    :param end: end position
    :param centrality_kwargs: additional keyword arguments for the centrality function
    :return: pd.DataFrame with centrality results
    """
    results = pd.DataFrame()
    data_iter = cnet.data.itertuples()
    # if start:
    #     data_iter = (row for row in data_iter if row.position >= start)
    # if end:
    #     data_iter = (row for row in data_iter if row.position <= end)

    if end:
        end[-1] += 1
    subset = cnet.get_interval(start, end)
    data_iter = subset.data.itertuples()

    for position, group in groupby(data_iter, key=attrgetter('position')):
        graph = subset.get_graph(position)

        centrality_measures = centrality_func(graph)

        for char in graph.nodes:
            position_dict = dict(zip(cnet.idx2pos, position))
            new_row = {
                **position_dict,
                'character': char,
            }
            for measure, values in centrality_measures.items():
                if values is not None:
                    new_row[measure] = values[char]
            results = pd.concat([results, pd.DataFrame(new_row, index=[0])], ignore_index=True)

    return results


def simple_degree(cnet: CharNet, *, start=None, end=None, weighted=False) -> pd.DataFrame:
    def degree_func(graph: nx.DiGraph) -> dict[str, dict[Any, Any]]:
        result = {}
        if cnet.is_directed:
            in_degree = {node: graph.in_degree(node) for node in graph.nodes()}
            out_degree = {node: graph.out_degree(node) for node in graph.nodes()}
            result = {
                'in_degree': in_degree,
                'out_degree': out_degree,
            }
            weighted_in_degree = None
            weighted_out_degree = None
            if weighted:
                weighted_in_degree = {node: sum(d['weight'] for _, _, d in graph.in_edges(node, data=True))
                                      for node in graph.nodes()}
                weighted_out_degree = {node: sum(d['weight'] for _, _, d in graph.out_edges(node, data=True))
                                       for node in graph.nodes()}
            result.update({
                'weighted_in_degree': weighted_in_degree,
                'weighted_out_degree': weighted_out_degree
            })
        else:
            degree = {node: graph.degree(node) for node in graph.nodes()}
            result['degree'] = degree
            if weighted:
                weighted_degree = {node: sum(d['weight'] for _, _, d in graph.edges(node, data=True))
                                   for node in graph.nodes()}
                result['weighted_degree'] = weighted_degree
        return result

    return centrality_analysis(cnet, degree_func, start=start, end=end)


def degree_centrality(cnet: CharNet, *, start=None, end=None) -> pd.DataFrame:
    def degree_centrality_func(graph: nx.DiGraph) -> dict[str, dict[Any, Any]]:
        if cnet.is_directed:
            in_degree_centrality = nx.in_degree_centrality(graph)
            out_degree_centrality = nx.out_degree_centrality(graph)
            return {
                'in_degree_centrality': in_degree_centrality,
                'out_degree_centrality': out_degree_centrality
            }
        else:
            degree_centrality = nx.degree_centrality(graph)
            return {'degree_centrality': degree_centrality}

    return centrality_analysis(cnet, degree_centrality_func, start=start, end=end)


def betweenness_centrality(cnet: CharNet, *, start=None, end=None, normalized=True, weighted=False) -> pd.DataFrame:
    def betweenness_centrality_func(graph: nx.DiGraph) -> dict[str, dict[Any, Any]]:
        weight = 'weight' if weighted else None
        results = {
            'betweenness': nx.betweenness_centrality(graph, normalized=normalized, weight=weight)
        }
        return results

    return centrality_analysis(cnet, betweenness_centrality_func, start=start, end=end)


def closeness_centrality(cnet: CharNet, *, start=None, end=None, distance=None, wf_improved=True) -> pd.DataFrame:
    def closeness_centrality_func(graph: nx.DiGraph) -> dict[str, dict[Any, Any]]:
        closeness = {node: nx.closeness_centrality(graph, u=node, distance=distance, wf_improved=wf_improved) for node in graph.nodes()}
        return {'closeness': closeness}

    return centrality_analysis(cnet, closeness_centrality_func, start=start, end=end)


def eigenvector_centrality(cnet: CharNet, *, start=None, end=None, max_iter=100, tol=1e-06, weight=None) -> pd.DataFrame:
    def eigenvector_centrality_func(graph: nx.DiGraph) -> dict[str, dict[Any, Any]]:
        eigenvector = nx.eigenvector_centrality(graph, max_iter=max_iter, tol=tol, weight=weight)
        return {'eigenvector': eigenvector}

    return centrality_analysis(cnet, eigenvector_centrality_func, start=start, end=end)
