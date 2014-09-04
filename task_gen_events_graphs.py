# -*- coding: utf-8 -*-

from pymongo import MongoClient
from underscore import _ as us
# from multiprocessing import Pool
from graph_tool.all import Graph
import cPickle as pickle
from fib import fib
import gc


gc.disable()

client = MongoClient()
db = client['github']
watch_events = db['watch_events']


def gen_graph((repo, events)):
    graph = Graph()

    repo_on_graph = graph.new_graph_property('string')
    repo_on_graph[graph] = repo
    graph.graph_properties['repo_on_graph'] = repo_on_graph

    language_on_graph = graph.new_graph_property('string')
    language_on_graph[graph] = events[0]['language']
    graph.graph_properties['language_on_graph'] = language_on_graph

    events_on_vertices = graph.new_vertex_property('object')
    graph.vertex_properties['events_on_vertices'] = events_on_vertices

    actors_on_vertices = graph.new_vertex_property('string')
    graph.vertex_properties['actors_on_vertices'] = actors_on_vertices

    weights_on_edges = graph.new_edge_property('long double')
    graph.edge_properties['weights_on_edges'] = weights_on_edges

    # pre_vertices = []
    pre_events_map = {}
    pre_vertices_map = {}

    # owner_vertex = graph.add_vertex()
    # owner = repo.split('/')[0]
    # actors_on_vertices[owner_vertex] = owner
    # pre_vertices_map[owner] = owner_vertex

    events = sorted(events, key=lambda x: x['created_at'])

    for event in events:
        actor = event['actor']

        if actor in pre_events_map:
            continue

        created_at = event['created_at']

        vertex = graph.add_vertex()
        events_on_vertices[vertex] = event
        actors_on_vertices[vertex] = actor

        if 'following' not in event:
            continue

        following = set(event['following'])
        commons = following.intersection(pre_vertices_map.keys())

        # pre_vertices.append(vertex)

        # if len(commons) == 0:
        #     edge = graph.add_edge(vertex, owner_vertex)
        #     weights_on_edges[edge] = 1.0

        for pre_actor in commons:
            edge = graph.add_edge(vertex, pre_vertices_map[pre_actor])
            interval =\
                (created_at - pre_events_map[pre_actor]['created_at']).days
            weight = 1.0 / fib(interval + 2)
            weights_on_edges[edge] = weight

        pre_events_map[actor] = event
        pre_vertices_map[actor] = vertex

    return graph


graphs = map(gen_graph, us.groupBy(list(watch_events.find(
    {'repo-disabled': {'$exists': False}})), 'repo').items())

print 'gen completed'
print 'graph count:', len(graphs)

pickle.dump(graphs, open('pickle/graphs', 'wb'), True)

print 'pickle completed'
