import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
import qiskit
from qiskit import *

from qiskit.tools.visualization import plot_histogram

from qiskit import QuantumCircuit, 

# nodes 
n = 20

#Graph Model with Edges (basic)
G = nx.Graph()
G.add_nodes_from([0, 1, 2, 3])
G.add_edges_from([(0, 1), (1, 2)])
nx.draw(G, with_labels=True, alpha=0.8, node_size=500)

nqubits = 7

qc = 
