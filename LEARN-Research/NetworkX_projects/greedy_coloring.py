# Daniel Hammer


# Import the necessary package
import networkx as nx

# Determines what kind of graph to make, given a name and # of vertices
def make_graph(g_name, n):
    switcher = {
        "path": nx.path_graph(n),
        "complete": nx.complete_graph(n),
        "binomial tree": nx.binomial_tree(n),
        "circular ladder": nx.circular_ladder_graph(n),
        "cycle": nx.cycle_graph(n),
        "dorogovtsev": nx.dorogovtsev_goltsev_mendes_graph(n),
        "ladder": nx.ladder_graph(n),
        "star": nx.star_graph(n),
        "wheel": nx.wheel_graph(n),
        "margulis gabber galil": nx.margulis_gabber_galil_graph(n),
        "chordal cycle": nx.chordal_cycle_graph(n),
        "hypercube": nx.hypercube_graph(n),
        "mycielski": nx.mycielski_graph(n)
        }
    return switcher.get(g_name)


# Asks for a graph name, used to make a graph
graph_name = input("Enter a graph name to generate\n")


# For every value between 2-10, make a new graph with the given name
for k in range(2,11):

    # Make a graph with the specified name and k number of vertices
    G = make_graph(graph_name, k)

    # Colors the graph using the 'largest first' strategy
    greedy_coloring = nx.coloring.greedy_color(G, strategy='largest_first')

    # Prints the number of vertices and the number of colors used
    print("\nNumber of vertices in graph G: " + str(k))
    print("Number of colors used: " + str(max(greedy_coloring.values()) + 1))

    # Sorts the vertices and their assigned color
    for i in sorted (greedy_coloring.keys()):
        print("Vtx " + str(i) + " | clr #" + str(greedy_coloring.get(i)))
