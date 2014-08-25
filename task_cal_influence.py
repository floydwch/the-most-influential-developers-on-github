# -*- coding: utf-8 -*-

from underscore import _ as us
from pymongo import MongoClient
import operator
import gc


gc.disable()

client = MongoClient()
db = client['github']
pageranks = db['pageranks']
influence = db['influence']


def cal_influence_ranking((actor, records)):
    return (actor, sum(us.pluck(records, 'centrality')))


all_influence_ranks = sorted(
    map(cal_influence_ranking,
        us.groupBy(list(pageranks.find()), 'actor').items()),
    key=operator.itemgetter(1), reverse=True)

influence.insert({
    'field': 'all',
    'ranks': all_influence_ranks
})

print 'top 25:'
for i, (actor, pagerank) in enumerate(all_influence_ranks[:25]):
    print str(i + 1) + '.', actor, pagerank

print 'top 25(hide score):'
for i, (actor, pagerank) in enumerate(all_influence_ranks[:25]):
    print str(i + 1) + '.', actor
