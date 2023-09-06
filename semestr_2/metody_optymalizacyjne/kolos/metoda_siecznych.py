import numpy as np


def function(x):
    return np.sin(1 / x) - 0.1


def secant_method(x0, x1, func, file_path="./metoda_siecznych.txt"):
    max_iter = 10 ** 5
    epsilon = 10 ** (-7)
    with open(file_path, "a") as file:
        for i in range(max_iter):
            new_x = (func(x1) * x0 - func(x0) * x1) / (func(x1) - func(x0))
            x0, x1 = x1, new_x
            print(f"Iteration {i:<4} | x1={x1:<20} | f(x1)={func(x1)}", file=file)

            if np.abs(func(x1)) <= epsilon:
                print(f"func(x)<=epsilon, x={x1}", file=file)
                break


if __name__ == '__main__':
    file_path = "./metoda_siecznych.txt"

    with open(file_path, "w") as file:
        print("", file=file)
    # Pierwsze minimum
    secant_method(0.075, 0.081, function, file_path)

    secant_method(0.038, 0.041, function, file_path)

    secant_method(0.125, 0.2, function, file_path)

    secant_method(0.2, 0.4, function, file_path)
