# -*- coding: utf-8 -*-

from pymongo import MongoClient


client = MongoClient()
db = client['github']
watch_events = db['watch_events']

db.watch_events.aggregate([
    {'$group': {
        '_id': '$actor',
        'starred': {
            '$push': {
                'repo': '$repo',
                'created_at': '$created_at'
            }
        }}},
    {'$project': {'_id': False, 'name': '$_id', 'starred': True}},
    {'$out': 'actors'}], allowDiskUse=True)
