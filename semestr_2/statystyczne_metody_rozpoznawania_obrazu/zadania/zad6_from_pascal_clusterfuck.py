import numpy as np

num_classes = 10
num_features = 600
max_objects = 10000

training_set_file_path = "../data/epj_trn.txt"
testing_set_file_path = "../data/epj_tst.txt"
output_file_path = "zad6.txt"

testing_file = open(testing_set_file_path, 'r')
output_file = open(output_file_path, 'w')

training_data = [[0.0] * num_features for _ in range(max_objects)]
testing_data = [0.0] * num_features
training_labels = [0] * max_objects
true_labels = [0] * num_features
assigned_labels = [0] * num_features
mean_values = [0.0] * num_features
sd = [0.0] * num_features
prior_probabilities = [[0.0] * num_classes for _ in range(num_classes)]
posterior_probabilities = [[0.0] * num_classes for _ in range(num_classes)]
confusion_matrix = [[0] * num_classes for _ in range(num_classes)]
class_counts = [0] * num_classes
class_totals = [0] * num_classes
incorrectly_assigned = 0

training_file = open(training_set_file_path, 'r')

line = training_file.readline()
training_class_count, feature_vector_len, training_file_len = map(int, line.split())



for i in range(training_file_len):
    line = training_file.readline()
    tokens = list(map(float, line.split()))
    training_labels[i] = int(tokens[0])
    training_data[i][:feature_vector_len] = tokens[1:feature_vector_len + 1]

training_file.close()

for j in range(feature_vector_len):
    mean_values[j] = sum(training_data[i][j] for i in range(training_file_len)) / training_file_len
    sd[j] = sum((training_data[i][j] - mean_values[j]) ** 2 for i in range(training_file_len))
    sd[j] = sd[j] ** 0.5

for i in range(training_file_len):
    for j in range(feature_vector_len):
        if sd[j] > 0.0001:
            training_data[i][j] = (training_data[i][j] - mean_values[j]) / sd[j]

for i in range(training_class_count):
    for j in range(training_class_count):
        confusion_matrix[i][j] = 0
incorrectly_assigned = 0

line = testing_file.readline()
training_class_count, feature_vector_len, mt = map(int, line.split())

output_file.write('\n')
output_file.write(' Results of classification:\n')
output_file.write(' Nr obj, Klasa faktyczna, Klasa przypisana\n')
output_file.write(' Object,      True class,   Assigned class\n')

for i in range(mt):
    line = testing_file.readline()
    tokens = list(map(float, line.split()))
    true_labels[i] = int(tokens[0])
    testing_data[:feature_vector_len] = tokens[1:feature_vector_len + 1]

    for j in range(feature_vector_len):
        if sd[j] > 0.001:
            testing_data[j] = (testing_data[j] - mean_values[j]) / sd[j]

    min_distance = 1e10
    for k in range(training_file_len):
        distance = sum((training_data[k][j] - testing_data[j]) ** 2 for j in range(feature_vector_len))
        if distance <= min_distance:
            min_distance = distance
            assigned_labels[i] = training_labels[k]

    if true_labels[i] != assigned_labels[i]:
        incorrectly_assigned += 1
    i1 = true_labels[i]
    i2 = assigned_labels[i]
    confusion_matrix[i1][i2] += 1

    output_file.write('{:7}{:16}{:18}\n'.format(i + 1, true_labels[i], assigned_labels[i]))

a = 100.0 * incorrectly_assigned / mt
output_file.write('\n')
output_file.write(' Error rate: {:4.1f}%\n'.format(a))

output_file.write('\n')
output_file.write(' OError rate: {:4.1f}%\n'.format(a))

output_file.write('\n')
output_file.write(' Confusion matrix:\n')
output_file.write('       ')

for j in range(1, training_class_count + 1):
    output_file.write('{:7}'.format(j))
output_file.write('\n')

for i in range(1, training_class_count + 1):
    output_file.write('{:7}'.format(i))
    for j in range(1, training_class_count + 1):
        output_file.write('{:7}'.format(confusion_matrix[i][j]))
    output_file.write('\n')

for i in range(1, training_class_count + 1):
    class_counts[i] = sum(confusion_matrix[i])
    class_totals[i] = sum(confusion_matrix[j][i] for j in range(0, training_class_count + 1))

for i in range(0, training_class_count):
    for j in range(0, training_class_count):
        prior_probabilities[i][j] = confusion_matrix[i + 1][j + 1] / class_counts[i + 1] if class_counts[
                                                                                                i + 1] != 0 else 0

output_file.write('\n')
output_file.write(' Probabilities a priori:\n')
output_file.write('        ')

for j in range(1, training_class_count + 1):
    output_file.write('{:7}'.format(j))
output_file.write('\n')

for i in range(0, training_class_count):
    output_file.write('{:7}'.format(i))
    for j in range(0, training_class_count):
        output_file.write('{:7.4f}'.format(prior_probabilities[i][j]))
    output_file.write('\n')

for i in range(0, training_class_count):
    for j in range(0, training_class_count):
        posterior_probabilities[i][j] = confusion_matrix[j + 1][i + 1] / class_totals[i + 1] if class_totals[
                                                                                                    i + 1] != 0 else 0

output_file.write('\n')
output_file.write(' Probabilities a posteriori:\n')
output_file.write('        ')

for j in range(1, training_class_count + 1):
    output_file.write('{:7}'.format(j))
output_file.write('\n')

for i in range(0, training_class_count):
    output_file.write('{:7}'.format(i + 1))
    for j in range(0, training_class_count):
        output_file.write('{:7.4f}'.format(posterior_probabilities[i][j]))
    output_file.write('\n')

output_file.write(' Press ENT to finish. Look into the file ' + output_file_path + '.')
testing_file.close()
output_file.close()
