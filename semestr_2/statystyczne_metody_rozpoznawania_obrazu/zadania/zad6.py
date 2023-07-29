import argparse
import logging

import numpy as np


def euclidean_distance(a, b):
    return np.sum((a - b) ** 2)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        prog='Zadanie 6',
        description='Nearest neighbor classifier',
    )
    parser.add_argument('-trn', '--train_file', required=False)
    parser.add_argument('-tst', '--test_file', required=False)
    parser.add_argument('-o', '--output_file', required=False)

    args = parser.parse_args()

    training_set_file_path = args.train_file or input("Training set file? ")
    testing_set_file_path = args.test_file or input("Testing set file? ")
    output_file_path = args.output_file or input("Output file? ")

    logging.basicConfig(level=logging.INFO,
                        format='%(message)s',
                        filename=output_file_path,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    training_data = np.genfromtxt(training_set_file_path, skip_header=1, dtype=np.float64)

    training_labels = training_data[:, 0].copy().astype(int)
    training_data = np.delete(training_data, 0, 1)

    feature_vector_len = training_data.shape[1] - 1
    training_file_len = training_data.shape[0]
    training_class_count = len(np.unique(training_labels))

    sd = np.std(training_data, axis=0) * np.sqrt(training_data.shape[0])
    mean = np.mean(training_data, axis=0)

    # standardize
    training_data -= mean
    training_data /= sd

    testing_data = np.genfromtxt(testing_set_file_path, skip_header=1, dtype=np.float64)

    # standardize with training params
    testing_labels = testing_data[:, 0].copy().astype(int)
    testing_data = np.delete(testing_data, 0, 1)
    testing_data -= mean
    testing_data /= sd

    confusion_matrix = np.zeros((training_class_count, training_class_count), dtype=int)

    assigned_labels = np.zeros(testing_data.shape[0], dtype=int)

    for testing_index, testing_data_entry in enumerate(testing_data):
        min_distance = np.infty
        assigned_label = None

        for training_index, training_data_entry in enumerate(training_data):
            distance = euclidean_distance(testing_data_entry, training_data_entry)
            if distance <= min_distance:
                min_distance = distance
                assigned_label = training_labels[training_index]

        assigned_labels[testing_index] = assigned_label
        confusion_matrix[testing_labels[testing_index] - 1][assigned_label - 1] += 1

    error_rate = 100 * np.sum(assigned_labels != testing_labels) / len(testing_labels)

    class_counts = np.sum(confusion_matrix, axis=1)
    class_totals = np.sum(confusion_matrix, axis=0)

    prior_probabilities = confusion_matrix / class_counts

    posterior_probabilities = confusion_matrix.T / class_totals



    logging.info(" Results of classification:")

    classification_template = "{:>10} {:>10} {:>10}"
    logging.info(classification_template.format("Nr obj", "Klasa faktyczna", "Klasa przypisana"))
    logging.info(classification_template.format("Object", "True class", "Assigned class"))
    for index, (true_class, assigned_class) in enumerate(zip(testing_labels, assigned_labels)):
        logging.info(classification_template.format(index + 1, true_class, assigned_class))

    logging.info(f"\nError rate {error_rate:.2f}%")

    logging.info("\nConfusion matrix")
    logging.info(np.array2string(confusion_matrix, max_line_width=None))

    logging.info("\nProbabilities a priori: ")
    logging.info(np.array2string(prior_probabilities, max_line_width=None))

    logging.info("\nProbabilities a posteriori:")
    logging.info(np.array2string(posterior_probabilities, max_line_width=None))
