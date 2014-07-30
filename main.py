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


def field_select(event):
    if event.get('repo', None):
        if type(event['actor']) is unicode:
            return (event['actor'], event['repo']['name'], event['created_at'])
        else:
            return (
                event.get('actor', {}).get('login', None),
                event.get('repo', {}).get('name', None),
                event.get('created_at', None))
    else:
        return (
            event.get('actor', None),
            event.get('repository', {}).get('name', None),
            event.get('created_at', None))


def grab():
    from gzip import GzipFile
    from urlgrabber import urlopen
    from datetime import datetime, timedelta

    from_time = datetime(2011, 2, 12, 0)
    to_time = datetime(2014, 7, 29, 0)
    time_strs = [(from_time + timedelta(hours=x)).strftime(
        '%Y-%m-%d-%-H') for x in range(0, int(
            (to_time - from_time).total_seconds() / 3600))]

    for time_str in time_strs:
        url = 'http://data.githubarchive.org/%s.json.gz' % time_str

        while True:
            try:
                with GzipFile(fileobj=urlopen(url)) as gz_file:
                    events = loads_invalid_obj_list(''.join(
                        map(lambda x: unicode(x, 'ISO-8859-1'), map(
                            lambda x: x.strip(), list(gz_file)))))

                    watch_events = map(field_select, filter(
                        lambda x: x['type'] == 'WatchEvent', events))

                    print watch_events, time_str
            except Exception as e:
                print e
                continue
            break


grab()
