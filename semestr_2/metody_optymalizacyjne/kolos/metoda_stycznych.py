import numpy as np

a, b = 2.2, 5


def func(x):
    return np.arctan(np.log(x ** 3 + 1) - 3)


def dfunc(x):
    return (3 * x ** 2) / ((x ** 3 + 1) * ((3 - np.log(x ** 3 + 1)) ** 2 + 1))


def ddfunc(x):
    return 3 * x * (8 * x ** 3 - (x ** 3 - 2) * np.log(x ** 3 + 1) ** 2 - 12 * np.log(x ** 3 + 1) + 20) / (
            (x ** 3 + 1) ** 2 * (np.log(x ** 3 + 1) ** 2 - 6 * np.log(x ** 3 + 1) + 10) ** 2
    )


x = a
max_iter = 1000
epsilon = 10 ** (-710)
file_path = "./metoda_stycznych.txt"
with open(file_path, "w") as file:
    for i in range(max_iter):
        if np.abs(func(x)) <= epsilon:
            print(f"abs(func(x)) <= epsilon, x={x}", file=file)
            break
        new_x = x - func(x) / dfunc(x)

        if np.abs(x - new_x) <= epsilon:
            print(f"abs(x - new_x) <= epsilon, x={x}", file=file)
            break
        x = new_x
        print(f"Iteration {i:<4} | x={x:<20} | f(x)={func(x)}", file=file)
