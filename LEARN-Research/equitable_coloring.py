# Daniel Hammer


# Import the necessary package
import networkx as nx

n = 4

#def graph_caller(self, graph_name):
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
#    return switcher.get(graph_name,"Invalid choice")


graph_name = input("Enter a graph name to generate\n")
print(graph_name)

#G = graph_caller(graph_name)
G = switcher.get(graph_name)

for k in range(3,11):
    for x in range(3,11):
        #greedy_coloring = nx.coloring.greedy_color(G, strategy='largest_first')
        #greedy_coloring = nx.coloring.equitable_color(G, num_colors=x)
        print("\nNumber of vertices in graph G: " + str(k))
        print("Number of colors used: " + str(max(greedy_coloring.values()) + 1))
