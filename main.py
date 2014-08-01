# -*- coding: utf-8 -*-

from datetime import datetime
from multiprocessing import Pool
import logging
from more_itertools import chunked, flatten
from pymongo import MongoClient


FROM_TIME = datetime(2011, 2, 12, 0)
TO_TIME = datetime(2011, 2, 12, 3)
CHUNK_SIZE = 60
THREAD_NUMBER = 2 * CHUNK_SIZE

logging.basicConfig(filename='grab.log', level=logging.DEBUG)

client = MongoClient()
db = client['github']
watch_events = db['watch_events']
processed_times = db['processed_times']
defects = db['defects']


def loads_invalid_obj_list(s):
    from json import JSONDecoder

    decoder = JSONDecoder()
    s_len = len(s)
    objs = []
    end = 0

    while end != s_len:
        obj, end = decoder.raw_decode(s, idx=end)
        objs.append(obj)

    return objs


def field_select(event):
    if event.get('repo', None):
        if type(event['actor']) is unicode:
            refined = (
                event['actor'],
                event.get('repo', {}).get('name', None),
                event.get('created_at', None))
        else:
            refined = (
                event.get('actor', {}).get(
                    'login', event.get('payload', {}).get('actor', None)),
                event.get('repo', {}).get('name', None),
                event.get('created_at', None))
    else:
        if event.get('repository', {}).get('full_name', None):
            refined = (
                event.get('actor', None),
                event.get('repository', {}).get('full_name', None),
                event.get('created_at', None))
        else:
            if event.get('repository', {}).get('owner', None) and \
                    event.get('repository', {}).get('name', None):
                refined = (
                    event.get('actor', None),
                    event.get('repository', {}).get('owner') + '/'
                    + event.get('repository', {}).get('name'),
                    event.get('repository', {}).get('name', None),
                    event.get('created_at', None))
            else:
                refined = (
                    event.get('actor', None),
                    None,
                    event.get('created_at', None))

    if None in refined:
        defects.insert(event)

    return dict(zip(['actor', 'repo', 'created_at'], refined))


def grab(number):
    from gzip import GzipFile
    from urlgrabber import urlopen
    from datetime import timedelta

    time_str = (FROM_TIME + timedelta(hours=number)).strftime('%Y-%m-%d-%-H')

    if processed_times.find(
            {'time': time_str, 'status': 'ok'}).count():  # already grab
        return []

    url = 'http://data.githubarchive.org/%s.json.gz' % time_str

    for i in xrange(10):  # retry 10 times
        try:
            with GzipFile(fileobj=urlopen(url)) as gz_file:
                events = loads_invalid_obj_list(''.join(
                    map(lambda x: unicode(x, 'ISO-8859-1'), map(
                        lambda x: x.strip(), list(gz_file)))))

                processed_times.insert({'time': time_str, 'status': 'ok'})

                return map(field_select, filter(
                    lambda x: x['type'] == 'WatchEvent', events))

        except Exception as e:
            logging.warning(str(e))
            continue
        break
    else:
        processed_times.insert({'time': time_str, 'status': 'error'})
        return []


numbers_chunks = chunked(
    range(int((TO_TIME - FROM_TIME).total_seconds() / 3600)), CHUNK_SIZE)


for numbers in numbers_chunks:
    pool = Pool(THREAD_NUMBER)
    new_watch_events = filter(
        lambda x: None not in x.values(), flatten(pool.map(grab, numbers)))
    pool.close()
    pool.join()

    if new_watch_events:  # avoid do an empty bulk write
        watch_events.insert(new_watch_events)
