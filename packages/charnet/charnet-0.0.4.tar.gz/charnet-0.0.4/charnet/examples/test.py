from charnet import *
import pandas as pd

# Example usage

df = pd.read_csv('../../bigbang_lines_test.csv')

# custom weight function
# input: interaction (str)
# output: weight (float)
def weight_func(interaction):
    return len(interaction)

# load data
# input: dataframe (pd.DataFrame), 
#        columns for position (tuple), 
#        column for interactions/dialogue (str), 
#        column for speakers (str), 
#        column for listeners (str)
net_test = CharNet(df, ('Season', 'Episode', 'Scene', 'Line'),
                   interactions='Words', speakers='Speaker', listeners='Listener', directed=True)
# net_test.load_data(df, ('Season', 'Episode', 'Scene', 'Line'),
#                    interactions='Words', speakers='Speaker', listeners='Listener')
# calculate weights using interaction
# input: weight function (function)
net_test.get_weights(weight_func)

# normalize weights
# net_test.normalize_weights()

# set minimum step for position
net_test.set_min_step('Scene')

# get subset of data
# input: start position (tuple), end position (tuple, exclusive)
# subset = net_test.get_interval((1, 1, 1), (1, 1, 3))

# get graph
# input: subset (pd.DataFrame)
# output: graph (nx.Graph)
# graph = subset.get_graph()

# set layout
# input: graph (nx.Graph), layout (str) [spring, kamada_kawai, circular, random]
net_test.set_layout('circular')
# subset.set_layout('circular')

# subset.draw(plot='matplotlib')

# draw graph
# input: graph (nx.Graph), plot (str) [matplotlib, plotly, gravis, pyvis]
# net_test.draw(plot='matplotlib')

# subset.data.to_csv('bigbang_lines_test.csv', index=False)
# degree_results = simple_degree(subset, weighted=True)
# degree_results.to_csv('simple_degree.csv', index=False)
# degree_results = degree_centrality(subset)
# degree_results.to_csv('degree_centrality.csv', index=False)
# degree_results = betweenness_centrality(subset, weighted=True)
# degree_results.to_csv('betweenness_centrality.csv', index=False)
degree_results = closeness_centrality(net_test)
print(degree_results)

# subset.draw(plot='matplotlib')
