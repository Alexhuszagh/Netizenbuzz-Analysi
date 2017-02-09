#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    validation
    ----------

    Extract and analyze the sentiment of 2 sets of 40 articles,
    one set with 20 articles each from the top male and female
    idols, and another set with 20 articles each from Block B and AOA.
'''

import json
import os
import random

from collections import defaultdict

# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.realpath(__file__))
JSON = os.path.join(HOME, "json")
VALIDATION = os.path.join(HOME, "validation")

MEN = {"exo", "big bang", "super junior", "g-dragon", "army", "b2st", "shinee", "rain", "infinite", "winner"}
WOMEN = {"snsd", "fx", "t-ara", "aoa", "2ne1", "suzy", "kara", "iu", "sulli", "sistar"}
COUNT = 20


# FUNCTIONS
# ---------


def get_title(data):
    '''Normalize the title with date as an identifie'''

    return u"{}-{}".decode("utf-8").format(data["date"], data["title"])


def extract_article(path, articles):
    '''Update article list if tag satisfies condition'''

    with open(path) as f:
        data = json.load(f)

    title = get_title(data)
    articles["all"].append(title)
    if "aoa" in data["tags"]:
        articles["aoa"].append(title)
    if "block b" in data["tags"]:
        articles["blockb"].append(title)
    if any([i in MEN for i in data["tags"]]):
        articles["men"].append(title)
    if any([i in MEN for i in data["tags"]]):
        articles["women"].append(title)


def save_articles(articles):
    '''Save all article titles as well as a random subset'''

    with open(os.path.join(VALIDATION, "articles.json"), 'w') as f:
        json.dump(articles, f)

    for key in ["aoa", "blockb", "men", "women"]:
        sample = random.sample(articles[key], COUNT)
        with open(os.path.join(VALIDATION, "{}.json".format(key)), 'w') as f:
            json.dump(sample, f)

def main():
    '''Walk over all posts and extract all articles within a certain subset.'''

    articles = defaultdict(list)
    # iterate over posts
    for year in os.listdir(JSON):
        for month in os.listdir(os.path.join(JSON, year)):
            for name in os.listdir(os.path.join(JSON, year, month)):
                path = os.path.join(JSON, year, month, name)
                extract_article(path, articles)

    save_articles(articles)


if __name__ == '__main__':
    main()
