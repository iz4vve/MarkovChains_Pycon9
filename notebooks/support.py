import itertools

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np
import pandas as pd
import seaborn as sns

from ipywidgets import *

from jupyterthemes import jtplot
jtplot.style(theme='grade3', figsize=(16, 10))


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