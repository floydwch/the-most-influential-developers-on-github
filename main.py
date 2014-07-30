# -*- coding: utf-8 -*-


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


def event_check(event):
    if event['type'] != 'WatchEvent':
        return False
    # if event.get('actor', False) is False:
    #     return False
    if type(event['actor']) is dict:
        if event['actor'].get('login', False) is False:
            return False

    return True


def field_select(event):
    if event.get('repo', False):
        if type(event['actor']) is unicode:
            return (event['actor'], event['repo']['name'], event['created_at'])
        else:
            return (
                event['actor']['login'],
                event['repo']['name'],
                event['created_at'])
    else:
        return (
            event['actor'],
            event['repository']['name'],
            event['created_at'])


def grab():
    from gzip import GzipFile
    from urlgrabber import urlopen
    from datetime import datetime, timedelta

    # from_time = datetime(2011, 2, 12, 0)
    # from_time = datetime(2011, 3, 15, 21)
    from_time = datetime(2014, 7, 27, 0)
    to_time = datetime(2014, 7, 29, 0)
    time_strs = [(from_time + timedelta(hours=x)).strftime(
        '%Y-%m-%d-%-H') for x in range(0, int(
            (to_time - from_time).total_seconds() / 3600))]

    for time_str in time_strs:
        url = 'http://data.githubarchive.org/%s.json.gz' % time_str

        with GzipFile(fileobj=urlopen(url)) as gz_file:
            events = loads_invalid_obj_list(''.join(
                map(lambda x: unicode(x, 'ISO-8859-1'), map(
                    lambda x: x.strip(), list(gz_file)))))

            well_defined_events = filter(event_check, events)
            watch_events = map(field_select, well_defined_events)

            print watch_events, time_str
            # print (map(lambda x: x[1].get('login', False), watch_events))


grab()
