# -*- coding: utf-8 -*-

from pymongo import MongoClient
from graph_tool.all import graph_draw, sfdp_layout
from funcy import group_by
from PIL import Image
from images2gif import writeGif
from task_gen_events_graphs import gen_graph
from task_cal_pagerank import gen_pagerank
import sys
import os
import gc


gc.disable()
sys.setrecursionlimit(100000)


def draw_graph(graph):
    vertices_names = graph.new_vertex_property('string')

    for vertex in graph.vertices():
        vertices_names[vertex] = \
            graph.vertex_properties['actors_on_vertices'][vertex] + \
            ' ' + str(graph.vertex_properties['pagerank'][vertex])

    pos = sfdp_layout(graph, eweight=graph.edge_properties['weights_on_edges'])

    graph_draw(
        graph,
        pos=pos,
        vertex_fill_color=graph.vertex_properties['pagerank'],
        vertex_text=vertices_names,
        vertex_font_size=5,
        output_size=(1024, 1024),
        output='pagerank/' +
        graph.graph_properties['repo_on_graph'].replace('/', '%') + '.pdf')


def draw_graph_frame((graph, dir_name, number)):
    vertices_filter = graph.new_vertex_property('bool')

    for i in xrange(len(vertices_filter.a)):
        if i < number:
            vertices_filter.a[i] = True
        else:
            vertices_filter.a[i] = False

    graph.set_vertex_filter(vertices_filter)
    graph_draw(
        graph,
        pos=graph.vertex_properties['pos'],
        vertex_fill_color=graph.vertex_properties['pagerank'],
        vertex_size=5,
        output_size=(1024, 1024),
        output=dir_name + str(number) + '.png')


def draw_graph_animation(graph):
    vertices_names = graph.new_vertex_property('string')
    graph.vertex_properties['vertices_names'] = vertices_names

    for vertex in graph.vertices():
        vertices_names[vertex] = \
            graph.vertex_properties['actors_on_vertices'][vertex] + \
            ' ' + str(graph.vertex_properties['pagerank'][vertex])

    graph.vertex_properties['pos'] = sfdp_layout(
        graph, eweight=graph.edge_properties['weights_on_edges'])

    dir_name = 'pagerank/' + \
        graph.graph_properties['repo_on_graph'].replace('/', '%') + '/'

    os.mkdir(dir_name)

    def event_bulk(vertex):
        event = graph.vertex_properties['events_on_vertices'][vertex]
        return event['created_at'].strftime("%Y-%m-%d %H")

    batch_sizes = map(lambda x: len(x[1]), sorted(group_by(
        event_bulk, graph.vertices()).items(), key=lambda x: x[0]))

    def tail_number(n):
        if n == 0:
            return batch_sizes[0]
        else:
            return tail_number(n - 1) + batch_sizes[n]

    batch_numbers = map(tail_number, range(len(batch_sizes)))

    map(draw_graph_frame, map(
        lambda x: (graph, dir_name, x), batch_numbers))

    images = [Image.open(dir_name + str(i) + '.png') for i in batch_numbers]

    writeGif(dir_name + 'animation.gif', images, duration=0.1)


def main(repo):
    client = MongoClient()
    db = client['github']
    events = list(db['watch_events'].find(
        {'repo-disabled': {'$exists': False}, 'repo': repo},
        {'actor': True, 'created_at': True,
            'actor-following': True, 'language': True}))

    graph = gen_pagerank(gen_graph((repo, events)))
    draw_graph_animation(graph)


if __name__ == '__main__':
    main(sys.argv[1])
