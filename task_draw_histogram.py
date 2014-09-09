# -*- coding: utf-8 -*-

from pymongo import MongoClient
from github import Github
import numpy as np
from itertools import starmap

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import urllib2
import lxml.html
from config import users
import operator
import math
import sys
import gc


gc.disable()


def main(field):
    client = MongoClient()
    db = client['github']
    ranks = map(lambda x: x[0],
                db['influences'].find_one({'field': field})['ranks'][:10])

    github = map(
        lambda x: Github(x['login'], x['passwd'], timeout=3600), users)[0]

    def count_followers(user):
        return github.get_user(user).followers

    def count_stars(user):
        html = lxml.html.fromstring(urllib2.urlopen(
            'https://github.com/' + user).read())

        results = html.xpath(
            '//strong[@class="vcard-stat-count"]')

        strings = results[1].text.split('k')
        if len(strings) > 1:
            number = int(float(strings[0]) * 1000)
        else:
            number = int(strings[0])

        return number

    def count_public_repos(user):
        return github.get_user(user).public_repos

    followers_numbers = map(count_followers, ranks)
    stars_numbers = map(count_stars, ranks)
    public_repos_numbers = map(count_public_repos, ranks)
    products_sqrts = map(math.sqrt, list(starmap(
        operator.mul, zip(followers_numbers, list(starmap(
            operator.add, zip(stars_numbers, public_repos_numbers)))))))

    fig, ax = plt.subplots()

    fig.set_size_inches(20, 10)

    index = np.arange(len(ranks))
    bar_width = 0.2

    plt.bar(index, followers_numbers, bar_width, color='r', label='Followers')
    plt.bar(index + bar_width, stars_numbers, bar_width, color='g',
            label='Starred')
    plt.bar(index + 2 * bar_width, public_repos_numbers, bar_width, color='b',
            label='Repos')
    plt.bar(index + 3 * bar_width, products_sqrts, bar_width, color='y',
            label='Product')

    plt.xlabel('Developer')
    plt.ylabel('Number')
    plt.title("Developer's Followers, Starred and Repos")
    plt.xticks(index + 3 * bar_width, ranks)
    plt.legend()
    plt.tight_layout()

    plt.savefig('images/' + field + '-histogram.png')


if __name__ == '__main__':
    main(sys.argv[1])
