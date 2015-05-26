__author__ = 'Samuel'


import matplotlib.pyplot as plt
import numpy as np


def create_new_figure(w, h):
    fig = plt.figure()
    fig.set_size_inches(w, h)

    params = {'backend': 'eps',
              'font.family': 'serif',
              'font.size': 8,
              'axes.labelsize': 6,
              'legend.fontsize': 6,
              'xtick.labelsize': 6,
              'ytick.labelsize': 6}
    plt.rcParams.update(params)
    fig.set_tight_layout(True)
    return fig


def count_list_structure(original):
    size = 0
    for e in original:
        try:
            size += count_list_structure(iter(e))
        except TypeError:
            size += 1
    return size


def copy_list_structure(original, val):
    structure = []
    for e in original:
        try:
            structure.append(copy_list_structure(iter(e), val))
        except TypeError:
            structure.append(val)
    return structure


def weight_structure(original, y_sum):
    return copy_list_structure(original, y_sum/count_list_structure(original)) if y_sum else None


def get_grayscale_colors(data_points, gradient_start=0.2):
    try:
        if len(data_points) > 0:
            iter(data_points[0])
            n_data_points = len(data_points)
        else:
            n_data_points = 0
    except TypeError:
        n_data_points = 1
    return plt.cm.gray(np.arange(gradient_start, 1.0, (1.0 - gradient_start)/n_data_points))


def subplot_histogram(figure, data_points, title,
                      labels=None, position=111, bins=20,
                      y_sum=None, x_range=None, normed=False,
                      gradient_start=0.2):
    ax = figure.add_subplot(position)
    ax.set_title(title)
    ret = ax.hist(data_points, label=labels, bins=bins,
                  weights=weight_structure(data_points, y_sum), range=x_range, stacked=True,
                  normed=normed, color=get_grayscale_colors(data_points, gradient_start), rwidth=0.9)
    if labels:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
    return list(ret) + [ax]

