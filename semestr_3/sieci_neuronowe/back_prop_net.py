import numpy as np

neuron_count = 5
out_neuron_count = 1


data = np.array(
    [
        [
            0,
            0,
            0,
            0,
            0,
        ],
        [
            1,
            1,
            1,
            1,
            1,
        ],
        [
            1,
            1,
            0,
            0,
            0,
        ],
        [
            1,
            0,
            1,
            0,
            1,
        ],
    ]
)

h_w = np.random.uniform(-1, 1, (data.shape[1], neuron_count))
o_w = np.random.uniform(-1, 1, (out_neuron_count, neuron_count))

expected = np.array([1, 0, 0.3, 0.7])

learn_speed = 0.1


def run_neuron(inputs, h_weigths, o_weigths, activation):
    inputs = np.array(inputs, ndmin=2).T
    h_out = activation(np.dot(h_weigths, inputs))
    o_out = activation(np.dot(o_weigths, h_out))
    return o_out


def error(output, expected):
    err = output - expected
    return err


def learn(
    inputs,
    expected,
    h_weigths,
    o_weigths,
    out_err,
    learn_speed,
    d_activation,
    activation,
):
    inputs = np.array(inputs, ndmin=2).T
    expected = np.array(expected, ndmin=2).T
    h_out = activation(np.dot(h_weigths, inputs))
    o_out = activation(np.dot(o_weigths, h_out))

    o_err = expected - o_out
    # print(f"p_err {o_err}")
    h_err = np.dot(o_weigths.T, o_err) * (h_out * (1 - h_out))

    # print(f"{h_out=}")
    # print(f"{o_weigths=}")
    o_weigths += learn_speed * np.dot(o_err * d_activation(o_out), h_out.T)
    h_weigths += learn_speed * np.dot(h_err, inputs.T)

    return h_weigths, o_weigths


def line_activation(a, b):
    def _inner(x):
        return a * x + b

    return _inner


@np.vectorize
def sign(x):
    if x > 0:
        return 1
    return -1


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def d_sigmoid(x):
    return sigmoid(x) * (1 - sigmoid(x))


def norm(d):
    div = np.sqrt(np.sum(np.power(d, 2), axis=1))
    # print(div)
    # print(np.sum(np.power(d, 2), axis=1))
    return (d.T / div).T


# main
afunc = line_activation(a=1, b=0)

epoch = 0
print(h_w)
print()
while True:
    print(f"Epoch {epoch}")
    # print("Single neuron")
    d_norm = data
    # print(f" dnorm {d_norm}")

    for in_, exp_ in zip(d_norm, expected):
        n_out = run_neuron(
            h_weigths=h_w, o_weigths=o_w, inputs=in_, activation=sigmoid
        )
        err_ = exp_ - n_out
        # print(f"Inp {in_}")
        # print(f"Out {n_out}")
        # print(f"Exp {exp_}")
        # print(f"error to learn {err_}")
        h_w, o_w = learn(
            inputs=in_,
            expected=exp_,
            out_err=err_,
            h_weigths=h_w,
            o_weigths=o_w,
            learn_speed=learn_speed,
            d_activation=d_sigmoid,
            activation=sigmoid,
        )
        print(
            f"error avg {np.mean(np.abs(err_)):<30} | error max {np.max(np.abs(err_))}"
        )
        # print("New weigths")
        # print(w)
    if epoch % 1 == 0:
        user_in = input("Press to continue")
    epoch += 1
    print("\n\n\n\n")
