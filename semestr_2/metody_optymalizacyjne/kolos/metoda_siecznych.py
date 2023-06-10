import numpy as np


def func(x):
    return 2 * np.sin(x) - np.log(x)


if __name__ == '__main__':
    a, b = 0.5, 4.5

    max_iter = 10**5
    epsilon = 10 ** (-7)

    x0 = epsilon
    x1 = b
    file_path = "./metoda_siecznych.txt"
    with open(file_path, "w") as file:
        for i in range(max_iter):
            new_x = (func(x1) * x0 - func(x0) * x1) / (func(x1) - func(x0))
            x0,x1 = x1, new_x
            print(f"Iteration {i:<4} | x1={x1:<20} | f(x1)={func(x1)}", file=file)

            if np.abs(func(x1)) <= epsilon:
                print(f"func(x)<=epsilon, x={x1}", file=file)
                break
