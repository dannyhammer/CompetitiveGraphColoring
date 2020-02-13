# Daniel Hammer


# Import the necessary package
import networkx as nx

# Loop through the the values for a graph with 2 vertices up to 20 vertices
for k in range(2,21):
    
    # Create a new path with K number of verticies
    path_k = nx.path_graph(k)

    # Color the graph with the greedy coloring using the largest-first strategy
    greedy_coloring = nx.coloring.greedy_color(path_k, strategy='largest_first')

    # Print out the number of vertices to make visualization of results easier
    print("\nNumber of vertices in path k " + str(k))

    # Displays the number of colors used to color the path
    print("Number of colors used " + str(max(greedy_coloring.values()) + 1))
