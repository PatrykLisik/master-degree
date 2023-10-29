import numpy as np


data = np.array(
    [
        [2, 2, 2, 2, 2],
        [-2, -2, -2, -2, -2],
        [1, 1, -1, -1, -1],
        [-1, -1, 1, 1, 1],
    ]
)

w = np.array([-0.1, 0.2, -0.5, 0.3, -0.4])

expected = np.array([1, -1, 0.8, -0.8])

learn_speed = 0.1


def run_neuron(input, weigths, activation_func):
    sum = np.dot(input, weigths)
    return activation_func(sum)


def error(output, expected):
    err = np.abs(np.subtract(output, expected))
    return err


def learn(inputs, weigths, error, learn_speed):
    new_w = weigths.copy()
    change = learn_speed * error * inputs
    print("Change")
    print(change)
    new_w -= change
    return new_w


def line_activation(a, b):
    def _inner(x):
        return a * x + b

    return _inner


def norm(d):
    div = np.sqrt(np.sum(np.power(d, 2), axis=1))
    # print(div)
    # print(np.sum(np.power(d, 2), axis=1))
    return (d.T / div).T


# main
afunc = line_activation(a=1, b=0)

epoch = 0

while True:
    print("Epoch {epoch}")
    print("Single neuron")
    d_norm = norm(data)
    print(d_norm)

    for in_, exp_ in zip(d_norm, expected):
        n_out = run_neuron(weigths=w, input=in_, activation_func=afunc)
        err_ = np.abs(exp_ - n_out)
        print(f"error to learn {err_}")
        w = learn(inputs=in_, error=err_, weigths=w, learn_speed=learn_speed)
        print("New weigths")
        print(w)
    input()
    epoch += 1
    print("\n\n\n\n")
