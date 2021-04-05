#!/usr/bin/env python3

'''Plot and save WIMA vs Baseline latency cdf graph.'''

import sys
import numpy as np
import scipy.stats

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import matplotlib.lines as mlines


NUM_TICKS = 12
NUM_SUBTICKS = NUM_TICKS * 5
MAJ_ALPHA = 1.5
MIN_ALPHA = 0.2

LW = 1.5

X_LABEL = 'E2E Flow Setup Time (ms)'
Y_LABEL = 'Probability [%]'

DATA_TYPE = 'latency'
GRAPH_TYPE = 'cdf'
FILE_EXTENSION = '.png'


def format_axis(axis):
    '''Uses axis to configure the graph.'''
    locator = ticker.MaxNLocator
    axis.xaxis.set_ticks_position('both')
    axis.xaxis.set_major_locator(locator(NUM_TICKS))
    axis.xaxis.set_minor_locator(locator(NUM_SUBTICKS))
    axis.xaxis.grid(which='major', linestyle='-', alpha=MAJ_ALPHA)
    axis.xaxis.grid(which='minor', linestyle='-', alpha=MIN_ALPHA)
    axis.yaxis.grid(which='major', linestyle='-', alpha=MAJ_ALPHA)
    axis.yaxis.grid(which='minor', linestyle='-', alpha=MIN_ALPHA)
    axis.set_axisbelow(True)
    for iter_axis in (axis, axis.twinx()):
        iter_axis.yaxis.set_major_locator(locator(NUM_TICKS))
        iter_axis.yaxis.set_minor_locator(locator(NUM_SUBTICKS))
        iter_axis.set_ylim(axis.get_ylim())


def format_plot():
    '''Uses pyplot to configure the graph.'''
    plt.xlabel(X_LABEL, fontweight='bold')
    plt.ylabel(Y_LABEL, fontweight='bold')

    # Legend configuration
    black_dot = mlines.Line2D([], [], color='black', marker='o',
                              label='WIMA', linestyle='')

    red_dot = mlines.Line2D([], [], color='r', marker='o',
                            label='Baseline', linestyle='')

    leg = plt.legend(handles=[black_dot, red_dot],
                     loc='lower right', fancybox=False,
                     framealpha=1, shadow=False, borderpad=1)

    leg.get_frame().set_edgecolor('black')


def get_filename(conn):
    '''Return filename of the figure.'''
    filename = DATA_TYPE + '-'
    filename += GRAPH_TYPE + '-'
    filename += str(conn) + FILE_EXTENSION
    return filename


def open_file(filename):
    '''Return file content given filename.'''
    with open(filename) as file_:
        return file_.read()


def plot_graphs(graphs_dir):
    '''Plot the graphs and save the figures in graphs_dir.'''
    beg = 0
    end = 0
    inc = 0
    data = []
    wima = 1
    _, axis = plt.subplots()

    if graphs_dir[-1] != '/':
        graphs_dir += '/'

    summ = open_file('summary.csv').split(',')
    beg = int(summ[4])
    end = int(summ[5])
    inc = int(summ[6])
    conn = beg

    for line in open_file('latency.raw').splitlines():
        data = [float(i) for i in line.split(',')]
        norm = scipy.stats.norm(np.mean(data), np.std(data))
        cdf = [norm.cdf(i) for i in data]
        color = 'black' if wima else 'red'
        axis.scatter(data, cdf, c=color)
        if wima:
            wima = 0
        else:
            format_plot()
            format_axis(axis)
            #plt.show()
            plt.savefig(graphs_dir + get_filename(conn), dpi=600)
            _, axis = plt.subplots()
            wima = 1
            conn += inc
            if conn > end:
                break


if __name__ == '__main__':
    plot_graphs(sys.argv[1])
