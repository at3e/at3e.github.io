# -*- coding: utf-8 -*-
"""
Created on Fri Sep  8 14:32:16 2023

@author: atreyees
"""
import random
import dgl
import networkx as nx
import numpy as np
import torch
import pickle
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
random.seed(7)

# edge_list = [(0, 1), (2, 1), (0, 2), (4, 3), (2, 4), (3, 1), (4, 0), (5, 1), (5, 0)]
edge_list = [(0, 1), (2, 1), (0, 2), (4, 3), (2, 4), (3, 1), (4, 0), (5, 1), (5, 0),
             (5, 6), (5, 7), (7, 8), (7, 9), (9, 5)]
# g = dgl.graph(([0, 2, 0, 4, 2, 3, 4, 1, 5], [1, 1, 2, 3, 4, 1, 0, 5, 0]))
# g.edata['w'] = torch.arange(18).view(9, 2)
g = nx.DiGraph()
g .add_edges_from(edge_list)

with open('sample_graph.dat', 'rb') as fp:
    g = pickle.load(fp)

plt.figure(figsize=(15,15))
# Draw the graph
pos = nx.spring_layout(g)
nx.draw(g, pos, node_color='skyblue', node_size=800, node_shape='s', font_size=10, font_color='black', font_weight='bold', edge_color='gray', width=1.0, arrows=True)
nx.draw_networkx_labels(g,pos)
# Show the plot
plt.show()

# Partition graph
Node_list = list(g.nodes())
k = 3
S = []
Nodes_visited = []

while len(list(set(Nodes_visited))) < len(g.nodes()):
    node = random.choice(Node_list)
    Nodes_visited.append(node)
    if len(g.out_edges(node))==0:
        continue
    loads = list(set(g.successors(node)).difference(set(Nodes_visited)))+[node]
    Nodes_visited += loads
    if len(loads)>0:
        sg = set(loads)
        # Nodes_visited = list(set(Nodes_visited))
        S.append(sg)
    Node_list = list(n for n in g.nodes() if n not in Nodes_visited)

plt.figure(figsize=(15,15))
i = 0
colors = np.random.choice(list(mcolors.CSS4_COLORS), len(S), replace=False)
for s in S:
    i+=1
    sg = g.subgraph(list(s))
    
    nx.draw_networkx(sg, pos=pos, node_size=800, node_shape='s', node_color = colors[i])

plt.show()
# for node in g.nodes():
#     # g.nodes[node].update({'IN': g.in_degree(node), 'OUT': g.out_degree(node)+1})
#     g.nodes[node].update({'IN': random.randint(1, 4), 'OUT': random.randint(1, 6)})
# dg = dgl.from_networkx(g)
# Node_list = dg.nodes()
# k = 2
# S = []
# Node_list_visited = []
# while len(Node_list) > k:
#     node = random.choice(Node_list)
#     if len(dg.out_edges(node)[0])==0:
#         continue
#     sg, inverse_indices = dgl.khop_out_subgraph(dg, node, k=2)
#     # print(node)
#     # print(sg.nodes())
#     # print(sg.edges())
#     S.append(sg)
#     for s in S:
#         # print(s.nodes())
#         # print(s.edges())
#         Node_list_visited += list(n for n in s.nodes())
#         # print(Node_list_visited)
#     Node_list_visited.append(torch.tensor(node))
#     Node_list = list(n for n in dg.nodes() if n not in Node_list_visited)


# # Form subgraphs
# sg = S.pop()
# sg_logic = nx.DiGraph()

# # Initiate LUT names
# for node in sg.nodes():
#     inLUTs = g.nodes[int(node)]['IN']
#     pin = random.randint(1, 4)
#     print(pin)
#     outLUTs = g.nodes[int(node)]['OUT'] // pin
#     outFLOPs = g.nodes[int(node)]['OUT'] % pin
#     g.nodes[int(node)].update({'pins': pin, 'inLUTs': list('INT'+str(int(node))+'_LUT_in'+str(i+1) for i in range(inLUTs)), 
#                           'outLUTs': list('INT'+str(int(node))+'_LUT_out'+str(i+1) + '['+str(j)+']' for i in range(outLUTs) for j in range(4)),
#                           'outFFs': list('INT'+str(int(node))+'_FF_out'+str(i+1) for i in range(outFLOPs))})
#     # Add nodes to logic graph
#     for lgnode in g.nodes[int(node)]['inLUTs']+g.nodes[int(node)]['outLUTs']+g.nodes[int(node)]['outFFs']:
#         sg_logic.add_node(lgnode)
        
# # Assign logic graph edges
# inPins_assigned = []
# outPins_assigned = []
# for node in sg.nodes():
#     for edge in g.in_edges(int(node)):
#         if torch.tensor(edge[0]) not in sg.nodes():
#             continue
#         print(edge)
#         inPins = g.nodes[edge[0]]['inLUTs']
        
#         if len(inPins_assigned)==0:
#             inPin = random.choice(inPins)
#         else:
#             inPin = random.choice(list(pin for pin in inPins if pin not in inPins_assigned))
#         inPins_assigned.append(inPin)
#         outPins = g.nodes[int(node)]['outLUTs']+g.nodes[int(node)]['outFFs']
#         # print(g.nodes[int(node)]['outLUTs'])
#         if len(outPins_assigned)==0:
#             outPin = random.choice(outPins)
#         elif len(list(pin for pin in outPins if pin not in outPins_assigned))==0:
#             continue
#         else:
#             outPin = random.choice(list(pin for pin in outPins if pin not in outPins_assigned))
#         outPins_assigned.append(outPin)
#         sg_logic.add_edge(inPin, outPin)


