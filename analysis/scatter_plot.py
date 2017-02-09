#!/usr/bin/env python
'''
    scatter_plot
    -------------

    Plot a scatter plot from CSV data
'''

import os
import pandas as pd
import matplotlib.pyplot as plt

import argparse

# ARGS
# ----

PARSER = argparse.ArgumentParser()
PARSER.add_argument('csv',
                type=str,
                help='Path to CSV file to plot')

ARGS = PARSER.parse_args()

# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
IMAGES = os.path.join(HOME, "images")
VALIDATION = os.path.join(HOME, "validation")


def main():
    '''Load all dataframe and plot'''

    df = pd.read_csv(ARGS.csv, sep="\t")
    df.dropna(inplace=True)
    df.plot(kind='scatter', x='Manual', y='Automatic')
    plt.title("Ranking Automatic vs. Manual Sentiment")
    plt.legend(loc='best')

    name = os.path.splitext(os.path.basename(ARGS.csv))[0]
    plt.savefig(os.path.join(IMAGES, "scatter_{}.png".format(name)))


if __name__ == '__main__':
    main()
