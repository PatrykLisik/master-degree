import numpy as np


def gradient_func(x, y):
    return (2 * np.exp(-5 * x - 3 * y ** 2) * (-5 * x ** 3 + 20 * x ** 2 * y + x - 2 * y)), (
            -2 * x * np.exp(-5 * x ** 2 - 3 * y ** 2) * (3 * x * y - 12 * y ** 2 + 2))


# %%
def func(X, Y):
    return (X ** 2 - 4 * X * Y) * np.exp(-3 * Y ** 2 - 5 * X ** 2)


# %%
def alpha(iter: int):
    return 0.02


def simple_gradient(gradient, start_point, file, max_iter_count=10 ** 5,
                    epsilon=np.float64(10) ** (-7),
                    ):
    current_point = start_point.copy()
    for iteration in range(max_iter_count):
        dx, dy = gradient(current_point[0], current_point[1])
        if np.abs(dx) <= epsilon and np.abs(dy) <= epsilon:
            print(f"STOP | Iter {iteration:<4} | dx={dx:<20} | dy={dy:<20}| dx<=epsilon and dy <=epsilon",
                  file=file)
            break
        current_point -= alpha(iteration) * np.array([dx, dy])
        print(
            f"Iter {iteration:<4} | alpha: {alpha(iteration):<5} | x={current_point[0]:<25} | y={current_point[1]:<20} | z={str(func(current_point[0], current_point[1])):<12}",
            file=file)


if __name__ == '__main__':
    start_point1 = np.array([-0.34, -1.04])
    file_path = "./gradient.txt"
    with open(file_path, "w") as file:
        print("Pierwsze minium", file=file)
        simple_gradient(gradient=gradient_func, start_point=start_point1, file=file)

    start_point2 = np.array([0.2, 1.16])
    with open(file_path, "a") as file:
        print("\n\nDrugie minium", file=file)
        simple_gradient(gradient=gradient_func, start_point=start_point2, file=file)
