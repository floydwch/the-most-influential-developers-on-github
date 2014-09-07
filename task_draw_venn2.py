# -*- coding: utf-8 -*-

from pymongo import MongoClient

import matplotlib
matplotlib.use('Agg')

from matplotlib import pyplot as plt
from matplotlib_venn import venn2
import sys


def main(*fields):
    client = MongoClient()
    db = client['github']
    influences = db['influences']
    sets = map(lambda x: set([i[0] for i in influences.find_one(
        {'field': x})['ranks'][:25]]), fields)

    venn2(sets, fields)
    plt.savefig('images/' +
                fields[0] + '-' + fields[1] +
                '-venn2.png')

    print sets[0].intersection(sets[1])


if __name__ == '__main__':
    main(*sys.argv[1:3])
