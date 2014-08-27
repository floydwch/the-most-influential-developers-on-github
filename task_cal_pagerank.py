# -*- coding: utf-8 -*-

from graph_tool.centrality import pagerank
from pymongo import MongoClient
from more_itertools import flatten
from multiprocessing import Pool
import cPickle as pickle
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


pool = Pool()
pagerank_maps = list(flatten(pool.map(gen_pagerank_maps, filter(
    lambda x: x.num_vertices(), graphs))))
pool.close()
pool.join()

pickle.dump(graphs, open('pickle/graphs', 'wb'), True)
pageranks.insert(pagerank_maps)
