# -*- coding: utf-8 -*-

from datetime import datetime
from multiprocessing import Pool
from threading import Thread
import logging
from pymongo import MongoClient
from random import shuffle


FROM_TIME = datetime(2011, 2, 12, 0)
TO_TIME = datetime(2014, 8, 1, 22)
# CHUNK_SIZE = 60
THREAD_NUMBER = 120

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
                event.get('repo', {}).get(
                    'name', event.get('payload', {}).get('repo', None)),
                event.get('created_at', None))

            if event.get('repo', {}).get('name', None) == '/':
                refined = (
                    refined[0],
                    event.get('payload', {}).get('repo', None),
                    refined[2])
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
                    event.get('repository', {})['owner'] + '/'
                    + event.get('repository', {})['name'],
                    event.get('repository', {}).get('name', None),
                    event.get('created_at', None))
            else:
                refined = (
                    event.get('actor', None),
                    None,
                    event.get('created_at', None))

    if refined[1]:
        owner, name = refined[1].split('/')

    if refined[1] is None or len(owner) == 0 or len(name) == 0:
        if event.get('url', None):
            split_url = event['url'].split('/')

            if split_url[0] == 'https:' and \
                    split_url[1] == '' and \
                    split_url[2] == 'github.com' and \
                    len(split_url[3]) > 0 and \
                    len(split_url[4]) > 0:

                refined = (
                    refined[0],
                    split_url[3] + '/' + split_url[4],
                    refined[2])

    if refined[1] == '/':
        refined = (refined[0], None, refined[2])

    extraction = dict(zip(['actor', 'repo', 'created_at'], refined))

    if None in refined:
        thread = Thread(
            target=defects.insert,
            args={'event': event, 'extraction': extraction})
        thread.start()

    return extraction


def grab(number):
    from gzip import GzipFile
    from urlgrabber import urlopen
    from datetime import timedelta

    time_str = (FROM_TIME + timedelta(hours=number)).strftime('%Y-%m-%d-%-H')

    if processed_times.find(
            {'time': time_str, 'status': 'ok'}).count():  # already grab
        return

    url = 'http://data.githubarchive.org/%s.json.gz' % time_str

    for i in xrange(10):  # retry 10 times
        try:
            with GzipFile(fileobj=urlopen(url)) as gz_file:
                events = loads_invalid_obj_list(''.join(
                    map(lambda x: unicode(x, 'ISO-8859-1'), map(
                        lambda x: x.strip(), list(gz_file)))))

                new_watch_events = filter(
                    lambda x: None not in x.values(), map(field_select, filter(
                        lambda x: x['type'] == 'WatchEvent', events)))

                thread = Thread(
                    target=watch_events.insert, args=new_watch_events)
                thread.start()

                thread = Thread(
                    target=processed_times.insert,
                    args={'time': time_str, 'status': 'ok'})
                thread.start()
        except Exception as e:
            logging.warning(str(e) + ' -- ' + url)
            continue
        break
    else:
        thread = Thread(
            target=processed_times.insert,
            args={'time': time_str, 'status': 'error'})
        thread.start()


numbers = range(int((TO_TIME - FROM_TIME).total_seconds() / 3600))
shuffle(numbers)

pool = Pool(THREAD_NUMBER)
pool.map(grab, numbers)
pool.close()
pool.join()
