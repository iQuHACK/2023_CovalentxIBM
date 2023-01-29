import networkx as nx
import pandas as pd
from radius_of_infection import *
import matplotlib.pyplot as plt

data=prepare_dataframe('Book1.xlsx')
final_dataframe=infection_circle(data,2)

edges_lst=[]

for i in range(len(final_dataframe)):
    temp_lst=[]
    temp_lst=[final_dataframe.iloc[i][0],final_dataframe.iloc[i][1]]
    edges_lst+=[temp_lst]

print(edges_lst)

network=nx.Graph()
network.add_edges_from(edges_lst)
nx.draw(network, with_labels = True, node_color='#7ab8f5', width=2, font_size=16, node_size=700, pos=nx.planar_layout(network))
plt.show()
plt.savefig('plotgraph.png', dpi=300, bbox_inches='tight')