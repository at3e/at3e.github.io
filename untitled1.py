# -*- coding: utf-8 -*-
"""
Created on Thu Sep 14 12:10:16 2023

@author: atreyees
"""

import networkx as nx
import random
import pickle
import matplotlib.pyplot as plt

# Create an empty directed graph
G = nx.DiGraph()

# Add nodes to the graph
num_nodes = 100
G.add_nodes_from(range(num_nodes))

# Create at least one incoming or outgoing edge for each node
for node in G.nodes():
    # Generate a random number of outgoing edges (at least 1)
    num_outgoing_edges = random.randint(1, min(5, num_nodes - 1))  # Ensure max 10 outgoing edges
    # Generate a random set of destination nodes for outgoing edges
    outgoing_edges = random.sample(range(num_nodes), num_outgoing_edges)
    for dest_node in outgoing_edges:
        if dest_node != node:
            G.add_edge(node, dest_node)

# Add additional random edges until reaching the desired total number of edges
desired_num_edges = 200
current_num_edges = G.number_of_edges()

while current_num_edges < desired_num_edges:
    source_node = random.randint(0, num_nodes - 1)
    dest_node = random.randint(0, num_nodes - 1)
    if source_node != dest_node and not G.has_edge(source_node, dest_node):
        G.add_edge(source_node, dest_node)
        current_num_edges += 1

print(f"Number of nodes: {num_nodes}")
print(f"Number of edges: {G.number_of_edges()}")

# Now G is your directed random graph with 5000 nodes and 2000 edges
with open('sample_graph.dat', 'wb') as fp:
    pickle.dump(G, fp)

# # Create a sample graph
# G = nx.DiGraph()
# G.add_edges_from([(1, 2), (2, 3), (3, 1), (2, 4), (4, 5)])

# Create a layout for our nodes 
# layout = nx.spring_layout(G)
plt.figure(figsize=(15,15))
# Draw the graph
nx.draw(G, node_color='skyblue', node_size=800, font_size=10, font_color='black', font_weight='bold', edge_color='gray', width=1.0, arrows=True)

# Show the plot
plt.show()
