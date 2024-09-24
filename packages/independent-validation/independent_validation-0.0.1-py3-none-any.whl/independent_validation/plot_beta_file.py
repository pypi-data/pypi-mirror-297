import matplotlib.pyplot as plt

import numpy as np
import scipy.stats as stats

import math

def plot_beta(predictions, true_values, filename='beta.png', all_betas=True, return_early=False):
    plt.clf()
    arr = np.array([predictions, true_values])
    cor = arr[0] == arr[1]

    x = np.linspace(0, 1, 10000)

    labels = np.unique(arr[1])
    _ = labels.shape[0]

    means = []
    vars = []

    for i in labels:
        mask = arr[1] == i
        a = cor[mask].sum() + 1
        b = mask.sum() - a + 2  # 2 because the minus a needs to be balanced.

        mean, var, skew, kurt = stats.beta.stats(a, b, moments='mvsk')
        means.append(mean)
        vars.append(var)

        if all_betas:
            plt.plot(x, stats.beta.pdf(x, a, b))

    # approximation as normal distributions to sum up the distributions
    mean = sum(means) / len(means)
    var = sum(vars) / (len(vars) ** 2)
    if return_early:
        return mean, var
    y = stats.norm.pdf(x, loc=mean, scale=math.sqrt(var))
    plt.plot(x, y, label='bacc')
    a = cor.sum() + 1
    b = cor.shape[0] - a + 2  # 2 because the minus a needs to be balanced.
    y = stats.beta.pdf(x, a, b)
    plt.plot(x, y, label='acc')
    plt.savefig(f'{filename}')
    return mean, var  # returning the parameters for the bacc