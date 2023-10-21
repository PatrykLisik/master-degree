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


def learn(inputs, weigths, err, learn_speed):
    new_w = weigths.copy()
    chnage = learn_speed*(err * inputs.T)
    print("Change")
    print(chnage)
    new_w -= chnage
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


print("Single neuron")
d_norm = norm(data)
print(d_norm)
afunc = line_activation(a=1, b=0)

n_out = run_neuron(weigths=w, input=d_norm, activation_func=afunc)
print("Neuron out")
print(n_out)

err = error(n_out, expected)
print("Neuron errors")
print(err)

w = learn(inputs=d_norm, err=err, weigths=w, learn_speed=learn_speed)
print("New weigths")
print(w)
