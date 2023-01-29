import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd 
import io 

# df = pd.read_excel(io.BytesIO(uploaded1['sensor.xlsx']))
# vf = pd.read_csv(io.BytesIO(uploaded2['value.txt']))

# df_new = df.to_numpy()

file=open("infection.csv")
file=file.read()
df_new=pd.read_csv("infection.csv")



df=df_new.to_numpy()




print(df)

last_time_limit_value = 25
the_distance_limit_value = 1.5
the_frequency_limit_value = 2

# print(df_new)
# print(vf.columns)

def Create_the_mat(the_matrix):
  # Defining a Class
  class GraphVisualization:
   
      def __init__(self):
          
        # visual is a list which stores all 
        # the set of edges that constitutes a
        # graph
          self.visual = []
          
    # addEdge function inputs the vertices of an
    # edge and appends it to the visual list
      def addEdge(self, a, b):
          temp = [a, b]
          self.visual.append(temp)
          
    # In visualize function G is an object of
    # class Graph given by networkx G.add_edges_from(visual)
    # creates a graph with a given list
    # nx.draw_networkx(G) - plots the graph
    # plt.show() - displays the graph
      def visualize(self):
          G = nx.Graph()
          G.add_edges_from(self.visual)
          nx.draw_networkx(G)
          plt.show()
  
# Driver code
  G = GraphVisualization()
  print(the_matrix)
 
  for i in range(1,len(the_matrix)):
    print(type(the_matrix))

    G.addEdge(the_matrix.iloc[i,1], the_matrix.iloc[i,2])
  G.visualize()

def cost_function(last_time_limit, the_distance_limit, the_frequency_limit, df_new):
  the_matrix = df_new
  if(last_time_limit==1):
    the_matrix = [row for row in the_matrix if not row[2] > int(last_time_limit_value)]
  if(the_distance_limit==1):
    the_matrix = [row for row in the_matrix if not float(row[4]) > float(the_distance_limit_value)]
  if(the_frequency_limit==1):
    the_matrix = [row for row in the_matrix if not float(row[3]) < float(the_frequency_limit_value)]

  Create_the_mat(the_matrix)  
  return the_matrix[:,0:2]

output_matrix = cost_function(0, 0, 0, df_new) 

output_matrix