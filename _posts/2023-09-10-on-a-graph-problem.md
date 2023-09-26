---
layout: post
use_math: true
title: On a graph problem
---

Lately, I came across this problem for one of my projects. I will explain in here and present an approach to solve it.
Start with a directed graph with nodes shown in blue. A directed graph or a "digraph," is a data structure representation that consists of a set of nodes (or vertices) and a set of directed edges (or arcs) that connect pairs of nodes. Each edge is directed from one node to another that indicates, for example, the direction of propagation of information from a node to the next. A directed acyclic graph(DAG) is a digraph with no directed cycles.

![Image](/assets/Graph/BGraph.001.jpeg){: width="65%" align="center"}

*Figure 1: A DAG G*

Each Blue box is connected to a certain number of elements shown in Red boxes.

![Image](/assets/Graph/BGraph.002.jpeg){: width="65%" align="center"}

*Figure 2: Graph G and G'*

Here’s the problem:  Derive a graph G' of the Red boxes, given the underlying of the Blue box graph. A sample set of edges is shown in Black dotted lines. Specifically, a Red box can talk to another Red box if there exists an edge between their corresponding Blue boxes. But subject to certain constraints.

![Image](/assets/Graph/BGraph.003.jpeg){: width="65%" align="center"}

*Figure 3: Graph G and nodes of graph G'*

Each Red box can have a maximum of `Ir` incoming edges. There can be multiple outgoing edges. But at least one input or output edge must be used. But while constructing the graph `G'`, no set of Red boxes can form a chain of more than N stages. For example, if N=3, an invalid set of edges the set of edges is marked using Red solid lines. Similarly the set of edges marked using Green solid lines connecting a chain of three nodes is valid.

![Image](/assets/Graph/BGraph.004.jpeg){: width="65%" align="center"}

*Figure 4: Set of valid and invalid edges of graph G'*

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
    G = pickle.load(fp)
for node in G.nodes():
    # G.nodes[node].update({'IN': G.in_degree(node), 'OUT': G.out_degree(node)+1})
    G.nodes[node].update({'IN': random.randint(1, 4), 'OUT': random.randint(1, 6)})
```

Next, the graph G is partitioned into one-hop subgraphs as shown below.

![Image](/assets/Graph/BGraph.005.jpeg){: width="65%" align="center"}

`S` is a list of one-hop disjoints subgraphs `sg`.  

```
# Partition graph
Node_list = list(G.nodes())
k = 3
S = []
Nodes_visited = []

while len(list(set(Nodes_visited))) < len(G.nodes()):
    node = random.choice(Node_list)
    Nodes_visited.append(node)
    if len(G.out_edges(node))==0:
        continue
    loads = list(set(G.successors(node)).difference(set(Nodes_visited)))+[node]
    Nodes_visited += loads
    if len(loads)>0:
        sg = set(loads)
        S.append(sg)
    Node_list = list(n for n in G.nodes() if n not in Nodes_visited)
```
Next, the node attributes of G' are updated. The graph edges are formed 
```
# Form subgraphs
Gp = nx.DiGraph() # Initialize graph G'
for sg in S:
    sg_p = nx.DiGraph()
    # Initiate node names
    for node in sg:
        inRnodes = G.nodes[node]['IN']
        Ir = 6 # Set the maximum number of inputs 
        outRnodes = G.nodes[node]['OUT'] // I_R
        G.nodes[node].update({'I_R': I_R, 'inR_out': list(node+'_inR'+str(i+1)+'_out' for i in range(I_R)),
                              'outR_in': list(node+'_outR'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(outRnodes) for j in range(4)),
                              'inR_in': list(node+'_inR'+str(i+1)+'_in'+ '['+str(j)+']' for i in range(inRnodes) for j in range(4)),
                              'outR_out': list(node+'_outR'+str(i+1)+'_out' for i in range(inRnodes))})
        # Add nodes to G'
        for gpnode in G.nodes[node]['inR_out']+G.nodes[node]['outR_in']+G.nodes[node]['inR_in']+G.nodes[node]['outR_out']:
            sg_p.add_node(gpnode)

        # Assign graph edges
        inNodes_assigned = []
        outNodes_assigned = []
        for node in sg:
            for edge in G.in_edges(node):
                if edge[0] not in sg:
                    continue
                inNodes = G.nodes[edge[0]]['inR_out']

                if len(inNodes_assigned)==0:
                    inNode = random.choice(inNodes)
                elif len([n for n in inNodes if n not in inNodes_assigned]) == 0:
                    numNodes = len(inNodes)
                    inNodes = 'N'+str(node)+'_R_in'+str(numNodes+1)
                    G.nodes[edge[0]]['inR_out'].append(inNode)
                else:
                    inNode = random.choice(list(e for e in inNodes if e not in inNodes_assigned))
                inNodes_assigned.append(inNode)
                outNodes = G.nodes[node]['outR_in']
                if len(outNodes_assigned)==0:
                    outNode = random.choice(outNodes)
                elif len(list(n for n in outNodes if n not in outNodes_assigned))==0:
                    continue
                else:
                    outNode = random.choice(list(n for n in outNodes if n not in outNodes_assigned))
                outNodes_assigned.append(outNode)
                sg_p.add_edge(inNode, outNode)
        Gp = nx.compose(Gp, sg_p)
```
Now comes the interesting part. The subgraphs are now merged in pairs, making sure the same node is not used in any iterations.

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
