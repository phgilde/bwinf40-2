import cProfile
from collections import Counter
from itertools import combinations
import pstats


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
        self.edges = set()

    def add_vertex(self, vertex_id):
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = Vertex(vertex_id)

    def add_edge(self, start, end, distance):
        self.vertices[start].add_neighbor(end, distance)
        self.vertices[end].add_neighbor(start, distance)
        self.edges.add(frozenset((start, end)))

    def get_vertex(self, vertex_id):
        return self.vertices[vertex_id]

    def path_length(self, path_vertices):
        distance = 0
        for i in range(len(path_vertices) - 1):
            distance += self.get_vertex(path_vertices[i]).get_distance(
                path_vertices[i + 1]
            )
        return distance

    def covers_all_edges(self, paths):
        edges_paths = set()
        for path in paths:
            for i in range(len(path) - 1):
                edges_paths.add(frozenset((path[i], path[i + 1])))

        return edges_paths == self.edges


def shortest_path(graph, start, end):
    closed_nodes = set()
    paths = set((start,))
    while (prime_path := min(paths, key=lambda x: graph.path_distance(x)))[
        -1
    ] != end:
        closed_nodes.add(prime_path[0])
        paths |= find_new_paths(graph, closed_nodes, prime_path)
    return prime_path


def find_new_paths(graph, prime_path, closed_nodes=[]):
    return {
        prime_path + (node,)
        for node in graph.get_vertex(prime_path[-1]).get_neighbors()
        if node not in closed_nodes
    }


def read_graph(path):
    graph = Graph()
    with open(path) as f:
        f.readline()
        while line := f.readline():
            start, end, distance = line.split(" ")
            graph.add_vertex(int(start))
            graph.add_vertex(int(end))
            graph.add_edge(int(start), int(end), int(distance))
    return graph


def main():
    file_path = input("Pfad: ")
    graph = read_graph(file_path)
    closed_paths = set()
    open_paths = {(0,)}
    last_n_closed = len(closed_paths)
    while True:
        prime_path = min(open_paths, key=lambda x: graph.path_length(x))
        open_paths.remove(prime_path)
        if prime_path[-1] == 0:
            closed_paths.add(prime_path)
        new_paths = find_new_paths(graph, prime_path)
        for new_path in new_paths:
            may_add = True
            for found_path in open_paths | closed_paths:
                if found_path[-1] == new_path[-1]:
                    if graph.path_length(found_path) <= graph.path_length(
                        new_path
                    ) and set(new_path) <= set(found_path):
                        may_add = False
                        break

            if may_add:
                open_paths.add(new_path)
        if len(closed_paths) > last_n_closed:
            print(closed_paths)
            last_n_closed = len(closed_paths)
            for combination in combinations(closed_paths, 4):
                if graph.covers_all_edges(combination + (prime_path,)):
                    print(combination + (prime_path,))
                    break
            else:
                continue
            break



if __name__ == "__main__":

    cProfile.run("main()", "restats")

    p = pstats.Stats("restats")
    p.strip_dirs().sort_stats("time").print_stats(10)
