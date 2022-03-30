from dataclasses import dataclass
from collections import Counter


@dataclass
class Vertex:
    start: int
    end: int
    length: int


class Graph:
    _vertices = {}
    _distances = {}

    def _add_half_vertex(self, node1, node2, length):
        if node1 not in self._vertices:
            self._vertices[node1] = []
        self._vertices[node1].append(Vertex(node1, node2, length))

    def add_vertex(self, node1, node2, length):
        self._add_half_vertex(node1, node2, length)
        self._add_half_vertex(node2, node1, length)
        self._distances[(node1, node2)] = length
        self._distances[(node2, node1)] = length

    def connected_vertices(self, node):
        return self._vertices[node]

    def get_distance(self, node1, node2) -> int:
        return self._distances[(node1, node2)]

    def path_length(self, path: list) -> int:
        total = 0
        for i in range(len(path) - 1):
            total += self.get_distance(path[i], path[i + 1])
        return total


def shortest_path(graph, start, end):
    paths = [start]
    while (prime_path := min(paths, key=lambda x: graph.path_length(x)))[
        -1
    ] != end:
        paths.remove(prime_path)
        paths += [
            prime_path + [new_vertex]
            for new_vertex in graph.connected_nodes(prime_path[-1])
        ]
    return prime_path

