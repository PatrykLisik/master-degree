import numpy as np


def function(x):
    return np.sin(1 / x) - 0.1


def bisection(start, end, func, max_iter=1000, epsilon=np.float64(10) ** (-7), file="./bisection.txt"):
    with open(file, "a") as file:
        print(f"\nBisection in rage [{start}, {end}]", file=file)
        for i in range(max_iter):
            x = (start + end) / 2
            if func(start) * func(x) < 0:
                end = x
            if func(x) * func(end) < 0:
                start = x

            print(
                f"Iteration {i:<4} | x={x:<20} | f((a+b)/2)={func((start + end) / 2)}",
                file=file)

            if (np.abs(x) <= epsilon) or (np.abs(func((start + end) / 2)) <= epsilon):
                print(f"abs(x) <= epsilon, solution: (a+b)/2={(start + end) / 2}", file=file)
                return (start + end) / 2


if __name__ == '__main__':
    file_path = "./bisection.txt"
    with open(file_path, "w") as file:
        print("", file=file)
    # Pierwsze minimum
    start, end = np.float64(0.07), np.float64(0.125)
    bisection(start, end, function)

    start, end = np.float64(0.125), np.float64(0.2)
    bisection(start, end, function)

    start, end = np.float64(0.2), np.float64(4)
    bisection(start, end, function)
