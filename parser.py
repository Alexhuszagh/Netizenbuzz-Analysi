'''
    parser
    ------

    Processes data from posts to create JSON stores of the data.

    Example:
        {
            "text": "....",
            "tags": ["AOA"],
            "date": "2016-12-01"
        }
'''

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

# FUNCTIONS
# ---------


def isspace(node):
    '''Check if node is space'''

    if getattr(node, "isspace"):
        return node.isspace()
    return True


def get_parser(path):
    '''Get a beautiful soup parser from a file'''

    with open(path, 'rb') as f:
        return BeautifulSoup(f.read(), "lxml")


def extract_text(parser):
    '''Extract the source content and remove formatting'''

    data = []
    for node in parser.find(attrs={"class": "post-body entry-content"}):
        if not (isspace(node) or node.name == "div"):
            data.append(node.encode("utf-8"))

    return ''.encode("utf-8").join(data)


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


def parse_file(src, dst):
    '''Parse a file and convert it to JSON'''

    # make output directory
    if not os.path.exists(os.path.dirname(dst)):
        os.makedirs(os.path.dirname(dst))

    data = {}
    parser = get_parser(src)
    data["text"] = extract_text(parser)
    data["tags"] = extract_tags(parser)
    data["date"] = extract_date(parser)


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
