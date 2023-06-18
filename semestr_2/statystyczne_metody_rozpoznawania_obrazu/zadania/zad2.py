import argparse
import logging

import numpy as np


def distance(a, b):
    return np.sum((a - b) ** 2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Zadanie 2',
        description='Maszyna linowa',
    )
    parser.add_argument('-trn', '--train_file', required=True)
    parser.add_argument('-tst', '--test_file', required=True)
    parser.add_argument('-o', '--output_file', default="zad2_out.txt")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        filename=args.output_file,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    train_file_path = args.train_file
    test_file_path = args.test_file

    train_data = np.genfromtxt(train_file_path, skip_header=1, dtype=np.float64)
    test_data = np.genfromtxt(test_file_path, skip_header=1,dtype=np.float64)

    classes = np.unique(train_data[:, 0])

    gravity_centers = []
    for class_ in classes:
        # mask class data
        class_data = train_data[train_data[:, 0] == class_]
        # remove class column
        class_data = class_data[:, 1:]
        # mean by column
        class_gravity_centers = np.mean(class_data, axis=0)
        gravity_centers.append(class_gravity_centers)
    gravity_centers = np.array(gravity_centers)
    logging.info(f"Class gravity centers before standardisation:\n{gravity_centers}")

    mv = np.mean(train_data[:, 1:], axis=0)
    sd = np.std(train_data[:, 1:], axis=0, ddof=0)

    gravity_centers_std = (gravity_centers - mv) / sd
    logging.info(f"\nClass gravity centers after standardisation:\n{gravity_centers_std}")

    weigths = gravity_centers_std * 2
    bias = -np.sum(gravity_centers_std ** 2, axis=1)

    logging.info(f"\nWeights before including standardisation:\n{np.column_stack([weigths, bias])}" )

    weigths_std = weigths / sd
    bias_std = bias - np.sum((weigths_std * mv), axis=1)

    logging.info(f"\nWeights with included standardisation:\n{np.column_stack([weigths_std, bias_std])}")

    distance_tab = []
    for data_row in test_data[:, 1:]:
        distances = []
        for weigth, b in zip(weigths_std, bias_std):
            g = np.sum(data_row * weigth) + b
            distances.append(g)
        distance_tab.append(distances)
    distance_tab = np.array(distance_tab)

    mins = np.argmax(distance_tab, axis=1) + 1

    correct_count = np.sum(mins == test_data[:, 0])

    incorrect_count = np.sum(mins != test_data[:, 0])
    logging.info("\nResults of classification:")
    logging.info(f"{'Nr obj':^15},\t{'Klasa faktyczna':^15},\t{'Klasa przypisana':^15}")
    logging.info(f"{'Object':^15},\t{'True class':^15},\t{'Assigned class':^15}")
    for index, (true_class, assigned_class) in enumerate(zip(test_data[:, 0], mins)):
        logging.info(f"{index+1:^15} \t{true_class:^15} \t{assigned_class:^15}")

    logging.info(f"Error rate {(incorrect_count / len(train_data)) * 100:.2f}%")
