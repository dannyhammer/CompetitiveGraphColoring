import networkx as nx

#Creates a new graph named 'G'
G = nx.Graph()

#Add nodes from the range 1 to 3
G.add_nodes_from([1, 3])

#Add edges from the range (1,2) to (1,3)
G.add_edges_from([(1, 2), (1, 3)])


#Prints out the number of nodes in graph G
print("Number of nodes: ")
print(G.number_of_nodes())


#Prints out the number of edges in graph G
print("Number of edges: ")
print(G.number_of_edges())
