import itertools

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

import scipy.sparse as sparse
from ipywidgets import *

from jupyterthemes import jtplot
jtplot.style(theme='grade3', figsize=(16, 10))


###################  COLOUR MAPS  ######################
from matplotlib.colors import LinearSegmentedColormap

optum_cmap = LinearSegmentedColormap.from_list(
    'optum', ["#E87722", "#A32A2E", "#422C88", "#078576", "#627D32"]
)
optum_cmap_simple = LinearSegmentedColormap.from_list(
    'optum', ["#E87722", "#078576"]
)  # for gradients
########################################################


def make_sequences(df, elements_field="new_elements", exits_field="new_exits"):
    """
    Generates sequences of item-exit_code and yields them
    """
    for _, row in df.iterrows():
        try:
            elements = np.array(row[elements_field].split("|")).astype(int)
            codes = np.array(row[exits_field].split("|")).astype(int)
            yield list(itertools.chain(*zip(elements, codes)))
        except AttributeError: # catches NaN
            pass
        
def build_pos(states):
    pos = dict()
    for key, state in states.items():
        for n, _state in enumerate(state):
            pos[_state["state_id"]] = (key, -n)
    return pos


def reset_edge_labels(G):
    edge_labels = dict()
    for start, end, attr in G.edges(data=True):
        G.remove_edge(start, end)
        G.add_edge(start, end, weight=attr["weight"])
        edge_labels[(start, end)] = round(attr["weight"], 3)
    return edge_labels


def build_node_labels(G, lookup):
    labels = dict()
    for node in G.nodes():
        label = lookup.get(G.node[node]["label"])
        labels[node] = label
    return labels