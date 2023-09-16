---
layout: post
use_math: true
title: On a graph problem
---

Lately, I came across this problem for one of my projects. I will explain in here and present an approach to solve it.
Start with a directed graph with nodes shown in blue.

![Image](/assets/Graph/BGraph.001.jpeg){: width="50%"}
*Figure 1: A directed graph `G`*

Each Blue box is connected to a certain number of elements shown in Red boxes.

![Image](/assets/Graph/BGraph.002.jpeg){: width="50%" align="center"}
*Figure 2: Graph `G` and `G'`*

Here’s the problem:  Derive a graph `G'` of the Red boxes, given the underlying of the Blue box graph. A sample set of edges is shown in Black dotted lines. Specifically, a Red box can talk to another Red box if there exists an edge between their corresponding Blue boxes. But subject to certain constraints.

![Image](/assets/Graph/BGraph.003.jpeg){: width="50%" align="center"}
*Figure 3: Graph `G` and nodes of graph `G'`*

Each Red box can have a maximum of I_R incoming edges. There can be multiple outgoing edges. But at least one input or output edge must be used. But while constructing the graph `G'`, no set of Red boxes can form a chain of more than N stages. For example, if N=3, the set of Red boxes connected using Red dotted lines is invalid, but the set of Red boxes connected using Green dotted lines works.

![Image](/assets/Graph/BGraph.004.jpeg){: width="50%" align="center"}
*Figure 4: Set of valid and invalid edges of graph `G'`*

I worked out an approach to this problem. Let's walk through with a code. 
First, import the necessary python libraries.

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

I have sample graph of 100 nodes, similar to the one shown earlier. Red boxes are randomly assigned to each node and are divided into two groups 'IN' and 'OUT'. These nodes of the graph that we want to derive.
```
with open('sample_graph.dat', 'rb') as fp:
    g = pickle.load(fp)
for node in g.nodes():
    # g.nodes[node].update({'IN': g.in_degree(node), 'OUT': g.out_degree(node)+1})
    g.nodes[node].update({'IN': random.randint(1, 4), 'OUT': random.randint(1, 6)})
```

Next, the graph `G` is partitioned into one-hop subgraphs as shown below.

![Image](/assets/Graph/BGraph.005.jpeg){: width="50%" align="center"}

S is a list of one-hop disjoints subgraphs sg.  

```
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
```

```
# Form subgraphs
logicG = nx.DiGraph()
logicG_list = []
for sg in S:
    sg_logic = nx.DiGraph()
    # Initiate node names
    for node in sg:
        inRnodes = g.nodes[node]['IN']
        I_R = 6; random.randint(1, 4)
        outRnodes = g.nodes[node]['OUT'] // I_R
        g.nodes[node].update({'I_R': I_R, 'inR_out': list(node+'_inR'+str(i+1)+'_out' for i in range(inR)),
                              'outR_in': list(node+'_outR'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(outRnodes) for j in range(4)),
                              'inR_in': list(node+'_inR'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(inRnodes) for j in range(4)),
                              'outLUTs_out': list(node+'_outLUT'+str(i+1)+'_out' for i in range(inRnodes))})
        # Add nodes to G'
        for lgnode in g.nodes[node]['inR_out']+g.nodes[node]['outR_in']+g.nodes[node]['inR_in']+g.nodes[node]['outR_out']:
            sg_logic.add_node(lgnode)

        # Assign graph edges
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
```
```
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
```
