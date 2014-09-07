# -*- coding: utf-8 -*-

from funcy import group_by
from pymongo import MongoClient
from multiprocessing import Pool
from task_gen_events_graphs import gen_graph
from task_cal_pagerank import gen_pagerank, gen_pagerank_maps
import task_cal_influence
import gc


gc.disable()


client = MongoClient()
db = client['github']
watch_events = db['watch_events']
pageranks = db['pageranks']


# def merge_dict(x, y):
#     z = {}
#     keys = us.uniq(x.keys() + y.keys())

#     for key in keys:
#         if key in x and key in y:
#             z[key] = x[key] + y[key]
#         elif key in x:
#             z[key] = x[key]
#         elif key in y:
#             z[key] = y[key]

#     return z


def group(events):
    return group_by(lambda x: x['repo'], events)


def set_events_info((repo, events)):
    def fetch(event):
        return watch_events.find_one(
            {'_id': event['_id']},
            {'repo': True, 'actor': True, 'created_at': True,
                'language': True, 'actor-following': True, '_id': False}
        )

    return (repo, map(fetch, events))


def not_single_event((repo, events)):
    return len(events) > 1


def store_pagerank((repo, events)):
    pageranks.insert(gen_pagerank_maps(gen_pagerank(gen_graph((repo, events)))))


def main():
    events = list(
        watch_events.find(
            {'repo-disabled': {'$exists': False}},
            {'repo': True}
        ))

    events = group(events)

    pool = Pool(15)

    events = pool.map(set_events_info, filter(not_single_event, events.items()))

    pool.close()
    pool.join()

    del pool

    pool = Pool(15)

    pool.map(store_pagerank, events)

    pool.close()
    pool.join()

    del pool

    task_cal_influence.main()

if __name__ == '__main__':
    main()
