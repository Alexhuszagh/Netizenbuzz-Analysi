#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
    word_count
    ----------

    Extract and rank the word counts from all posts, and extract
    the most common.
'''

import json
import os
import re

from collections import Counter

# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.realpath(__file__))
JSON = os.path.join(HOME, "json")

# REGEXP
# ------

DELIMITERS = re.compile(u"[\r\n\t !\"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]", re.U)
#  ㅋ|ㅠ
HANGUL = re.compile(u"((?:\u314b)|(?:\u3160))", re.U)

# FUNCTIONS
# ---------


def process(path, counts):
    '''Process the word counts from each comment.'''

    with open(path, "rb") as f:
        data = json.load(f)

    for posts in data["posts"].values():
        for post in posts:
            for word in DELIMITERS.split(post["text"]):
                for item in HANGUL.split(word):
                    item.strip()
                    if item:
                        counts[item] += 1


def main():
    '''Walk over all posts and process them to useable formats.'''

    # iterate over posts
    counts = Counter()
    for year in os.listdir(JSON):
        for month in os.listdir(os.path.join(JSON, year)):
            for name in os.listdir(os.path.join(JSON, year, month)):
                path = os.path.join(JSON, year, month, name)
                process(path, counts)

    # save
    with open(os.path.join(HOME, "word_count.json"), "wb") as f:
        json.dump(counts, f)


if __name__ == '__main__':
    main()
