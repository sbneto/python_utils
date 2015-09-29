__author__ = 'Samuel'


import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


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
                      gradient_start=0.2, log=False):
    ax = figure.add_subplot(position)
    ax.set_title(title)
    ret = ax.hist(data_points, label=labels, bins=bins,
                  weights=weight_structure(data_points, y_sum), range=x_range, stacked=True,
                  normed=normed, rwidth=0.9, #color=get_grayscale_colors(data_points, gradient_start),
                  log=log)
    if labels:
        handles, labels = ax.get_legend_handles_labels()
        ax.legend(handles[::-1], labels[::-1])
    return list(ret) + [ax]


def multiplot(data, labels, axes=('linear', 'linear'), loc='upper right', normalize=False):
    data_x = data[0]
    data_sets = data[1]
    data_y = data[2]
    ax = plt.gca()
    for s in np.nditer(np.unique(data_sets)):
        x_plot = data_x[data_sets == s]
        y_plot = data_y[data_sets == s]/np.sum(data_y[data_sets == s]) if normalize else data_y[data_sets == s]
        plt.plot(x_plot, y_plot)
    plt.xlabel(labels[0], fontsize=18)
    plt.ylabel(labels[2], fontsize=18)
    ax.xaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    if axes[0] == 'log':
        ax.set_xscale('log')
    if axes[1] == 'log':
        ax.set_yscale('log')
    ax.legend(np.unique(data_sets), loc=loc)
    plt.show()


def scatter(data, labels, axes=('linear', 'linear'), loc='upper right'):
    data_x = data[0]
    data_sets = data[1]
    data_y = data[2]
    ax = plt.gca()
    for s in np.nditer(np.unique(data_sets)):
        plt.scatter(data_x[data_sets == s], data_y[data_sets == s])
    plt.xlabel(labels[0], fontsize=18)
    plt.ylabel(labels[2], fontsize=18)
    if axes[0] == 'log':
        ax.set_xscale('log')
        plt.xlim(10**np.floor(np.log10(np.min(data_x))),
                 10**np.ceil(np.log10(np.max(data_x))))
    else:
        ax.xaxis.get_major_formatter().set_useOffset(False)
    if axes[1] == 'log':
        ax.set_yscale('log')
        plt.ylim(10**np.floor(np.log10(np.min(data_y))),
                 10**np.ceil(np.log10(np.max(data_y))))
    else:
        ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.legend(np.unique(data_sets), loc=loc)
    plt.show()


def scatter3d(data, labels, axes=('linear', 'linear', 'linear')):
    data_x = data[0]
    data_y = data[1]
    if axes[2] == 'log':
        data_z = np.log10(data[2])
    else:
        data_z = data[2]
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim3d(data_x.min(), data_x.max())
    ax.set_ylim3d(data_y.min(), data_y.max())
    ax.set_zlim3d(data_z.min(), data_z.max())
    ax.xaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.zaxis.get_major_formatter().set_scientific(False)
    ax.xaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.get_major_formatter().set_useOffset(False)
    ax.set_xlabel(labels[0], fontsize=18)
    ax.set_ylabel(labels[1], fontsize=18)
    ax.set_zlabel(labels[2], fontsize=18)
    if axes[0] == 'log':
        ax.xaxis.set_scale('log')
    if axes[1] == 'log':
        ax.yaxis.set_scale('log')
    if axes[2] == 'log':
        ax.zaxis.set_scale('log')
    ax.scatter(data_x, data_y, data_z)
    plt.show()


def wireframe(data, labels, axes=('linear', 'linear', 'linear')):
    data_x = data[0]
    data_y = data[1]
    if axes[2] == 'log':
        data_z = np.log10(data[2])
    else:
        data_z = data[2]
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_xlim3d(data_x.min(), data_x.max())
    ax.set_ylim3d(data_y.min(), data_y.max())
    ax.set_zlim3d(data_z.min(), data_z.max())
    ax.xaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.zaxis.get_major_formatter().set_scientific(False)
    ax.xaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.get_major_formatter().set_useOffset(False)
    ax.set_xlabel(labels[0], fontsize=18)
    ax.set_ylabel(labels[1], fontsize=18)
    ax.set_zlabel(labels[2], fontsize=18)
    if axes[0] == 'log':
        ax.xaxis.set_scale('log')
    if axes[1] == 'log':
        ax.yaxis.set_scale('log')
    if axes[2] == 'log':
        ax.zaxis.set_scale('log')
    data_x = np.array([data_x[data_y == year] for year in np.unique(data_y)])
    data_z = np.array([data_z[data_y == year] for year in np.unique(data_y)])
    data_y = np.array([data_y[data_y == year] for year in np.unique(data_y)])
    ax.plot_wireframe(data_x, data_y, data_z)
    plt.show()


def multiplot3d(data, labels, axes=('linear', 'linear', 'linear')):
    data_x = data[0]
    data_y = data[1]
    if axes[2] == 'log':
        data_z = np.log10(data[2])
    else:
        data_z = data[2]
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlim3d(data_x.min(), data_x.max())
    ax.set_ylim3d(data_y.min(), data_y.max())
    ax.set_zlim3d(data_z.min(), data_z.max())
    ax.set_xlabel(labels[0], fontsize=18)
    ax.set_ylabel(labels[1], fontsize=18)
    ax.set_zlabel(labels[2], fontsize=18)
    ax.xaxis.get_major_formatter().set_scientific(False)
    ax.yaxis.get_major_formatter().set_scientific(False)
    ax.zaxis.get_major_formatter().set_scientific(False)
    ax.xaxis.get_major_formatter().set_useOffset(False)
    ax.yaxis.get_major_formatter().set_useOffset(False)
    ax.zaxis.get_major_formatter().set_useOffset(False)
    if axes[0] == 'log':
        ax.xaxis.set_scale('log')
    if axes[1] == 'log':
        ax.yaxis.set_scale('log')
    if axes[2] == 'log':
        ax.zaxis.set_scale('log')
    for i in np.nditer(np.unique(data_y)):
        ax.plot(data_x[data_y == i], data_y[data_y == i], data_z[data_y == i])
    plt.show()


def histogram(data, labels, bins=100, axes=('linear', 'linear'), log_bin=None):
    data = data[0]
    if log_bin:
        bins = np.logspace(log_bin[0], log_bin[1], bins)

    fig = create_new_figure(4, 3)
    subplot_histogram(fig, data, 'bla', bins=bins)
    plt.xlabel(labels[0], fontsize=18)

    if axes[0] == 'log':
        plt.gca().set_xscale('log')
    if axes[1] == 'log':
        plt.gca().set_yscale('log')

    plt.show()