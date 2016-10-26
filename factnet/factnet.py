# main.py

import string
import pandas as pd

from bokeh.layouts import column, row
from bokeh.plotting import Figure, show
from bokeh.embed import standalone_html_page_for_models
from bokeh.models import ColumnDataSource, HoverTool, HBox, VBox
from bokeh.models.ranges import Range1d
from bokeh.models import LinearAxis
from bokeh.models.widgets import Slider, Select, TextInput, RadioGroup, Paragraph, Div
from bokeh.io import curdoc, save
from bokeh.charts import HeatMap, bins, output_file, vplot, TimeSeries, Line, Bar
from bokeh.charts.operations import blend
from bokeh.charts.attributes import cat
from bokeh.models import FixedTicker, SingleIntervalTicker, ColumnDataSource, DataRange1d
from bokeh.layouts import widgetbox
from bokeh.layouts import gridplot
import bokeh.palettes as palettes
from bokeh.resources import INLINE, CDN

import networkx as nx

import pickle
import gzip

with gzip.open("../data/preprocessed_df.pklz", "rb") as infile:
    df = pickle.load(infile)

B = nx.Graph()
B.add_nodes_from(df["pmcid"], bipartite=0)
B.add_nodes_from(df["term"], bipartite=1)
for row in df.iterrows():
    B.add_edge(row[1]["pmcid"], row[1]["term"])
term_nodes, paper_nodes = bipartite.sets(B)
term_projection = nx.bipartite.weighted_projected_graph(B, term_nodes)
paper_projection = nx.bipartite.weighted_projected_graph(B, paper_nodes)
nx.set_node_attributes(term_projection, "degree", nx.degree_centrality(term_projection))

nodes = dict()
nodes["group1"] = [(n,d) for n, d in term_projection.nodes(data=True) if d["bipartite"]==0]
nodes["group2"] = [(n,d) for n, d in term_projection.nodes(data=True) if d["bipartite"]==1]

edges = dict()
edges['group1'] = [(u,v,d) for u,v,d in term_projection.edges(data=True)]

def getDegree(item):
    return item[1].get("degree")

for group, nodelist in nodes.items():
    nodes[group] = sorted(nodelist, key=getDegree)
    nodes[group] = [n for n, d in nodes[group]]

edges = dict()
edges['group1'] = [(u,v,d) for u,v,d in term_projection.edges(data=True)]

nodes_cmap = dict()
nodes_cmap['group0'] = 'green'
nodes_cmap['group1'] = 'red'
nodes_cmap['group2'] = 'blue'

edges_cmap = dict()
edges_cmap['group1'] = 'green'

h = HivePlot(nodes, edges, nodes_cmap, edges_cmap)
h.draw()
