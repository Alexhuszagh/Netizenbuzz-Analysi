#!/usr/bin/env python
'''
    sentiment_time
    --------------

    Process the sentiment with respect to time.
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

MALE_IDOLS = set(json.load(open(os.path.join(TAGS, "men.json"))))
FEMALE_IDOLS = set(json.load(open(os.path.join(TAGS, "women.json"))))

# FUNCTIONS
# ---------


def process(path, sentiment):
    '''Extract the sentiment with respect to time'''

    with open(path) as f:
        data = json.load(f)

    if "overall_score" in data:
        date = datetime.datetime.strptime(data["date"], "%Y/%m/%d")
        sentiment["all"][date] = data["overall_score"]
        if any([i in MALE_IDOLS for i in data["tags"]]):
            sentiment["men"][date] = data["overall_score"]
        if any([i in FEMALE_IDOLS for i in data["tags"]]):
            sentiment["women"][date] = data["overall_score"]


def plot(sentiment):
    '''Plot the data series'''

    # the data is noisy, take the sample every month
    all_ = pd.Series(sentiment["all"]).resample("1M", np.mean)
    men = pd.Series(sentiment["men"]).resample("1M", np.mean)
    women = pd.Series(sentiment["women"]).resample("1M", np.mean)
    df = pd.DataFrame({"All": all_, "Men": men, "Women": women})

    df.plot()
    plt.title("Netizenbuzz Sentiment")
    plt.legend(loc='best')
    plt.savefig(os.path.join(IMAGES, "sentiment_time.png"))


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
