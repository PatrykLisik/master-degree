import numpy as np


data = np.array(
    [
        [3, 4, 3, 4, 5],
        [1, -2, 1, -2, -2],
        [-3, -2, -3, 2, 3],
    ]
)

neuron_count = 3

w = np.random.uniform(-1, 1, (data.shape[1], neuron_count))
expected = np.array([[1, -1, -1], [-1, 1, -1], [-1, -1, 1]])

learn_speed = 0.1


def run_neuron(input, weigths, activation_func):
    sum = np.dot(input, weigths)
    return activation_func(sum)


def error(output, expected):
    err = output - expected
    return err


def learn(inputs, weigths, error, learn_speed):
    new_w = weigths.copy()
    # error = np.expand_dims(error, axis=1)
    # inputs = np.expand_dims(inputs, axis=0)
    # print(f"Error {error.shape}")
    # print(f"Inputs {inputs.shape}")
    change = learn_speed * np.outer(inputs, error)
    # print("Change")
    # print(change)
    new_w = new_w + change
    return new_w


def line_activation(a, b):
    def _inner(x):
        return a * x + b

    return _inner


@np.vectorize
def sign(x):
    if x > 0:
        return 1
    return -1


def norm(d):
    div = np.sqrt(np.sum(np.power(d, 2), axis=1))
    # print(div)
    # print(np.sum(np.power(d, 2), axis=1))
    return (d.T / div).T


# main
afunc = line_activation(a=1, b=0)

epoch = 0
print(w)
while True:
    print(f"Epoch {epoch}")
    # print("Single neuron")
    d_norm = data
    # print(f" dnorm {d_norm}")

    for in_, exp_ in zip(d_norm, expected):
        n_out = run_neuron(weigths=w, input=in_, activation_func=sign)
        err_ = exp_ - n_out
        print(f"Out {n_out}")
        print(f"Exp {exp_}")
        print(f"error to learn {err_}")
        w = learn(inputs=in_, error=err_, weigths=w, learn_speed=learn_speed)
        # print("New weigths")
        # print(w)
    input()
    epoch += 1
    print("\n\n\n\n")
