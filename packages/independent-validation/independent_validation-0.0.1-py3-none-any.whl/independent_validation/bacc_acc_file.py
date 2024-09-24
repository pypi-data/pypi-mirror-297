from sklearn.metrics import accuracy_score, balanced_accuracy_score
import matplotx
from matplotlib import pyplot as plt


def bacc_acc(predicitions, true_values):
    preds = []
    trues = []
    accs = []
    baccs = []
    for pre, tru in zip(predicitions, true_values):
        preds.append(pre)
        trues.append(tru)
        accs.append(accuracy_score(trues, preds))
        baccs.append(balanced_accuracy_score(trues, preds))
    return accs, baccs


def save_as(filename='iv.png', x_axis=None, xlabel=None, ylabel=None, **kwargs):
    plt.clf()
    for label, values in kwargs.items():
        if x_axis is None:
            x_axis = list(range(len(values)))
        assert len(values) == len(x_axis)  # TODO: Make this error pretty
        plt.plot(x_axis, values, label=label)
    matplotx.line_labels()
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)
    if filename[-4:] != '.png':
        filename = filename + '.png'
    # filename.replace(' ', '_')
    plt.savefig(filename)
