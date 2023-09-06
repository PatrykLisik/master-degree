import numpy as np

a, b = 2.2, 5


def func(x):
    return np.sin(1 / x) - 0.1


def dfunc(x):
    return -np.cos(1 / x) / (x * x)


def ddfunc(x):
    return (2 * np.cos(1 / x) - np.sin(1 / x)) / x ** 4


def styczne(x):
    max_iter = 1000
    epsilon = np.float64(10) ** (-10)
    file_path = "./metoda_stycznych.txt"
    with open(file_path, "a") as file:
        print("Styczne ")
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


if __name__ == '__main__':
    file_path = "./metoda_stycznych.txt"
    with open(file_path, "w") as file:
        print("", file=file)

    styczne(0.072)
    styczne(0.132)
    styczne(0.3)
