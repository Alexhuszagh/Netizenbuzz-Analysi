#!/usr/bin/env python
'''
    aoa_blockb
    ----------

    Compare AOA vs. Block B.
'''

import datetime
import json
import os

from collections import defaultdict

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
JSON = os.path.join(HOME, "json")
IMAGES = os.path.join(HOME, "images")
TAGS = os.path.join(HOME, "tags")

# FUNCTIONS
# ---------


def process(path, sentiment):
    '''Extract the sentiment with respect to time'''

    with open(path) as f:
        data = json.load(f)

    if "overall_score" in data:
        date = datetime.datetime.strptime(data["date"], "%Y/%m/%d")
        sentiment["all"][date] = data["overall_score"]
        if "block b" in data["tags"]:
            sentiment["block b"][date] = data["overall_score"]
        if "aoa" in data["tags"]:
            sentiment["aoa"][date] = data["overall_score"]


def plot(sentiment):
    '''Plot the data series'''

    # the data is noisy, take the sample every month
    all_ = pd.Series(sentiment["all"]).resample("1M", np.mean)
    aoa = pd.Series(sentiment["aoa"]).resample("1M", np.mean)
    blockb = pd.Series(sentiment["block b"]).resample("1M", np.mean)
    df = pd.DataFrame({"All": all_, "AOA": aoa, "Block B": blockb})

    df.plot()
    plt.title("AOA vs. Block B")
    plt.legend(loc='best')
    plt.savefig(os.path.join(IMAGES, "aoa_blockb.png"))


def main():
    '''Load all files and create a series with date and time'''

    sentiment = defaultdict(dict)
    for year in os.listdir(JSON):
        for month in os.listdir(os.path.join(JSON, year)):
            for name in os.listdir(os.path.join(JSON, year, month)):
                path = os.path.join(JSON, year, month, name)
                process(path, sentiment)

    plot(sentiment)


if __name__ == '__main__':
    main()
