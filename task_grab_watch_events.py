# -*- coding: utf-8 -*-

from gevent.pool import Pool as GPool
from pymongo import MongoClient
from datetime import datetime
from multiprocessing.pool import ThreadPool
from multiprocessing import Pool
from threading import Thread
import logging
from pymongo.errors import AutoReconnect
from random import shuffle
import arrow
from arrow.parser import ParserError
from more_itertools import flatten
from github import Github
from github.GithubException import UnknownObjectException, GithubException
from config import users
from math import ceil
from underscore import _ as us
from functools import partial
import random
import gc


gc.disable()

FROM_TIME = datetime(2014, 5, 23, 0)
TO_TIME = datetime(2014, 8, 23, 0)
THREAD_NUMBER = 20
MONGO_MAX_POOL_SIZE = 800

logging.basicConfig(filename='grab.log', level=logging.WARNING)

client = MongoClient(max_pool_size=MONGO_MAX_POOL_SIZE / THREAD_NUMBER)
db = client['github']
watch_events = db['watch_events']
processed_times = db['processed_times']
defects = db['defects']

githubs = map(lambda x: Github(x['login'], x['passwd']), users)


def items_insert(collection):
    def wrapper(items):
        while True:
            try:
                collection.insert(items)
                break
            except AutoReconnect:
                pass

    return wrapper


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

    try:
        refined = (refined[0], refined[1], arrow.get(refined[2], [
            'YYYY/MM/DD HH:mm:ss Z',
            'YYYY-MM-DDTHH:mm:ssZZ',
            'YYYY-MM-DDTHH:mm:ss']).datetime)
    except ParserError:
        logging.warning('unknown format: ' + refined[2])

    extraction = dict(zip(['actor', 'repo', 'created_at'], refined))

    if None in refined:
        thread = Thread(
            target=items_insert(defects),
            args=({'event': event, 'extraction': extraction}, ))
        thread.start()

    return extraction


def unicode_data_charset(string):
    return unicode(string, 'ISO-8859-1')


def is_not_none(data):
    return None not in data.values()


def strip(string):
    return string.strip()


def is_watch_event(event):
    return event['type'] == 'WatchEvent'


def set_time(time, event):
    event['time'] = time

    return event


def grab(number):
    from gzip import GzipFile
    from urlgrabber import urlopen
    from datetime import timedelta

    time_str = (FROM_TIME + timedelta(hours=number)).strftime('%Y-%m-%d-%-H')

    watch_events = []

    while True:
        try:
            if processed_times.find({
                    'time': time_str, 'status': 'ok'}).count():  # already grab
                return []

            url = 'http://data.githubarchive.org/%s.json.gz' % time_str

            for i in xrange(10):  # retry 10 times
                try:
                    with GzipFile(fileobj=urlopen(url)) as gz_file:
                        events = loads_invalid_obj_list(''.join(
                            map(unicode_data_charset, map(
                                strip, list(gz_file)))))

                        watch_events = filter(
                            is_not_none,
                            map(us.compose(
                                field_select, partial(set_time, time_str)),
                                filter(is_watch_event, events)))

                        if not watch_events:
                            logging.warning(
                                'watch_events is none' + ' -- ' + url)

                        thread = Thread(
                            target=items_insert(processed_times),
                            args=({'time': time_str, 'status': 'ok'}, ))
                        thread.start()

                        break
                except Exception as e:
                    logging.warning(str(e) + ' -- ' + url)
                    continue
                break
            else:
                thread = Thread(
                    target=items_insert(processed_times),
                    args=({'time': time_str, 'status': 'error'}, ))
                thread.start()
            break
        except AutoReconnect:
            pass

    return watch_events


def get_following(actor, get_following, i):
    following_obj = get_following.get_page(i)

    return map(lambda x: x.login, following_obj)


def set_actor_info(events):
    actor = events[0]['actor']
    github_bot_id = random.randrange(len(githubs))
    github = githubs[github_bot_id]

    try:
        actor_obj = github.get_user(actor)
    except UnknownObjectException:
        for event in events:
            event['actor-disabled'] = True
            event['following'] = []
            event['hireable'] = ''
            event['location'] = ''
        return events

    following_count = actor_obj.following
    following_pages = int(ceil(following_count / 30.0))

    get_following_pagination = actor_obj.get_following()

    pool = GPool()
    following = pool.map(partial(
        get_following, actor, get_following_pagination),
        range(following_pages))

    for event in events:
        event['following'] = list(flatten(following))
        event['hireable'] = actor_obj.hireable
        event['location'] = actor_obj.location

    return events


def set_language(events):
    repo = events[0]['repo']
    github_bot_id = random.randrange(len(githubs))
    github = githubs[github_bot_id]

    try:
        repo_obj = github.get_repo(repo)
    except UnknownObjectException:
        for event in events:
            event['repo-disabled'] = True

        return events
    except GithubException:
        for event in events:
            event['repo-disabled'] = True

        return events

    for event in events:
        event['language'] = repo_obj.language

    return events


numbers = range(int((TO_TIME - FROM_TIME).total_seconds() / 3600))
shuffle(numbers)
pool = Pool(20)
new_watch_events = list(flatten(pool.map(grab, numbers)))
pool.close()
pool.join()

print 'original watching event count:', len(new_watch_events)

count = us.countBy(new_watch_events, lambda x, _: x['repo'])
new_watch_events = filter(lambda x: count[x['repo']] > 1, new_watch_events)

print 'more than 1 watching event count:', len(new_watch_events)

pool = ThreadPool(24)
new_watch_events = list(flatten(pool.map(set_actor_info, us.groupBy(
    new_watch_events, 'actor').values())))
pool.close()
pool.join()

pool = ThreadPool(24)
new_watch_events = list(flatten(pool.map(set_language, us.groupBy(
    new_watch_events, 'repo').values())))
pool.close()
pool.join()

watch_events.insert(new_watch_events)

print 'done'
