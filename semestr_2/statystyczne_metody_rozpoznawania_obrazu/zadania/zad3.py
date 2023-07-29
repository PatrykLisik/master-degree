import argparse
import logging
from itertools import cycle

import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Zadanie 3',
        description=' Error correction algorithm.',
    )
    parser.add_argument('-trn', '--train_file', required=False, help='Training set file')
    parser.add_argument('-cls', '--classes', required=False, nargs="+", type=int)
    parser.add_argument('-i', '--max_iter_count', required=False, type=int, help='Maximum number of iterations')
    parser.add_argument('-o', '--output_file', help='Output file')

    args = parser.parse_args()

    training_filename = args.train_file or input("Training set file? ")
    class_1, class_2 = args.classes or map(int, input("Pair of classes? ").split(" "))
    max_iter_count = args.max_iter_count or int(input("Maximum naumber of iteration? "))
    output_file = args.output_file or input("Output file? ")

    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        filename=args.output_file,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info("\nError correction algorithm.")



    train_data = np.genfromtxt(training_filename, skip_header=1, dtype=np.float64)

    # remove row with class not consider in trainning
    train_data = np.delete(train_data,
                           np.where((train_data[:, 0] != class_2) & (train_data[:, 0] != class_1)),
                           axis=0)
    original_train_data = train_data.copy()

    # Replace classes with 1 and -1
    class_1_mask = train_data[:, 0] == class_2

    train_data[class_1_mask] *= -1
    train_data[:, 0][class_1_mask] = -1

    train_data[:, 0][train_data[:, 0] == class_1] = 1
    train_data = np.roll(train_data, -1, axis=1)

    num_labeled_samples = train_data.shape[0]

    iteration_without_change = 0
    current_index = 0
    num_corrections = 0
    max_correct_decisions = 0

    current_weighs = np.zeros(train_data.shape[1], dtype=np.float64)
    best_weight = current_weighs.copy()

    for current_data in cycle(train_data):
        if iteration_without_change == num_labeled_samples or num_corrections == max_iter_count:
            break
        iteration_without_change += 1

        if current_index >= num_labeled_samples:
            current_index -= num_labeled_samples

        if np.dot(current_weighs, current_data) <= 0.0:
            iteration_without_change = 0
            num_corrections += 1
            current_weighs += current_data

            current_correct_decisions = 0
            for data in train_data:
                if np.dot(current_weighs, data) > 0.0:
                    current_correct_decisions += 1
            if current_correct_decisions > max_correct_decisions:
                max_correct_decisions = current_correct_decisions
                best_weight = current_weighs.copy()
        current_index += 1

    logging.info(f"\nNumber of correct decisions: {max_correct_decisions}")
    logging.info(f"Training set size: {num_labeled_samples}")
    logging.info(f"Number of corrections: {num_corrections}")
    logging.info("\nBest weights:")
    for index, weight in enumerate(best_weight):
        logging.info(f"{index + 1:4} {weight:12.4f}")
