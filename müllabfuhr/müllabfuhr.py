from dataclasses import dataclass


@dataclass
class Vertex:
    start: int
    end: int
    length: int


class Graph:
    vertices = {}

    def add_half_vertex(self, node1, node2, length):
        if node1 not in self.vertices:
            self.vertices[node1] = []
        self.vertices[node1].append(Vertex(node1, node2, length))

    def add_vertex(self, node1, node2, length):
        self.add_half_vertex(node1, node2, length)
        self.add_half_vertex(node2, node1, length)

    def connected_nodes(self, node):
        return self.vertices[node]

