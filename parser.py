#!/usr/bin/env python
'''
    parser
    ------

    Processes data from posts to create JSON stores of the data.
    This ranks the popularity of the posts.

    Example:
        {
            "text": "....",
            "tags": ["AOA"],
            "date": "2016-12-01"
        }
'''

import json
import os
import re

from bs4 import BeautifulSoup

# CONSTANTS
# ---------

HOME = os.path.dirname(os.path.realpath(__file__))
POSTS = os.path.join(HOME, "posts")
JSON = os.path.join(HOME, "json")

MONTHS = {
    "January": "01",
    "February": "02",
    "March": "03",
    "April": "04",
    "May": "05",
    "June": "06",
    "July": "07",
    "August": "08",
    "September": "09",
    "October": "10",
    "November": "11",
    "December": "12",
}

# REGEXP
# ------

DATE = re.compile("(?P<weekday>\w+), (?P<month>\w+) (?P<day>\d+), (?P<year>\d+)")
TITLE = re.compile("(?:Naver)|(?:Nate)|(?:Instiz)|(?:Daum)")
VOTE = re.compile(".*\[(?P<up>(?:\+)?[0-9,]+), (?:\-(?P<down>[0-9,]+))?\](?P<text>.*)")

# FUNCTIONS
# ---------


def tostring(node):
    '''Get string representation of node'''

    return node.encode("utf-8")


def isspace(node):
    '''Check if node is space'''

    if getattr(node, "isspace"):
        return node.isspace()
    return True


def istitle(string):
    '''Check if the node is a title'''

    return TITLE.search(string)


def get_parser(path):
    '''Get a beautiful soup parser from a file'''

    with open(path, 'rb') as f:
        return BeautifulSoup(f.read(), "lxml")


def extract_votes(text):
    '''Extract votes from the text'''

    match = VOTE.search(text)
    if match:
        down = match.group("down").replace(",", "") or "0"
        return {
            "text": match.group("text"),
            "up": int(match.group("up").replace(",", "")),
            "down": int(down)
        }

    return {"text": text}


def extract_text(parser, data):
    '''Extract the source content and remove formatting'''

    data["posts"] = {}
    title = ""

    # Instiz articles don't have special
    is_instiz = "instiz" in data["tags"] or "Instiz" in data["title"]
    is_pann = "pann" in data["tags"] or "Pann" in data["title"]
    if is_instiz:
        title = "Instiz"
        data["posts"][title] = []
    elif is_pann:
        title = "Pann"
        data["posts"][title] = []

    # iterate over all comments
    for node in parser.find(attrs={"class": "post-body entry-content"}):
        if not (isspace(node) or node.name == "div"):
            string = tostring(node).strip()

            if istitle(string):
                # new article, set a new title
                title = string
            elif string not in {"-", ":", "'", "+"}:
                # process a comment
                posts = data["posts"].setdefault(title, [])
                if not is_instiz:
                    posts.append(extract_votes(string))
                else:
                    posts.append({"text": string})


def extract_tags(parser):
    '''Extract the tags for the post'''

    tags = []
    for node in parser.find(attrs={"class": "meta_categories"}):
        if hasattr(node, "text"):
            tags.append(node.text)

    return tags


def extract_date(parser):
    '''Extract the date for the post'''

    node = parser.find(attrs={"class": "date-header"})
    match = DATE.match(node.text)
    if match:
        return "{year}/{month}/{day}".format(year=match.group("year"), month=MONTHS[match.group("month")], day=match.group("day"))


def extract_title(parser):
    '''Extract title for the post'''

    return parser.find(attrs={'property': 'og:title'}).get("content")


def extract_url(parser):
    '''Extract URL for the post'''

    return parser.find(attrs={'property': 'og:url'}).get("content")


def parse_file(src, dst):
    '''Parse a file and convert it to JSON'''

    # make output directory
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    data = {}
    parser = get_parser(src)
    data["tags"] = extract_tags(parser)
    data["date"] = extract_date(parser)
    data["title"] = extract_title(parser)
    data["url"] = extract_url(parser)
    extract_text(parser, data)

    with open(dst, "wb") as f:
        json.dump(data, f)


def main():
    '''Walk over all posts and process them to useable formats.'''

    # iterate over posts
    for year in os.listdir(POSTS):
        for month in os.listdir(os.path.join(POSTS, year)):
            for name in os.listdir(os.path.join(POSTS, year, month)):
                src = os.path.join(POSTS, year, month, name)
                dst = os.path.join(JSON, year, month, name)
                parse_file(src, dst)


if __name__ == '__main__':
    main()
