'''
    archiver
    --------

    Scrapes and saves all data from netizenbuzz.net
'''

import os
import re
import time

import requests

# CONSTANTS
# ---------

DOMAIN = u"https://netizenbuzz.blogspot.com/"
PATH = u"2017/02/teen-tops-l-joe-requests-contract.html"
URL = DOMAIN + PATH

HOME = os.path.dirname(__file__)
POSTS = os.path.join(HOME, "posts")

# REGEXP
# ------

NAME = re.compile(".*(?P<year>\d{4})/(?P<month>\d{2})/(?P<post>.*\.html)")
PREVIOUS = re.compile(r"blog-pager-older-link\' href=\'(.*)\' id")

# FUNCTIONS
# ---------


def download(url):
    '''Download a URL and return the text'''

    return requests.get(url).text


def find_previous(text):
    '''Find the previous URL from the parser'''

    match = PREVIOUS.search(text)
    if match:
        return match.group(1)


def parse_post(url, text):
    '''Parse url and extract data from post'''

    match = NAME.match(url)
    directory = os.path.join(match.group("year"), match.group("month"))
    name = match.group("post")
    path = os.path.join(POSTS, directory, name)

    if not os.path.exists(os.path.dirname(path)):
        os.makedirs(os.path.dirname(path))

    with open(path, 'wb') as f:
        f.write(text.encode('utf-8'))


def main():
    '''Archive all posts iteratively from Netizenbuzz'''

    url = URL
    while url:
        text = download(url)
        parse_post(url, text)
        url = find_previous(text)
        time.sleep(0.1)


if __name__ == '__main__':
    main()
