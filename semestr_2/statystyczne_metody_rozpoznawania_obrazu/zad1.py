import numpy as np
import pandas as pd

train_file_path = "./data/iris_trn.txt"
test_file_path = "./data/iris_tst.txt"

train_data = pd.read_csv(train_file_path, sep=" ", skiprows=1)
train_data.values[0] = "Class"

for index in range(len(train_data.values)):
    train_data.values[index] = f"P{index}"

print(train_data)
