# -*- coding: utf-8 -*-

from graph_tool.centrality import pagerank
from pymongo import MongoClient
from more_itertools import flatten
from multiprocessing import Pool
import cPickle as pickle
import gc


gc.disable()

DAMPING = 0.85

graphs = pickle.load(open('pickle/graphs', 'rb'))
client = MongoClient()
db = client['github']
pageranks = db['pageranks']


def gen_pagerank_maps(graph):
    pr = pagerank(
        graph, weight=graph.edge_properties['weights_on_edges'])

    dangling_vertices = filter(lambda x: x.out_degree() == 0, graph.vertices())
    low_pr = (1 / graph.num_vertices()) * (DAMPING + (1 - DAMPING) * sum(
        map(lambda x: pr[x], dangling_vertices)))

    pr.a /= low_pr
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
