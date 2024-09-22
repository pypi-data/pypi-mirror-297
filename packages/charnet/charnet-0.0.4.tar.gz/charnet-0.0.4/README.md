![license](https://img.shields.io/github/license/MediaCompLab/CharNet.svg)
![package](https://github.com/MediaCompLab/CharNet/actions/workflows/python-package.yml/badge.svg?event=push)
![publish](https://github.com/MediaCompLab/CharNet/actions/workflows/python-publish.yml/badge.svg)

# CharNet: Dynamic Social Network Analysis for TV Series Dialogues

CharNet is a Python package designed for performing graph analysis on dynamic social networks based on dialogues in TV series. It provides tools for loading dialogue data, calculating and creating weighted graphs, and visualizing character interactions over time.

- **Github:** https://github.com/MediaCompLab/CharNet

## Simple example

---

```python
import charnet as cn
import pandas as pd

df = pd.read_csv('bigbang_lines_test.csv')
net_test = cn.CharNet(df, ('Season', 'Episode', 'Scene', 'Line'),
                   interactions='Words', speakers='Speaker', listeners='Listener', directed=True)
net_test.get_weights(lambda x: len(x))
net_test.draw(plot='matplotlib')

net_test.get_weights(lambda x: len(x))
net_test.set_min_step('Scene')
subset = net_test.get_interval((1, 1, 1, 1), (1, 2, 1, 1))
subset.normalize_weights()
subset.set_layout('circular')
subset.draw(plot='matplotlib')

from charnet.analysis import simple_degree

degree_results = simple_degree(subset, weighted=True)
degree_results.to_csv('results.csv', index=False)
```

## Install

---

Install the latest version of CharNet:

```bash
$ pip install charnet
```
Install with all optional dependencies:
```bash
$ pip install charnet[all]
```

## To Do
- [x] Add non-directed graph support
- [x] Add closeness centrality
- [x] Add Eigenvector centrality
- [ ] Add Louvain community detection
- [ ] Add temporal visualization
- [ ] Add centrality visualizer (with visualization)

## License

Released under the [GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.en.html).

```
Copyright (c) 2024 Media Comprehension Lab
```
