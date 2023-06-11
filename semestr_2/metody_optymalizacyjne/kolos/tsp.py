from itertools import permutations, tee

import numpy as np


def pairwise(iterable):
    # pairwise('ABCDEFG') --> AB BC CD DE EF FG
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)


if __name__ == '__main__':
    data = np.genfromtxt("./dist_10.txt", delimiter=None, autostrip=True)

    length = len(data[0])
    results_text = {}
    results = {}
    best_order = None
    best_length = np.infty
    # print(f"System file buffer size {io.DEFAULT_BUFFER_SIZE}")
    with open("./tsp_all.txt", "a") as tsp_file:
        for order in permutations(range(length), length):
            order = [*order, order[0]]
            road_length = 0
            for point_a, point_b in pairwise(order):
                distance = data[point_a, point_b]
                road_length += distance
            print(f"{order}:{road_length}", file=tsp_file, flush=False)
            if road_length < best_length:
                best_length = road_length
                best_order = order

        print(f"\n\nBEST order {best_order}", file=tsp_file)
        print(f"BEST road length {best_length}", file=tsp_file)
