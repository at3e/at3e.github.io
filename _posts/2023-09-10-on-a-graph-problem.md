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

Given a random Directed acyclic graph `G` (there are several ways to create a DAG, a simple one can be found [here]({% post_url https://gist.github.com/flekschas/0ea70dec4d92bc706e61 %})similar to the one shown earlier. Red boxes are randomly assigned to each node and are divided into two groups 'IN' and 'OUT'. These nodes of the graph that we want to derive.
```
for node in G.nodes():
    # G.nodes[node].update({'IN': G.in_degree(node), 'OUT': G.out_degree(node)+1})
    G.nodes[node].update({'IN': random.randint(1, 4), 'OUT': random.randint(1, 6)})
```


We traverse the graph `G`, adding edges to `G_R` along the way while also keeping track of the chain length for every node of `G'`. 
```
for edge in G.edges():
	node0 = edge[0]
	Rnode0_out = random.choice(list(n for n in G.nodes[node0]['inR_out'] if logicG.nodes[n]['s']<max_length)+
	                       list(n for n in G.nodes[node0]['outR_out'] if logicG.nodes[n]['s']<max_length))
	node1 = edge[1]
    Rnode1_in = random.choice(list(n for n in G.nodes[node1]['inR_in'] if logicG.nodes[n]['s']==0)+
                          list(n for n in G.nodes[node1]['outR_in'] if logicG.nodes[n]['s']==0))

    name = Rnode1_in.split('_')
    Rnode1_out = '_'.join(name[:-1]) + '_outR'
    logicG.add_edge(outPin, inPin)
    
    # Update graph
    logicG.nodes[Rnode1_out]['s'] = max(logicG.nodes[Rnode1_out]['s'], logicG.nodes[Rnode0_out]['s'] + 1)

    updateNodescores(G_R, Rnode1_out)
    
    G_R.nodes[Rnode1_in]['s'] = logicG.nodes[Rnode1_in]['s'] + 1
```

The updateNodescores method is a BFS algorithm that updates the node scores of all successors at every iteration,
```
def updateNodescores(G, node):
    visited = [node]
    q = [node]
    q.append(node)
    while q:
        u = q.pop(0)
        vnodes_in = list(G.successors(u))
        if not vnodes_in:
            continue
        else:
            
            for vnode in vnodes_in:
                print(u, G.nodes[u]['s'], list(G.successors(u)))
                vnode_out = '_'.join(vnode.split('_')[:-1])+"_out"
                visited.append(vnode_out)
                if vnode_out not in visited and 'LUT' in vnode_out:
                    G.nodes[vnode_out]['s'] = max(G.nodes[vnode_out]['s'], G.nodes[u]['s']+1)
                    q.append(vnode_out)
    return
```
