# -*- coding: utf-8 -*-

from graph_tool.centrality import pagerank
from pymongo import MongoClient
from more_itertools import flatten
import pickle
import gc


gc.disable()

graphs = pickle.load(open('pickle/graphs', 'rb'))
client = MongoClient()
db = client['github']
pageranks = db['pageranks']


def gen_pagerank_maps(graph):
    pr = pagerank(
        graph, weight=graph.edge_properties['weights_on_edges'])

    pr.a /= pr.a.min()
    graph.vertex_properties['pagerank'] = pr

    pr_maps = [{
        'repo': graph.graph_properties['repo_on_graph'],
        'language': graph.graph_properties['language_on_graph'],
        'actor': graph.vertex_properties['actors_on_vertices'][vertex],
        'centrality': pr[vertex]} for vertex in graph.vertices()]

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
