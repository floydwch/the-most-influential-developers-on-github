# -*- coding: utf-8 -*-


def grab():
    from gzip import GzipFile
    from urlgrabber import urlopen
    import json

    url = 'http://data.githubarchive.org/2011-02-12-0.json.gz'

    with GzipFile(fileobj=urlopen(url)) as gz_file:
        events = map(json.loads, list(gz_file))
        print events


grab()
