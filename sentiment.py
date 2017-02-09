#!/usr/bin/env python
'''
    sentiment
    ---------

    Calculate the overall sentiment for each post.
'''

from __future__ import division

import json
import math
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


def get_score(text):
    '''Rank the sentiment of text'''

    return SENTIMENT.polarity_scores(text)


def rank_score(post, highest):
    '''Rank the score to get a total, weighted value for the score'''

    # if no upvotes, assume 1
    up = post.get("up", 1)
    down = post.get("down", 0)
    if not up or down:
        # if not any upvotes or downvotes, avoid a 0-division error
        up = 1
    percent = up / (up + down)

    # We want to favors comments with a high upvote percentage, while
    # rendering comments with a low upvote percentage into oblivion.
    # However, since early comments tend to get more upvotes regardless
    # we also want to slightly disfavor total votes.

    return (percent ** 2) * math.log(up/highest) * post["score"]["compound"]


def process(path):
    '''Process a file'''

    with open(path) as f:
        data = json.load(f)

    data["scores"] = []
    for posts in data["posts"].values():
        if posts:
            scores = []
            use_rank = "up" in posts[0]
            highest = posts[0].get("up", 1)
            for post in posts:
                # for instiz posts, take the mean
                # otherwise, weight the post rank into the equation
                post["score"] = get_score(post["text"])
                if use_rank:
                    scores.append(rank_score(post, highest))
                else:
                    scores.append(post["score"]["compound"] / len(posts))
            data["scores"].append(sum(scores))

    if data["scores"]:
        data["overall_score"] = sum(data["scores"]) / len(data["scores"])

    with open(path, 'w') as f:
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
