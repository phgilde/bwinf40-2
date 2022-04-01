from collections import Counter


class Vertex:
    def __init__(self, id: int):
        self.id = id
        self.neighbour_distances = {}

    def add_neighbor(self, neighbor_id: int, distance: int):
        self.neighbour_distances[neighbor_id] = distance

    def get_neighbors(self) -> list:
        return self.neighbour_distances.keys()

    def get_distance(self, neighbor_id: int) -> int:
        return self.neighbour_distances[neighbor_id]

    def get_id(self) -> int:
        return self.id


class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        self.vertices[vertex_id] = Vertex(vertex_id)

    def add_edge(self, start, end, distance):
        self.vertices[start].add_neighbor(end, distance)
        self.vertices[end].add_neighbor(start, distance)

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]

    def path_distance(self, path_vertices):
        distance = 0
        for i in range(len(path_vertices) - 1):
            distance += self.get_vertex(path_vertices[i]).get_distance(
                path_vertices[i + 1]
            )
        return distance


def shortest_path(graph, start, end):
    closed_nodes = []
    paths = [[start]]
    while (prime_path := min(paths, key=lambda x: graph.path_distance(x)))[
        -1
    ] != end:
        closed_nodes.append(prime_path[0])
        paths += [
            prime_path + [node]
            for node in graph.get_vertex(prime_path[-1]).get_neighbors()
            if node not in closed_nodes
        ]
    return prime_path


def read_graph(path):
    graph = Graph()
    with open(path) as f:
        f.readline()
        while line := f.readline():
            start, end, distance = line.split(" ")
            graph.add_vertex(int(start))
            graph.add_vertex(int(end))
            graph.add_edge(start, end, distance)
    return graph


def main():
    path = input("Pfad: ")
    graph = read_graph(path)
