#!/usr/bin/env python
'''
    tags
    ----

    Extract all tags from the file.
'''

import json
import os

from collections import Counter

# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.realpath(__file__))
JSON = os.path.join(HOME, "json")
TAGS = os.path.join(HOME, "tags")


# FUNCTIONS
# ---------


def process(path, tags):
    '''Update taglist with tags'''

    with open(path) as f:
        data = json.load(f)

    for item in data["tags"]:
        tags[item] += 1


def main():
    '''Walk over all posts and process the taglists.'''

    # iterate over posts
    tags = Counter()
    for year in os.listdir(JSON):
        for month in os.listdir(os.path.join(JSON, year)):
            for name in os.listdir(os.path.join(JSON, year, month)):
                path = os.path.join(JSON, year, month, name)
                process(path, tags)

    common = tags.most_common()
    with open(os.path.join(TAGS, "tags.json"), "w") as f:
        json.dump(common, f)

    with open(os.path.join(TAGS, "tags.csv"), "w") as f:
        f.write(u"Tag\tCounts\n")
        for item in common:
            f.write(u"{}\t{}\n".format(item[0], item[1]).encode("utf-8"))


if __name__ == '__main__':
    main()
