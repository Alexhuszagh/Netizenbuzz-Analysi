#!/usr/bin/env python
'''
    analyze
    -------

    Use Natural Language Text
'''

import json
import os

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.realpath(__file__))
JSON = os.path.join(HOME, "json")
LEXICON = os.path.join(HOME, "kpop_lexicon.txt")

SENTIMENT = SentimentIntensityAnalyzer(lexicon_file=LEXICON)


# FUNCTIONS
# ---------


def score(text):
    '''Rank the sentiment of text'''

    return SENTIMENT.polarity_scores(text)


def process(path):
    '''Process a file'''

    with open(path) as f:
        data = json.load(f)

    for posts in data["posts"].values():
        for post in posts:
            post["score"] = score(post["text"])

    with open(path, 'wb') as f:
        json.dump(data, f)


def main():
    '''Walk over all posts and process them to useable formats.'''

    # iterate over posts
    for year in os.listdir(JSON):
        for month in os.listdir(os.path.join(JSON, year)):
            for name in os.listdir(os.path.join(JSON, year, month)):
                path = os.path.join(JSON, year, month, name)
                process(path)


if __name__ == '__main__':
    main()
