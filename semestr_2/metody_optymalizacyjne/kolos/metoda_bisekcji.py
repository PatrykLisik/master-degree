import numpy as np


def function(x):
    return np.arctan(np.log(x ** 3 + 1) - 5)


def bisection(start, end, func, max_iter=1000, epsilon=np.float64(10) ** (-7), file="./bisection.txt"):
    with open(file, "w") as file:
        for i in range(max_iter):
            x = (start + end) / 2
            if func(start) * func(x) < 0:
                end = x
            if func(x) * func(end) < 0:
                start = x

            print(
                f"Iteration {i:<4} | x={x:<20} | Solution (a+b)/2={(start + end) / 2:<20} | f((a+b)/2)={func((start + end) / 2)}",
                file=file)

            if (np.abs(x) <= epsilon) or (np.abs(func((start + end) / 2)) <= epsilon):
                print("np.abs(x) <= epsilon")
                return (start + end) / 2


if __name__ == '__main__':
    start, end = np.float64(1), np.float64(6)
    bisection(start, end, function)
