from plot_beta_file import plot_beta
from independent_validation_file import independent_validation

import matplotlib.pyplot as plt
import scipy.stats as stats
import numpy as np

def plot_multiple(classifiers, X, y, batch_size=1, start_trainset_size=10, scaler=None, talk=False, filename='beta.png', all_betas=False):
    dists = {}
    for clf in classifiers:
        if talk:
            print(f'Starting with classifier {clf.__class__.__name__}')
        predictions, true_values = independent_validation(clf, X, y, batch_size=batch_size, start_trainset_size=start_trainset_size, scaler=scaler, talk=talk)
        mean, var = plot_beta(predictions, true_values, filename=filename, all_betas=all_betas, return_early=True)
        dists.update({clf: (mean, var)})
    plt.clf()
    x = np.linspace(0, 1, 10000)
    for clf in dists.keys():
        mean, var = dists[clf]
        y = stats.norm.pdf(x, loc=mean, scale=math.sqrt(var))
        plt.plot(x, y, label=clf.__class__.__name__)
    plt.savefig(f'{filename}')