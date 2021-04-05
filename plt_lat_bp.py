#!/usr/bin/env python3

'''Plot and save WIMA vs Baseline latency boxplot graph.'''

import sys

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


NUM_TICKS = 12
NUM_SUBTICKS = NUM_TICKS * 5
MAJ_ALPHA = 1.5
MIN_ALPHA = 0.2

LW = 1.5

X_LABEL = ''
Y_LABEL = 'E2E Flow Setup Time (ms)'

DATA_TYPE = 'latency'
GRAPH_TYPE = 'boxplot'
FILE_EXTENSION = '.png'


def format_graph(graph):
    '''Configure graph properties.'''
    colors = ['black', 'black', 'red', 'red']
    for cap, color in zip(graph['caps'], colors):
        cap.set(color=color, linewidth=LW)

    for whisker, color in zip(graph['whiskers'], colors):
        whisker.set(color=color, linewidth=LW)

    colors = ['black', 'red']
    for mean, color in zip(graph['means'], colors):
        mean.set(markeredgecolor=color, linewidth=LW)

    for median, color in zip(graph['medians'], colors):
        median.set(color=color, linewidth=LW)

    for patch, color in zip(graph['boxes'], colors):
        patch.set_facecolor("None")
        patch.set_edgecolor(color)
        patch.set_linewidth(LW)

def format_axis(axis):
    '''Uses axis to configure the graph.'''
    locator = ticker.MaxNLocator
    axis.xaxis.set_ticks_position('both')
    axis.xaxis.set_ticks([0, 1, 2, 3])
    axis.set_xticklabels(['', 'WIMA', 'Baseline', ''])
    axis.yaxis.grid(which='major', linestyle='-', alpha=MAJ_ALPHA)
    axis.yaxis.grid(which='minor', linestyle='-', alpha=MIN_ALPHA)
    axis.set_axisbelow(True)
    for iter_axis in (axis, axis.twinx()):
        iter_axis.yaxis.set_major_locator(locator(NUM_TICKS))
        iter_axis.yaxis.set_minor_locator(locator(NUM_SUBTICKS))
        iter_axis.set_ylim(axis.get_ylim())


def format_plot(graph):
    '''Uses pyplot to configure the graph.'''
    plt.xlabel(X_LABEL, fontweight='bold')
    plt.ylabel(Y_LABEL, fontweight='bold')

    # Legend configuration
    leg = plt.legend([graph["boxes"][0], graph["boxes"][1]],
                     ['WIMA', 'Baseline'], loc='upper left',
                     fancybox=False, framealpha=1,
                     shadow=False, borderpad=1)

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
    _, axis = plt.subplots()

    meanpointprops = dict(
        marker='s',
        markerfacecolor='None',
        markeredgewidth=LW)

    if graphs_dir[-1] != '/':
        graphs_dir += '/'

    summ = open_file('summary.csv').split(',')
    beg = int(summ[4])
    end = int(summ[5])
    inc = int(summ[6])
    conn = beg

    for line in open_file('latency.raw').splitlines():
        data.append([float(i) for i in line.split(',')])
        if len(data) == 2:
            boxplot = axis.boxplot(
                data,
                showfliers=False,
                meanprops=meanpointprops,
                meanline=False,
                showmeans=True,
                patch_artist=True,
                notch=False,
                labels=['WIMA', 'Baseline'])
            format_graph(boxplot)
            format_plot(boxplot)
            format_axis(axis)
            #plt.show()
            plt.savefig(graphs_dir + get_filename(conn), dpi=600)
            _, axis = plt.subplots()
            data.clear()
            conn += inc
            if conn > end:
                break


if __name__ == '__main__':
    plot_graphs(sys.argv[1])
