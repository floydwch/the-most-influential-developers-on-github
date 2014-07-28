# -*- coding: utf-8 -*-


def grab():
    from gzip import GzipFile
    from urlgrabber import urlopen
    import json

    url = 'http://data.githubarchive.org/2011-02-12-0.json.gz'

    with GzipFile(fileobj=urlopen(url)) as gz_file:
        events = map(json.loads, list(gz_file))
        watch_events = filter(lambda x: x['type'] == 'WatchEvent', events)
        print watch_events


grab()
