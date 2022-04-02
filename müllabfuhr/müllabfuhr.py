import cProfile
from collections import Counter
from functools import lru_cache, reduce
from itertools import combinations
import pstats
from time import time
from bitsets import bitset


class NodeContainer:
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
        self.nodes = {}
        self.edges = set()
        self.edge_bitset = None

    def add_node(self, node_id):
        if node_id not in self.nodes:
            self.nodes[node_id] = NodeContainer(node_id)

    def add_edge(self, start, end, distance):
        self.nodes[start].add_neighbor(end, distance)
        self.nodes[end].add_neighbor(start, distance)
        self.edges.add((start, end))
        self.edges.add((end, start))
        self.edge_bitset = bitset("Edges", tuple(self.edges))

    def get_node(self, node_id):
        return self.nodes[node_id]

    def path_length(self, path_nodes):
        distance = 0
        for i in range(len(path_nodes) - 1):
            distance += self.get_node(path_nodes[i]).get_distance(
                path_nodes[i + 1]
            )
        return distance

    def covers_all_edges(self, paths):
        return (
            self.edges_equal(reduce(set_union, map(lambda x: x.edges, paths)))
            # if len(self.edges) <= sum(len(path.edges) for path in paths)
            # else False
        )

    def edges_equal(self, other_edges):
        return other_edges == self.edge_bitset.supremum


# @lru_cache(200_000)
def set_union(set1, set2):
    return set1.union(set2)


class PathContainer:
    def __init__(self, graph: Graph, nodes: list):
        self.nodes = nodes
        self.graph = graph
        self.length = graph.path_length(self.nodes)
        self.edges = graph.edge_bitset(edges_from_path(self.nodes))

    def __hash__(self):
        return hash(self.nodes)

    def __repr__(self):
        return f"Path{self.nodes}"


def find_new_paths(prime_path, closed_nodes=[]):
    return {
        PathContainer(prime_path.graph, prime_path.nodes + (node,))
        for node in prime_path.graph.get_node(
            prime_path.nodes[-1]
        ).get_neighbors()
        if node not in closed_nodes
    }


def edges_from_path(path):
    edges = set()
    for i in range(len(path) - 1):
        edges.add((path[i], path[i + 1]))
        edges.add((path[i + 1], path[i]))
    return frozenset(edges)


def read_graph(path):
    graph = Graph()
    with open(path) as f:
        f.readline()
        while line := f.readline():
            start, end, distance = line.split(" ")
            graph.add_node(int(start))
            graph.add_node(int(end))
            graph.add_edge(int(start), int(end), int(distance))
    return graph


def main():
    try:
        file_path = input("Pfad: ")
        graph = read_graph(file_path)
        closed_paths = set()
        paths_old = set()
        open_paths = {PathContainer(graph, (0,))}
        loop = True
        while loop:
            prime_path = min(open_paths, key=lambda x: x.length)
            open_paths.remove(prime_path)
            new_paths = find_new_paths(prime_path)
            for new_path in new_paths:
                may_add = True
                for old_path in open_paths | closed_paths | paths_old:
                    if old_path.nodes[-1] == new_path.nodes[-1]:
                        if old_path.length <= new_path.length and (
                            new_path.edges.issubset(old_path.edges)
                        ):
                            may_add = False
                            break
                if new_path.nodes[::-1] in ({p.nodes for p in open_paths} | {p.nodes for p in closed_paths}):
                    may_add = False

                if may_add:
                    open_paths.add(new_path)
            paths_old.add(prime_path)

            if prime_path.nodes[-1] == 0:
                print(len(closed_paths))
                print(len(list(combinations(closed_paths, 4))))
                start_time = time()
                if len(closed_paths) != 0:
                    if graph.covers_all_edges(closed_paths | {prime_path}):
                        for subpaths in combinations(closed_paths, 4):
                            if graph.covers_all_edges(
                                subpaths + (prime_path,)
                            ):
                                print(
                                    tuple(path.nodes for path in subpaths)
                                    + (prime_path.nodes,)
                                )
                                loop = False
                                break

                closed_paths.add(prime_path)
                print(timedelta := (time() - start_time))
                print(
                    timedelta / (len(list(combinations(closed_paths, 4))) or 1)
                )

                closed_paths = set(
                    filter(
                        lambda f: not any(
                            f.edges.issubset(g.edges) and f != g
                            for g in closed_paths
                        ),
                        closed_paths,
                    )
                )

    except KeyboardInterrupt:
        pass


if __name__ == "__main__":

    cProfile.run("main()", "restats")

    p = pstats.Stats("restats")
    p.strip_dirs().sort_stats("time").print_stats(10)
