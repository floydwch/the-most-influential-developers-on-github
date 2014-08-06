# -*- coding: utf-8 -*-

from pymongo import MongoClient


client = MongoClient()
db = client['github']
watch_events = db['watch_events']

db.watch_events.aggregate([
    {'$group': {'_id': '$repo'}},
    {'$project': {'_id': False, 'name': '$_id'}},
    {'$out': 'repos'}])
