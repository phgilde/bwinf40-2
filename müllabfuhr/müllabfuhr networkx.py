import networkx as nx
import matplotlib.pyplot as plt


graph = nx.Graph()
path = input("Pfad: ")
with open(path) as f:
    n_nodes, n_edges = f.readline().split(" ")
    graph.add_nodes_from(range(int(n_nodes)))
    while line := f.readline():
        node1, node2, dist = line.split(" ")
        graph.add_edge(int(node1), int(node2), weight=int(dist))


pos = nx.spring_layout(graph)
nx.draw(graph, node_size=5)
plt.show()
