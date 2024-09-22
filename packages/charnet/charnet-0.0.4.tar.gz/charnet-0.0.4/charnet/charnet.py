import contextlib
import warnings
from itertools import takewhile, combinations

import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from .utils import default_directed_agg_weight, default_undirected_agg_weight
from .visualization import (
    plot_graph_matplotlib,
    plot_graph_plotly,
    plot_graph_gravis,
    plot_graph_pyvis
)


class CharNet:

    def __init__(self, data=None, position_columns=None, speakers='speakers', listeners='listeners',
                 interactions='interactions', weights=None, directed=True):
        self.data = None
        self.pos2idx = dict()
        self.idx2pos = None
        self._graph = None
        self._time_point = None
        self._layout = None
        self._directed = directed

        if data is not None:
            self.load_data(data, position_columns, speakers, listeners, interactions, weights)

    def load_data(self, data, position_columns, speakers='speakers', listeners='listeners', interactions='interactions',
                  participants=None, weights=None):
        """
        Load data into CharNet and ensure it's sorted by position.

        :param data: pd.DataFrame, data containing the conversation lines
        :param position_columns: tuple, column names representing the hierarchical order of each line
        :param speakers: str, column name for speakers
        :param listeners: str, column name for listeners
        :param interactions: str, column name for interactions
        :param participants: str, column name for participants (for undirected graphs)
        :param weights: str or None, column name for weights (if any)
        """
        # get the data
        df = data.copy()

        # check if the columns are present in the data
        required_columns = list(position_columns) + [speakers, listeners]
        if not all(col in df.columns for col in required_columns):
            raise ValueError("Not all required columns found in the data.")

        self.pos2idx = {col: idx for idx, col in enumerate(position_columns)}

        for col in position_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

        df['position'] = df[list(position_columns)].apply(tuple, axis=1)

        def process_column(series):
            return series.apply(lambda x: list(set(
                str(item).strip() for item in (x if isinstance(x, list) else str(x).strip('[]').split(',')) if item)))

        if self._directed:
            df[speakers] = process_column(df[speakers])
            df[listeners] = process_column(df[listeners])
            df = df.rename(columns={speakers: 'speakers', listeners: 'listeners'})
        else:
            # For undirected graphs, we need to combine speakers and listeners
            if participants:
                df[participants] = process_column(df[participants])
                df = df.rename(columns={participants: 'participants'})
            else:
                df[speakers] = process_column(df[speakers])
                df[listeners] = process_column(df[listeners])
                df['participants'] = df.apply(lambda row: list(set(row[speakers] + row[listeners])), axis=1)

        if interactions:
            df = df.rename(columns={interactions: 'interactions'})
        if weights:
            df = df.rename(columns={weights: 'weights'})

        columns_to_keep = (list(position_columns) + ['position'] +
                           (['speakers', 'listeners'] if self._directed else ['participants']) +
                           (['interactions'] if interactions else []) +
                           (['weights'] if weights else []))
        df = df[columns_to_keep]

        df = df.sort_values(by=list(position_columns)).reset_index(drop=True)

        self.data = df
        self.idx2pos = position_columns

        self._graph = None
        self._time_point = None
        self._layout = None

        return self

    def get_weights(self, calculator=lambda x: 1):
        """
        Calculate weights based on interactions.
        
        :param interactions: str, column name for interactions
        :param calculator: callable, function to calculate weights
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data using the load_data method.")
        if 'interactions' not in self.data.columns:
            raise ValueError(f"Column 'interactions' not found in the data.")

        self.data['weights'] = self.data['interactions'].apply(calculator)

    def normalize_weights(self):
        """
        Normalize weights.
        """
        if 'weights' not in self.data.columns:
            raise ValueError("Column 'weights' not found in the data.")
        self.data['weights'] = self.data['weights'] / self.data['weights'].max()
        self._graph = None
        return self

    @property
    def time_point(self):
        return self._time_point

    def __set_time_point(self, time: tuple):
        """
        Set the current time point.

        :param time: tuple, time point for the current position
        """
        self._time_point = time

        return self._time_point

    def __get_max_time_point(self):
        return tuple(self.data.iloc[-1]['position'])

    def get_interval(self, start=None, end=None):
        """
        Get a subset of the data based on the start and end time points.
        
        :param start: dict, dictionary containing the start time points for some position columns
        :param end: dict, dictionary containing the end time points for some position columns
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data using the load_data method.")

        interval = CharNet(directed=self._directed)
        interval.data = self.data.copy()
        if start:
            interval.data = interval.data[interval.data['position'] >= start]
        if end:
            interval.data = interval.data[interval.data['position'] < end]
        interval.idx2pos = self.idx2pos
        interval.pos2idx = self.pos2idx.copy()
        interval.set_layout(self._layout)

        return interval

    def set_min_step(self, min_step, weight_func=None):
        """
        Set the minimum step size for the position columns.

        :param aggregate_fn:
        :param min_step: int, minimum step size
        """
        if min_step not in self.idx2pos:
            raise ValueError(f"'{min_step}' is not a valid position column.")

        if 'weights' not in self.data.columns:
            self.get_weights()
            warnings.warn("No weights found. Calculating weights using default function.")

        min_step_index = self.pos2idx[min_step]
        group_columns = self.idx2pos[:min_step_index + 1]

        aggregate_fn = lambda df: self.step_agg_func(df, min_step, weight_fn=weight_func)
        grouped_data = self.data.groupby(list(group_columns)).apply(aggregate_fn).reset_index(drop=True)
        self.data = grouped_data

        self.idx2pos = self.idx2pos[:min_step_index + 1]
        self.pos2idx = {col: idx for idx, col in enumerate(self.idx2pos)}

        self._graph = None
        return self

    def step_agg_func(self, df, min_step, weight_fn=None):
        """
        Default aggregation function for minimum step.
        Counts the number of dialogues between each pair of speakers and listeners.

        :param weight_fn: callable, function to calculate weights (df -> dict)
        :param min_step:
        :param df: pd.DataFrame, dataframe containing rows within the minimum step
        :return: pd.DataFrame, aggregated rows with dialogue counts
        """
        if weight_fn is None:
            weight_fn = default_directed_agg_weight if self._directed else default_undirected_agg_weight
        agg_weights = weight_fn(df)

        agg_position = df['position'].iloc[0][:self.pos2idx[min_step] + 1]
        position_dict = dict(zip(self.idx2pos[:self.pos2idx[min_step] + 1], agg_position))

        if self._directed:
            aggregated = pd.DataFrame([
                {
                    **position_dict,
                    'position': agg_position,
                    'speakers': speaker,
                    'listeners': listener,
                    'weights': count
                }
                for (speaker, listener), count in agg_weights.items()
            ])
        else:
            aggregated = pd.DataFrame([
                {
                    **position_dict,
                    'position': agg_position,
                    'participants': participant,
                    'weights': count
                }
                for participant, count in agg_weights.items()
            ])

        return aggregated

    @property
    def is_directed(self):
        return self._directed

    def __create_digraph(self, time_point):
        digraph = nx.DiGraph()
        for row in takewhile(lambda r: r.position <= time_point, self.data.itertuples()):
            speakers = row.speakers if isinstance(row.speakers, list) else [row.speakers]
            listeners = row.listeners if isinstance(row.listeners, list) else [row.listeners]
            weight = getattr(row, 'weights', 1)

            for speaker in speakers:
                if speaker not in digraph:
                    digraph.add_node(speaker, count=1)
                else:
                    digraph.nodes[speaker]['count'] += 1

                for listener in listeners:
                    if listener not in digraph:
                        digraph.add_node(listener, count=1)
                    else:
                        digraph.nodes[listener]['count'] += 1

                    if digraph.has_edge(speaker, listener):
                        digraph[speaker][listener]['weight'] += weight
                    else:
                        digraph.add_edge(speaker, listener, weight=weight)
        return digraph

    def __create_graph(self, time_point):
        graph = nx.Graph()
        for row in takewhile(lambda r: r.position <= time_point, self.data.itertuples()):
            participants = row.participants if isinstance(row.participants, list) else [row.participants]
            weight = getattr(row, 'weights', 1)

            for part in participants:
                if part not in graph:
                    graph.add_node(part, count=1)
                else:
                    graph.nodes[part]['count'] += 1

            for part1, part2 in combinations(participants, 2):
                if graph.has_edge(part1, part2):
                    graph[part1][part2]['weight'] += weight
                else:
                    graph.add_edge(part1, part2, weight=weight)

        return graph

    def __update_graph(self, time_point):
        print("update_graph - time_point", time_point)
        print("update_graph - self._time_point", self._time_point)
        if time_point > self._time_point:
            print("update_graph: adding nodes and edges")
            # Add new nodes and edges
            print(self.data.itertuples())
            is_sorted = all(
                self.data['position'].iloc[i] <= self.data['position'].iloc[i + 1] for i in range(len(self.data) - 1))
            print(f"Is data sorted by position? {is_sorted}")
            for row in self.data.itertuples():
                if self._time_point < row.position <= time_point:
                    print("update_graph: adding row")
                    print(row)
                    self.__add_row_to_graph(row)
                elif row.position > time_point:
                    break
        else:
            print("update_graph: removing nodes and edges")
            # Remove nodes and edges
            for row in reversed(list(self.data.itertuples())):
                if time_point < row.position <= self._time_point:
                    print("update_graph: removing row")
                    print(row)
                    self.__remove_row_from_graph(row)
                elif row.position < time_point:
                    break

        self._time_point = time_point

    def __add_row_to_graph(self, row):
        if self._directed:
            speakers = row.speakers if isinstance(row.speakers, list) else [row.speakers]
            listeners = row.listeners if isinstance(row.listeners, list) else [row.listeners]
            weight = getattr(row, 'weights', 1)

            for speaker in speakers:
                self.__add_or_update_node(speaker)
                for listener in listeners:
                    self.__add_or_update_node(listener)
                    self.__add_or_update_edge(speaker, listener, weight)
        else:
            participants = row.participants if isinstance(row.participants, list) else [row.participants]
            weight = getattr(row, 'weights', 1)

            for part in participants:
                self.__add_or_update_node(part)
            for part1, part2 in combinations(participants, 2):
                self.__add_or_update_edge(part1, part2, weight)

    def __remove_row_from_graph(self, row):
        if self._directed:
            speakers = row.speakers if isinstance(row.speakers, list) else [row.speakers]
            listeners = row.listeners if isinstance(row.listeners, list) else [row.listeners]
            weight = getattr(row, 'weights', 1)
            for speaker in speakers:
                for listener in listeners:
                    self.__remove_or_update_edge(speaker, listener, weight)
                    self.__remove_or_update_node(speaker)
                    self.__remove_or_update_node(listener)
        else:
            participants = row.participants if isinstance(row.participants, list) else [row.participants]
            weight = getattr(row, 'weights', 1)
            for part1, part2 in combinations(participants, 2):
                self.__remove_or_update_edge(part1, part2, weight)
            for part in participants:
                self.__remove_or_update_node(part)

    def __add_or_update_node(self, node):
        if node not in self._graph:
            self._graph.add_node(node, count=1)
        else:
            self._graph.nodes[node]['count'] += 1

    def __add_or_update_edge(self, node1, node2, weight):
        if self._graph.has_edge(node1, node2):
            self._graph[node1][node2]['weight'] += weight
        else:
            self._graph.add_edge(node1, node2, weight=weight)

    def __remove_or_update_edge(self, node1, node2, weight):
        self._graph[node1][node2]['weight'] -= weight
        if self._graph[node1][node2]['weight'] == 0:
            self._graph.remove_edge(node1, node2)

    def __remove_or_update_node(self, node):
        self._graph.nodes[node]['count'] -= 1
        if self._graph.nodes[node]['count'] == 0:
            self._graph.remove_node(node)

    def get_graph(self, time_point=None):
        """
        Get the graph representation of the current data.

        :return: nx.DiGraph, the graph representation
        """
        if self.data is None:
            raise ValueError("No data loaded. Please load data using the load_data method.")

        if self._layout is None:
            warnings.warn("No layout set. Using 'spring' layout by default.")
            self.set_layout('spring')

        if time_point is None:
            print("get_graph: no time_point")
            time_point = self.__get_max_time_point()
        else:
            if not all(isinstance(t, int) for t in time_point):
                raise ValueError("Time points must be integers.")
            if len(time_point) != len(self.idx2pos):
                raise ValueError("Time points must match the number of position columns.")

        if self._graph is None:
            print("get_graph: creating graph")
            self._graph = self.__create_digraph(time_point) if self._directed else self.__create_graph(time_point)
        elif time_point != self._time_point:
            print("get_graph: updating graph")
            self.__update_graph(time_point)
        print("#nodes:", len(self._graph.nodes))
        print("#edges:", len(self._graph.edges))
        self.__set_time_point(time_point)

        return self._graph

    @contextlib.contextmanager
    def graph_context(self):
        """
        context manager for graph operations.
        """
        graph = self._graph
        try:
            yield graph
        finally:
            self._graph = None

    @property
    def layout(self):
        return self._layout

    def set_layout(self, layout='spring'):
        """
        Set the layout for the graph representation.

        :param layout: str, the layout algorithm to use
        :return: self, for method chaining
        """
        self._layout = layout
        if self._graph is not None:
            self._apply_layout()

    def _apply_layout(self):
        if self._graph is None:
            raise ValueError("No graph available. Call get_graph() first.")
        if self._layout == 'spring':
            pos = nx.spring_layout(self._graph)
        elif self._layout == 'kamada_kawai':
            pos = nx.kamada_kawai_layout(self._graph)
        elif self._layout == 'circular':
            pos = nx.circular_layout(self._graph)
        elif self._layout == 'random':
            pos = nx.random_layout(self._graph)
        else:
            raise ValueError(f"Invalid layout '{self._layout}'.")

        pos_scaled = nx.rescale_layout_dict(pos, scale=100)

        node_count = [data['count'] for node, data in self._graph.nodes(data=True)]
        edge_weight = [data['weight'] for u, v, data in self._graph.edges(data=True)]
        min_max_node = (min(node_count), max(node_count))
        min_max_edge = (min(edge_weight), max(edge_weight))

        # Use a colormap to map counts and weights to colors
        cmap = plt.cm.viridis
        norm_node = plt.Normalize(*min_max_node)
        norm_edge = plt.Normalize(*min_max_edge)

        for node in self._graph.nodes:
            self._graph.nodes[node]['x'] = pos_scaled[node][0]
            self._graph.nodes[node]['y'] = pos_scaled[node][1]
            self._graph.nodes[node]['color'] = cmap(norm_node(self._graph.nodes[node]['count']))

        for u, v, data in self._graph.edges(data=True):
            data['color'] = cmap(norm_edge(data['weight']))

    def draw(self, plot: str = 'matplotlib'):
        """
        Draw the dynamic graphs.
        
        :param plot: test_visualization library to use
        :param graph: nx.DiGraph, graph to be plotted
        """
        graph = self.get_graph()
        if self._layout is not None:
            self._apply_layout()
        if plot == 'matplotlib':
            plot_graph_matplotlib(graph)
        elif plot == 'plotly':
            plot_graph_plotly(graph)
        elif plot == 'gravis':
            plot_graph_gravis(graph)
        elif plot == 'pyvis':
            plot_graph_pyvis(graph)
