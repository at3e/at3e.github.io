# -*- coding: utf-8 -*-
"""
Created on Mon Sep 11 16:00:41 2023

@author: atreyees
"""
import os
import pickle
import random
import itertools
import networkx as nx
import pdb

class Net:
    def __init__(self, id_, fanout, src, src_coord, dst, dst_coord):
        self.net_id = id_
        self.fanout = fanout
        self.src = src
        if src is not None:
            self.src_x = int(src_coord[0])
            self.src_y = int(src_coord[1])
        else:
            self.src_x = None; self.src_y = None
        self.dst = list()
        self.dst_x = list()
        self.dst_y = list()
        
        self.INTusage_North = 0
        self.INTusage_South = 0
        self.INTusage_East = 0
        self.INTusage_West = 0
        
        for i in range(fanout):
            self.dst.append(dst[i])
            self.dst_x.append(int(dst_coord[i][0]))
            self.dst_y.append(int(dst_coord[i][1]))
            if int(dst_coord[i][0]) > int(src_coord[0]):
                self.INTusage_East += 1
            elif int(dst_coord[i][0]) < int(src_coord[0]):
                self.INTusage_West += 1
            
            if int(dst_coord[i][1]) > int(src_coord[1]):
                self.INTusage_North += 1
            elif int(dst_coord[i][1]) < int(src_coord[1]):
                self.INTusage_South += 1

        x = self.dst_x + [self.src_x]
        y = self.dst_y + [self.src_y]
    
        self.BBox_blcoord = (min(x), min(y))
        self.BBox_urcoord = (max(x), max(y))

dir_ = "nets"
with open(os.path.join(dir_, "bloom_filter.dat"), "rb") as fp:
    Nets = pickle.load(fp)
G = nx.DiGraph()
edge_list = []
for net in Nets:
    if net.src is not None:
        for i in range(net.fanout):
            edge = ("INT_X"+str(net.src_x)+"Y"+str(net.src_y), "INT_X"+str(net.dst_x[i])+"Y"+str(net.dst_y[i]))
            if edge not in G.edges():
                G.add_edge(edge[0], edge[1])
                G[edge[0]][edge[1]]['w'] = 1
            else:
                G[edge[0]][edge[1]]['w'] += 1

            edge_list.append(("INT_X"+str(net.src_x)+"Y"+str(net.src_y), 
                              "INT_X"+str(net.dst_x[i])+"Y"+str(net.dst_y[i])))

nx.draw(G,
        node_color='lightgreen', 
        with_labels=True,
        node_size=60)

# for node in G.nodes():
#     # g.nodes[node].update({'IN': g.in_degree(node), 'OUT': g.out_degree(node)+1})
#     G.nodes[node].update({'IN': random.randint(1, 4), 'OUT': random.randint(1, 6)})
# # G.add_edges_from(edge_list)
# # G_ = dgl.from_networkx(G)
# # Node_list = G_.nodes()
# # k = 3
# # S = []
# # Node_list_visited = []
# # while len(Node_list) > k:
# #     node = random.choice(Node_list)
# #     if len(G_.out_edges(node)[0])==0:
# #         continue
# #     sg, inverse_indices = dgl.khop_out_subgraph(G_, node, k=k)
# #     print(node)
# #     print(sg.nodes())
# #     print(sg.edges())
# #     S.append(sg)
# #     for s in S:
# #         # print(s.nodes())
# #         # print(s.edges())
# #         Node_list_visited += list(n for n in s.nodes())
# #         # print(Node_list_visited)
# #     Node_list_visited.append(torch.tensor(node))
# #     Node_list = list(n for n in G_.nodes() if n not in Node_list_visited)
# #     if len(list(set(Node_list_visited))) >= len(G.nodes()):
# #         break

# # Partition graph
# Node_list = list(G.nodes())
# k = 3
# S = []
# Nodes_visited = []

# while len(Node_list) > k:
#     node = random.choice(Node_list)
#     Nodes_visited.append(node)
#     if len(G.out_edges(node))==0:
#         continue
#     loads = list(G.successors(node))
#     # loads = list(G.predecessors(node))
#     Nodes_visited += loads
#     sg = set(loads)
#     # # for _ in range(k-1):
#     # for cnode in loads:
#     #     post_loads = list(G.successors(cnode))
#     #     sg += post_loads
#     #     Node_list_visited += post_loads
#     Nodes_visited = list(set(Nodes_visited))
#     S.append(sg)
#     # breakpoint()
#     # print(len(Node_list_visited))
#     Node_list = list(n for n in G.nodes() if n not in Nodes_visited)
#     if len(list(set(Nodes_visited))) >= len(G.nodes()):
#         break

# dS = [S.pop()]
# Nodes_visited = list(dS[0])
# for sg in S:
#     nodes =  list(sg.difference(set(Nodes_visited)))#list(n for n in sg if n not in Nodes_visited)
#     if len(nodes) > 0:
#         dS.append(set(nodes))
#         Nodes_visited += nodes

# # Form subgraphs
# logicG_list = []
# for sg in dS:
# # sg = dS.pop(0)
#     sg_logic = nx.DiGraph()
    
#     # Initiate LUT names
#     for node in sg:
#         inLUTs = G.nodes[node]['IN']
#         pin = 6; random.randint(1, 4)
#         outLUTs = G.nodes[node]['OUT'] // pin
#         outFLOPs = G.nodes[node]['OUT'] % pin
#         G.nodes[node].update({'pins': pin, 'inLUTs_out': list(node+'_inLUT'+str(i+1)+'_out' for i in range(inLUTs)), 
#                               'outLUTs_in': list(node+'_outLUT'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(outLUTs) for j in range(4)),
#                               'inLUTs_in': list(node+'_inLUT'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(inLUTs) for j in range(4)),
#                               'outLUTs_out': list(node+'_outLUT'+str(i+1)+'_out' for i in range(inLUTs)),
#                               'outFFs_in': list(node+'_FF'+str(i+1)+'_out' for i in range(outFLOPs))})
#         # Add nodes to logic graph
#         for lgnode in G.nodes[node]['inLUTs_out']+G.nodes[node]['outLUTs_in']+G.nodes[node]['outFFs_in']:
#             sg_logic.add_node(lgnode)
            
#     # Assign logic graph edges
#     inPins_assigned = []
#     outPins_assigned = []
#     for node in sg:
#         for edge in G.in_edges(node):
#             if edge[0] not in sg:
#                 continue

#             inPins = G.nodes[edge[0]]['inLUTs_out']

#             if len(inPins_assigned)==0:
#                 inPin = random.choice(inPins)
#             elif len([pin for pin in inPins if pin not in inPins_assigned]) == 0:
#                 numPins = len(inPins)
#                 inPin = node+'_LUT_in'+str(numPins+1)
#                 G.nodes[edge[0]]['inLUTs_out'].append(inPin)
#             else:
#                 inPin = random.choice(list(pin for pin in inPins if pin not in inPins_assigned))
#             inPins_assigned.append(inPin)
#             outPins = G.nodes[node]['outLUTs_in']+G.nodes[node]['outFFs_in']
#             # print(g.nodes[int(node)]['outLUTs'])
#             if len(outPins_assigned)==0:
#                 outPin = random.choice(outPins)
#             elif len(list(pin for pin in outPins if pin not in outPins_assigned))==0:
#                 continue
#             else:
#                 outPin = random.choice(list(pin for pin in outPins if pin not in outPins_assigned))
#             outPins_assigned.append(outPin)
#             sg_logic.add_edge(inPin, outPin)
#     logicG_list.append(sg_logic)

# # Compose graph
# logicG = logicG_list.pop(0)
# for sg in logicG_list:
#     logicG = nx.compose(logicG, sg)
# subG = dS
# # Now connect pairs of subgraphs
# k = 0
# for k in range(3):
#     usedLUTs = []
#     visited = []
#     dS_ = []
#     for i, s1 in enumerate(dS):
#         for j, s2 in enumerate(dS):
#             if s1 != s2 and (s1 not in visited and s2 not in visited) :
                
#                 flag = 0
#                 for node1, node2 in list(itertools.product(s1, s2)):
#                     # sg_logic1 = logicG_list[i]
#                     # sg_logic2 = logicG_list[j]
#                     if G.has_edge(node1, node2):
#                         try:
#                             outPin1 = random.choice(list(n for n in G.nodes[node1]['outLUTs_out'] if n not in usedLUTs))
#                             inPin2 = random.choice(list(n for n in G.nodes[node2]['inLUTs_in'] if n not in logicG.nodes()))
#                             inPin2_out = inPin[:-4]+'_out'
#                             usedLUTs.append(inPin2_out)
#                             logicG.add_edge(outPin1, inPin2)
#                             print('Yeah1!')
#                             flag = 1
#                         except:
#                             continue
    
#                     if G.has_edge(node2, node1) and node1!=node2: 
#                         try:
#                             outPin2 = random.choice(list(n for n in G.nodes[node1]['outLUTs_out'] if n not in usedLUTs))
#                             inPin1 = random.choice(list(n for n in G.nodes[node2]['inLUTs_in'] if n not in logicG.nodes()))
#                             inPin1_out = inPin[:-4]+'_out'
#                             usedLUTs.append(inPin1_out)
#                             logicG.add_edge(outPin2, inPin1)
#                             print('Yeah2!')
#                             flag = 1
#                         except:
#                             continue
#                 if flag:
#                     visited.append(s1); visited.append(s2)
#                     dS_.append(set(list(s1)+list(s2)))
#                     print('Done!'+str(k))
#     dS = dS_
    


