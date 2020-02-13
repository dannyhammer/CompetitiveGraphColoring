# Daniel Hammer

# Imports the required networkx packages
import networkx as nx


# Prompts the user for the number of vertices to be in 'G'
vtx = int(input("Enter a number of vertices for this graph: "))


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
