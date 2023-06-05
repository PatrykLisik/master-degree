import io
from itertools import permutations, pairwise

import numpy as np
from tqdm import tqdm

if __name__ == '__main__':
    data = np.genfromtxt("./dist_10.txt", delimiter=None, autostrip=True)

    length = len(data[0])
    results_text = {}
    results = {}
    best_order = None
    best_length = np.infty
    # print(f"System file buffer size {io.DEFAULT_BUFFER_SIZE}")
    with open("./tsp_all.txt", "w", buffering=io.DEFAULT_BUFFER_SIZE * 2) as tsp_file:
        for order in tqdm(permutations(range(length), length)):
            order = (*order, order[0])
            road_length = 0
            for point_a, point_b in pairwise(order):
                distance = data[point_a, point_b]
                road_length += distance
            # print(f"{order}:{road_length}", file=tsp_file, flush=False)
            if road_length < best_length:
                best_length = road_length
                best_order = order

        print(f"\n\nBEST order {best_order}", file=tsp_file)
        print(f"BEST road length {best_length}", file=tsp_file)
