import cProfile
from collections import Counter
from functools import lru_cache, reduce
from itertools import combinations
import pstats
from time import time
from bitsets import bitset
from utils import read_graph, PathContainer, find_new_paths


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
                        print("buh")
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
