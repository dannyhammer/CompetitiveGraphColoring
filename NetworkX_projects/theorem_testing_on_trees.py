# Daniel Hammer

# CURRENTLY DOES NOT WORK AS INTENDED

# Imports the required networkx packages
import networkx as nx
import random as r


# Generates random integer to build a random graph
vtx = r.randint(2, 7)
print("Generating a random integer: " + str(vtx))

# Creates a random tree graph named 'G'
G = nx.random_tree(vtx)

# Creates lists to reference the nodes and edges in 'G'
nodes = list(G.nodes)
edges = list(G.edges)

# Lists all of the nodes in 'G'
print("\nList of nodes in G")
print(nodes)


# Lists all of the edges in 'G'
print("\nList of edges in G")
print(edges)


# Lists the adjacent nodes for every node in 'G'
print("\nList of adjacent nodes in G")
for node in nodes:
    print("Node " + str(node) + " is adjacent to node " + str(list(G.adj[node])))


# Lists the degree of every node in 'G'
print("\nList of the degrees of every node in G")
for node in nodes:
    print("The degree of node #" + str(node) + " is " + str(G.degree[node]))

# Displays the diameter of graph 'G'
print("\nDiameter of G is: " + str(nx.diameter(G)))

# Displays a subgraph of graph 'G'
print("\nA subgraph of 'G' is " + str(nx.subgraph(G, None)))

# Displays the distance between two vertices
print("\nThe distance between vertex " + str(nodes[0]) + " and " + str(nodes[-1]) + " is ")
#print(nx.resistance_distance(G, nodes[0], nodes[-1]))
print(nx.resistance_distance(G, 0, 1))
print(nx.distance(G, node[0], node[-1]))
