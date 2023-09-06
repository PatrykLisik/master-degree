import numpy as np


def gradient_func(x, y):
    return -np.cos(1 / (x * y)) / (x * x * y), -np.cos(1 / (x * y)) / (x * y * y)


# %%
def func(X, Y):
    return np.sin(1 / (X * Y))


# %%
def alpha(iter: int):
    return 0.05


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
    start_point1 = np.array([-1.87, 0.53])
    file_path = "./gradient.txt"
    with open(file_path, "w") as file:
        print("Pierwsze minium", file=file)
        simple_gradient(gradient=gradient_func, start_point=start_point1, file=file)

    start_point2 = np.array([-1, 0.3])
    with open(file_path, "a") as file:
        print("\n\nDrugie minium", file=file)
        simple_gradient(gradient=gradient_func, start_point=start_point2, file=file)
