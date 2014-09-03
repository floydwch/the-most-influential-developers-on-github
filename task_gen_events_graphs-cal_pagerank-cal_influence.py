# -*- coding: utf-8 -*-

from underscore import _ as us
from more_itertools import flatten
from pymongo import MongoClient
from task_gen_events_graphs import gen_graph
from task_cal_pagerank import gen_pagerank_maps
import task_cal_influence
import gc


gc.disable()


def main():
    client = MongoClient()
    db = client['github']
    watch_events = db['watch_events']
    pageranks = db['pageranks']

    pagerank_maps = list(
        flatten(map(us.compose(gen_graph, gen_pagerank_maps),
                us.groupBy(list(watch_events.find(
                {'repo-disabled': {'$exists': False}})), 'repo').items())))

    pageranks.insert(pagerank_maps)

    task_cal_influence.main()

if __name__ == '__main__':
    main()
