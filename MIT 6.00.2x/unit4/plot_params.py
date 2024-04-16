import matplotlib.pyplot as plt


def plt_params():
    # set line width
    plt.rcParams['lines.linewidth'] = 4
    # set font size for titles
    plt.rcParams['axes.titlesize'] = 20
    # set font size for labels on axes
    plt.rcParams['axes.labelsize'] = 20
    # set size of numbers on x-axis
    plt.rcParams['xtick.labelsize'] = 16
    # set size of numbers on y-axis
    plt.rcParams['ytick.labelsize'] = 16
    # set size of ticks on x-axis
    plt.rcParams['xtick.major.size'] = 7
    # set size of ticks on y-axis
    plt.rcParams['ytick.major.size'] = 7
    # set size of markers
    plt.rcParams['lines.markersize'] = 10
    # set number of examples shown in legends
    plt.rcParams['legend.numpoints'] = 1