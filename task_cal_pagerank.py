# -*- coding: utf-8 -*-

from graph_tool.centrality import pagerank
from pymongo import MongoClient
from more_itertools import flatten
import pickle
import gc


gc.disable()


def gen_pagerank(graph):
    if graph.num_edges():
        pr = pagerank(
            graph, weight=graph.edge_properties['weights_on_edges'])
    else:
        pr = pagerank(graph)

    pr.a /= pr.a.min()
    graph.vertex_properties['pagerank'] = pr

    return graph


def gen_pagerank_maps(graph):
    pr_maps = [{
        'repo': graph.graph_properties['repo_on_graph'],
        'language': graph.graph_properties['language_on_graph'],
        'actor': graph.vertex_properties['actors_on_vertices'][vertex],
        'pagerank': graph.vertex_properties['pagerank'][vertex]}
        for vertex in graph.vertices()]

    return pr_maps


def main():
    graphs = pickle.load(open('pickle/graphs', 'rb'))
    client = MongoClient()
    db = client['github']
    pageranks = db['pageranks']

    pagerank_maps = list(flatten(map(gen_pagerank_maps, graphs)))

    pickle.dump(graphs, open('pickle/graphs-pageranks', 'wb'), 2)
    pageranks.insert(pagerank_maps)


if __name__ == '__main__':
    main()
