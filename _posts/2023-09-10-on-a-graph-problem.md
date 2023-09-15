---
layout: post
use_math: true
title: On a graph problem
---

Lately, I came across this problem for one of my projects. I will explain in here and present an approach to solve it.
Start with a directed graph with nodes shown in blue.
![Image](/assets/BGraph.svg){: style="float: left" width="50%"}
```
import random
import networkx as nx
import numpy as np
import torch
import pickle
import itertools
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np
random.seed(7)
```
with open('sample_graph.dat', 'rb') as fp:
    g = pickle.load(fp)

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

for node in g.nodes():
    # g.nodes[node].update({'IN': g.in_degree(node), 'OUT': g.out_degree(node)+1})
    g.nodes[node].update({'IN': random.randint(1, 4), 'OUT': random.randint(1, 6)})

# Form subgraphs
logicG = nx.DiGraph()
logicG_list = []
for sg in S:
    sg_logic = nx.DiGraph()

    # Initiate LUT names
    for node in sg:
        inLUTs = g.nodes[node]['IN']
        pin = 6; random.randint(1, 4)
        outLUTs = g.nodes[node]['OUT'] // pin
        outFLOPs = g.nodes[node]['OUT'] % pin
        g.nodes[node].update({'pins': pin, 'inLUTs_out': list(node+'_inLUT'+str(i+1)+'_out' for i in range(inLUTs)),
                              'outLUTs_in': list(node+'_outLUT'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(outLUTs) for j in range(4)),
                              'inLUTs_in': list(node+'_inLUT'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(inLUTs) for j in range(4)),
                              'outLUTs_out': list(node+'_outLUT'+str(i+1)+'_out' for i in range(inLUTs))})
        # Add nodes to logic graph
        for lgnode in g.nodes[node]['LUTs_out']+g.nodes[node]['LUTs_in']+g.nodes[node]['FFs_in']:
            sg_logic.add_node(lgnode)

        # Assign logic graph edges
        inPins_assigned = []
        outPins_assigned = []
        for node in sg:
            for edge in g.in_edges(node):
                if edge[0] not in sg:
                    continue

                inPins = g.nodes[edge[0]]['inLUTs_out']

                if len(inPins_assigned)==0:
                    inPin = random.choice(inPins)
                elif len([pin for pin in inPins if pin not in inPins_assigned]) == 0:
                    numPins = len(inPins)
                    inPin = 'N'+str(node)+'_LUT_in'+str(numPins+1)
                    g.nodes[edge[0]]['inLUTs_out'].append(inPin)
                else:
                    inPin = random.choice(list(pin for pin in inPins if pin not in inPins_assigned))
                inPins_assigned.append(inPin)
                outPins = g.nodes[node]['outLUTs_in']
                # print(g.nodes[int(node)]['outLUTs'])
                if len(outPins_assigned)==0:
                    outPin = random.choice(outPins)
                elif len(list(pin for pin in outPins if pin not in outPins_assigned))==0:
                    continue
                else:
                    outPin = random.choice(list(pin for pin in outPins if pin not in outPins_assigned))
                outPins_assigned.append(outPin)
                sg_logic.add_edge(inPin, outPin)
        logicG_list.append(sg_logic)
        logicG = nx.compose(logicG, sg_logic)

subG = S
# Now connect pairs of subgraphs
k = 0
for k in range(3):
    usedLUTs = []
    visited = []
    dS_ = []
    for i, s1 in enumerate(S):
        for j, s2 in enumerate(S):
            if s1 != s2 and (s1 not in visited and s2 not in visited) :

                flag = 0
                for node1, node2 in list(itertools.product(s1, s2)):
                    if g.has_edge(node1, node2):
                        try:
                            outPin1 = random.choice(list(n for n in g.nodes[node1]['outLUTs_out'] if n not in usedLUTs))
                            inPin2 = random.choice(list(n for n in g.nodes[node2]['inLUTs_in'] if n not in logicG.nodes()))
                            inPin2_out = inPin[:-4]+'_out'
                            usedLUTs.append(inPin2_out)
                            logicG.add_edge(outPin1, inPin2)
                            flag = 1
                        except:
                            continue

                    if g.has_edge(node2, node1) and node1!=node2:
                        try:
                            outPin2 = random.choice(list(n for n in g.nodes[node1]['outLUTs_out'] if n not in usedLUTs))
                            inPin1 = random.choice(list(n for n in g.nodes[node2]['inLUTs_in'] if n not in logicG.nodes()))
                            inPin1_out = inPin[:-4]+'_out'
                            usedLUTs.append(inPin1_out)
                            logicG.add_edge(outPin2, inPin1)
                            flag = 1
                        except:
                            continue
                if flag:
                    visited.append(s1); visited.append(s2)
                    dS_.append(set(list(s1)+list(s2)))
    dS = dS_