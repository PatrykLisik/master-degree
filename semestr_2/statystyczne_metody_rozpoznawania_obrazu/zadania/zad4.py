import argparse
import logging

import numpy as np


def get_plane_equation(start_point, normal_vector):
    def plane_equation(point):
        return np.inner(normal_vector, point - start_point)

    return plane_equation


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='Zadanie 4',
        description='Training set editing for linear separability.',
    )
    parser.add_argument('-trn', '--train_file', required=True, help='Training set file')
    parser.add_argument('-cls', '--classes', required=True, nargs="+", type=int)
    parser.add_argument('-o', '--output_file', default="zad4_out.txt", help='Output file')

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        filename=args.output_file,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    logging.info("Training set editing for linear separability.\n")

    train_data = np.genfromtxt(args.train_file, skip_header=1, dtype=np.float64)

    class_1, class_2 = args.classes

    class_1_data = train_data[train_data[:, 0] == class_1][:, 1:]
    class_2_data = train_data[train_data[:, 0] == class_2][:, 1:]
    a = np.mean(class_1_data, axis=0)
    b = np.mean(class_2_data, axis=0)
    plane_vec = a - b

    gb = get_plane_equation(b, plane_vec)
    eps = 10 ** (-5)

    max_iter_count = 10 ** 10

    removed = []

    for run_index in range(1, max_iter_count):

        c = min(class_1_data, key=gb)
        d = max(class_2_data, key=gb)
        gc = get_plane_equation(c, plane_vec)
        gd = get_plane_equation(d, plane_vec)

        l1 = np.sum(gd(class_1_data) <= eps)
        l2 = np.sum(gc(class_2_data) >= -eps)

        index_c = np.flatnonzero(np.all((class_1_data == c), axis=1))[0]
        index_d = np.flatnonzero(np.all((class_2_data == d), axis=1))[0]

        print_index_c = np.flatnonzero(np.all((train_data[:, 1:] == c), axis=1))[0] + 1
        print_index_d = np.flatnonzero(np.all((train_data[:, 1:] == d), axis=1))[0] + 1

        logging.info(f"Run number {run_index}:  Extreme objects:   {print_index_c} and   {print_index_d}")
        logging.info(f"from the classes {class_1} and {class_2} respectively")
        logging.info(f" l1 = {l1}   l2 = {l2}")

        if gb(c) > gb(d):
            def hx(x):
                return gc(x) + gd(x)


            logging.info("No objects rejected. Success.")
            break

        if l1 < l2:
            class_1_data = np.delete(class_1_data, index_c, axis=0)
            logging.info(f"Rejected object nr   {print_index_c} from the class  {class_1}")
            removed.append([print_index_c, class_1])
        if l1 > l2:
            class_2_data = np.delete(class_2_data, index_d, axis=0)
            logging.info(f"Rejected object nr   {print_index_d} from the class  {class_2}")
            removed.append([print_index_d, class_2])
        if l1 == l2:
            class_1_data = np.delete(class_1_data, index_c, axis=0)
            class_2_data = np.delete(class_2_data, index_d, axis=0)
            logging.info(f"Rejected object nr   {print_index_c} from the class  {class_1}")
            logging.info(f"Rejected object nr   {print_index_d} from the class  {class_2}")
            removed.append([print_index_c, class_1])
            removed.append([print_index_d, class_2])
        logging.info("")
    logging.info("\nRemoved objects:")
    logging.info(f"{'Object':>10}{'class':>10}")
    for object_print_index, object_class in removed:
        logging.info(f"{object_print_index:>10}{object_class:>10}")

    logging.info("\nMisclassified objects from the selected class pair:")
    logging.info(f" {'Object':>20}{'True class':>20}{'Assigned class':>20}")
    for index, point in enumerate(train_data):
        if (hx(point[1:]) > 0 and point[0] == class_2):
            logging.info(f" {index + 1:>20}{class_2:>20}{class_1:>20}")
        if (hx(point[1:]) < 0 and point[0] == class_1):
            logging.info(f" {index + 1:>20}{class_1:>20}{class_2:>20}")
