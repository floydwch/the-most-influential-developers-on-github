# -*- coding: utf-8 -*-

from pymongo import MongoClient


client = MongoClient()
db = client['github']
watch_events = db['watch_events']

db.watch_events.aggregate([
    {'$group': {
        '_id': '$repo',
        'stargazers': {
            '$push': {
                'actor': '$actor',
                'created_at': '$created_at'
            }
        }}},
    {'$project': {'_id': False, 'name': '$_id', 'stargazers': True}},
    {'$out': 'repos'}], allowDiskUse=True)
