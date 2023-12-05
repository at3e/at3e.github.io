---
layout: post
use_math: true
title: On a graph problem
---

Lately, I came across this problem for one of my projects. I will present a simplified version of the problem over here and present an approach to solve it.
Start with a directed graph with nodes shown in blue. A directed graph or a "digraph," is a data structure representation that consists of a set of nodes (or vertices) and a set of directed edges (or arcs) that connect pairs of nodes. Each edge is directed from one node to another that indicates, for example, the direction of propagation of information from a node to the next. A directed acyclic graph(DAG) is a digraph with no directed cycles.

![Image](/assets/Graph/BGraph.001.jpeg){: width="65%" align="center"}

*Figure 1: A DAG G*

Each Blue box is connected to a certain number of elements shown in Red boxes.

![Image](/assets/Graph/BGraph.002.jpeg){: width="65%" align="center"}

*Figure 2: Graph G and G'*

Here’s the problem:  Derive a graph G' of the Red boxes, given the underlying of the Blue box graph. A sample set of edges is shown in Black dotted lines. Specifically, a Red box can talk to another Red box if there exists an edge between their corresponding Blue boxes. But subject to certain constraints.

![Image](/assets/Graph/BGraph.003.jpeg){: width="65%" align="center"}

*Figure 3: Graph G and nodes of graph G'*

Each Red box can have multiple incoming and outgoing edges. But at least one input or output edge must be used. But while constructing the graph `G'`, no set of Red boxes can form a chain of more than N stages. For example, if N=3, an invalid set of edges the set of edges is marked using Red solid lines. Similarly the set of edges marked using Green solid lines connecting a chain of three nodes is valid.

![Image](/assets/Graph/BGraph.004.jpeg){: width="65%" align="center"}

*Figure 4: Set of valid and invalid edges of graph G'*

I worked out an approach to this problem. Let's walk through along with a code. 
First, import the necessary python libraries.

```
import random
import networkx as nx
import numpy as np
random.seed(7)
```

Given a random Directed acyclic graph `G_B` created using the `networkx` package, similar to the DAG G with Blue nodes shown in Figure 1. There are several ways to create a DAG, a simple one can be found <a href="https://gist.github.com/flekschas/0ea70dec4d92bc706e61" rel="noreferrer">here</a> . Red boxes are randomly assigned to each node. These nodes of the graph `G_R` that we want to derive. Let the number of Red nodes assigned to each node of `G_B` be `numR`. In this case I will limit it till 4. These nodes are added to the empty graph `G_R`. Each node of `G_R` has a `score`, initialized to 0. The `score` keeps track of the levels of Red nodes preceeding it.

```
# Initialize G_R
G_R = nx.DiGraph()

for node in G_B.nodes():
    numR = random.randint(1, 4)
    G_B.nodes[node].update({'numR': numR})
    G_B.nodes[node].update({'Rnodes': list(node+'_R'+str(i+1) for i in range(numR))})

    # Add nodes to G_R
    for nodeR in G_B.nodes[node]['Rnodes']:
            G_R.add_node(nodeR)
            G_R.nodes[nodeR].update({'score': 0})
```

We traverse the graph `G_B`, adding edges to `G_R` along the way while also keeping track of the chain length for every node of `G_R`. First we set the maximum length of the chain of Red nodes, `max_length`. Then for node pair `(node0, node1)` in the set of edges of `G_B`, we pick an associated `Rnode0` with score less than `max_length`. It may be the case that no such is avaiable, in which case an new node is added to the graph `G_R`. `Rnode1` randomly selected. Once edge is formed between `Rnode0` and `Rnode1`, the scores of all nodes after `Rnode1` must be updated.
```
max_length = 5

for edge in G_B.edges():
    node0 = edge[0]
    flag = bool(list(n for n in G_B.nodes[node0]['Rnodes'] if G_R.nodes[n]['score']<max_length))
    if flag:
       Rnode0 = random.choice(list(n for n in G_B.nodes[node0]['Rnodes'] if G_R.nodes[n]['score']<max_length))
    else:
       Rnode0 = node+'_R'+str(G_B.nodes[node]['numR']+1)
       G_B.nodes[node]['Rnodes'].append(Rnode0)
       G_R.add_node(Rnode0)
       G_R.nodes[Rnode0].update({'score': 0})
       G_B.nodes[node]['numR'] += 1
       
    node1 = edge[1]
    Rnode1 = random.choice(G_B.nodes[node1]['Rnodes'])
    G_R.add_edge(Rnode0, Rnode1)
    
    # Update graph
    G_R.nodes[Rnode1]['score'] = max(logicG.nodes[Rnode1]['score'], logicG.nodes[Rnode0]['score'] + 1)
    updateNodescores(G_R, Rnode1)

```

The updateNodescores method is a BFS algorithm based routine that updates the node scores of all successors.
```
def updateNodescores(G, node):
    visited = [node]
    q = [node]
    q.append(node)
    while q:
        u = q.pop(0)
        v = list(G.successors(u))
        if not v:
            continue
        else:
            for vnode in v:
                if vnode not in visited:
                    G.nodes[vnode]['score'] = max(G.nodes[vnode]['score'], G.nodes[u]['s']+1)
                    q.append(vnode)
                    visited.append(vnode)
    return
```
This method can be computationally intensive for large graphs. Do let me know if you have suggestions!
![](https://www.youtube.com/watch?v=Ptk_1Dc2iPY)

![](//www.youtube.com/watch?v=Ptk_1Dc2iPY?width=800&height=500)
<video autoplay muted loop>
  <source src="https://github.com/at3e/at3e.github.io/tree/main/assets/Graph/27197181_MotionElements_awkward-dumbfounded-hd.mp4" type="video/mp4">
  <p>Your browser does not support the video element.</p>
</video>
![](https://github.com/at3e/at3e.github.io/tree/main/assets/Graph/27197181_MotionElements_awkward-dumbfounded-hd.mp4)
