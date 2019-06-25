# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 10:04:53 2019

@author: raphael charbey
"""

from igraph import Graph

class Enumerate(object):
    
    
    def __init__(self, graph, k):
        
        self._k = k
    
        self.dict_patterns = {
            '[1, 1]' : 1,
            '[1, 1, 2]' : 2,
            '[2, 2, 2]' : 3,
            '[1, 1, 2, 2]' : 4,
            '[1, 1, 1, 3]' : 5,
            '[1, 2, 2, 3]' : 6,
            '[2, 2, 2, 2]' : 7,
            '[2, 2, 3, 3]' : 8,
            '[3, 3, 3, 3]' : 9,
            '[1, 1, 2, 2, 2]' : 10,
            '[1, 1, 1, 1, 4]' : 11,
            '[1, 1, 1, 2, 3]' : 12,
            '[1, 2, 2, 2, 3]' : (1,2,(13,17)),
            '[1, 1, 2, 3, 3]' : 14,
            '[1, 1, 2, 2, 4]' : 15,
            '[2, 2, 2, 2, 2]' : 16,
            '[1, 2, 3, 3, 3]' : 18,
            '[1, 2, 2, 3, 4]' : 19,
            '[2, 2, 2, 2, 4]' : 20,
            '[2, 2, 2, 3, 3]' : (3,3,(21,22)),
            '[1, 3, 3, 3, 4]' : 23,
            '[2, 2, 3, 3, 4]' : 24,
            '[2, 2, 2, 4, 4]' : 25,
            '[2, 3, 3, 3, 3]' : 26,
            '[3, 3, 3, 3, 4]' : 27,
            '[2, 3, 3, 4, 4]' : 28,
            '[3, 3, 4, 4, 4]' : 29,
            '[4, 4, 4, 4, 4]' : 30
        }

        self.dict_positions = [
            {1 : 1}, #1
            {1 : 2, 2 : 3}, #2
            {2 : 4}, #3
            {1 : 5, 2: 6}, #4
            {1 : 7, 3 : 8}, #5
            {1 : 9, 2 : 10, 3 : 11}, #6
            {2 : 12},#7
            {2 : 13, 3 : 14},#8
            {3 : 15},#9
            {1 : 16, 2 : (1,(17,18))},#10
            {1 : 19, 4 : 20},#11
            {1 : (2,(21,22)), 2 : 23, 3 : 24},#12
            {1 : 25, 2 : (1,(26,27)), 3 : 28},#13
            {1 : 29, 2 : 30, 3 : 31},#14
            {1 : 32, 2 : 33, 4 : 34},#15
            {2 : 35},#16
            {1 : 36, 2 : (3,(38,37)), 3 : 39},#17
            {1 : 40, 2 : 41, 3 : (1,(42,43))},#18
            {1 : 44, 2 : 45, 3 : 46, 4 : 47},#19
            {2 : 48, 4 : 49},#20
            {2 : (2,(50, 51)), 3 : 52},#21
            {2 : 53, 3 : 54},#22
            {1 : 55, 3 : 56, 4 : 57},#23
            {2 : 58, 3 : 59, 4 : 60},#24
            {2 : 61, 4 : 62},#25
            {2 : 63, 3 : (2,(64,65))},#26
            {3 : 66, 4 : 67},#27
            {2 : 68, 3 : 69, 4 : 70},#28
            {3 : 71, 4 : 72},#29
            {4 : 73}#30
        ]

        self.patterns_tab = []
        self.positions_tab = []
        self._graph = graph

    def create_list_neighbors(self):
        for v in self._graph.vs:
            v['list_neighbors'] = []
        for e in self._graph.es:
            if not e.source in self._graph.vs[e.target]['list_neighbors']:
                self._graph.vs[e.target]['list_neighbors'].append(e.source)
            if not e.target in self._graph.vs[e.source]['list_neighbors']:
                self._graph.vs[e.source]['list_neighbors'].append(e.target)
        for v in self._graph.vs:
            v['list_neighbors'].sort(reverse = True)

    def degree_distribution(self, graph_sub):
        result = []
        for v in graph_sub.vs:
            result.append(v.degree())
            v['d'] = result[v.index]
        result.sort()
        return result

    def disambiguate_pattern(self, graph_sub, new_pattern):
        for v in graph_sub.vs:
            if v['d'] == new_pattern[0]:
                for n in v.neighbors():
                    if n['d'] == new_pattern[1]:
                        return new_pattern[2][0]
        return new_pattern[2][1]

    def disambiguate_position(self, graph_sub, v, new_position):
        for n in v.neighbors():
            if n['d'] == new_position[0]:
                return new_position[1][0]
        return new_position[1][1]

    def index_pattern(self, graph_sub):
        new_pattern = self.dict_patterns[str(self.degree_distribution(graph_sub))]
        if type(new_pattern) != int :
            new_pattern = self.disambiguate_pattern(graph_sub, new_pattern)
        self.patterns_tab[new_pattern - 1] += 1
        new_positions = self.dict_positions[new_pattern - 1]
        if new_pattern in [10, 12, 13, 17, 18, 21, 26] :
            for v in graph_sub.vs:
                new_position = new_positions[v['d']]
                if type(new_position) != int:
                    new_position = self.disambiguate_position(graph_sub, v, new_positions[v['d']])
                self.positions_tab[v['id_principal']][new_position - 1] += 1
        else:
            for v in graph_sub.vs:
                self.positions_tab[v['id_principal']][new_positions[v['d']] - 1] += 1

    def in_neighborhood_vsub(self, list_neighbors, length_vsub):
        for n in list_neighbors:
            if self._graph.vs[n]['id_sub'] != -1 and self._graph.vs[n]['id_sub'] != length_vsub-1:
                return True
        return False

    def add_vertex(self, graph_sub, vertex):
        vertex['id_sub'] = len(graph_sub.vs)
        graph_sub.add_vertex(name = vertex['name'], **{'id_principal' : vertex.index})

    def extend_subgraph(self, graph_sub, v, vext):
        if len(graph_sub.es) > 0 :
            self.index_pattern(graph_sub)
        if len(graph_sub.vs) == self._k:
            return
        while vext:
            w = vext.pop()
            vext2 = list(vext)
            self.add_vertex(graph_sub, w)
            for nei in w['list_neighbors']:
                u = self._graph.vs[nei]
                if u.index >= v.index:
                    if u['id_sub'] == -1 :
                        if not self.in_neighborhood_vsub(u['list_neighbors'], len(graph_sub.vs)):
                            vext2.append(u)
                    else:
                        graph_sub.add_edge(len(graph_sub.vs) - 1, u['id_sub'])
                else:
                    break

            self.extend_subgraph(graph_sub, v, vext2)
            graph_sub.delete_vertices(w['id_sub'])
            w['id_sub'] = -1

    def characterize_with_patterns(self):
        self.create_list_neighbors()
        self.patterns_tab = 30*[0]
        for v in self._graph.vs:
            self.positions_tab.append(73*[0])
            v['id_sub'] = -1
        for v in self._graph.vs:

            graph_sub = Graph.Formula()
            v['id_sub'] = 0
            if not 'name' in v.attributes():
                v['name'] = str(v.index)
            graph_sub.add_vertex(name = v['name'], **{'id_principal' : v.index, 'evol_class' : 1, 'pattern_sub' : 0})

            vext = []
            for nei in v['list_neighbors']:
                if nei > v.index:
                    vext.append(self._graph.vs[nei])

            if len(vext) > 0:
                self.extend_subgraph(graph_sub, v, vext)
            v['id_sub'] = -1
        return (self.patterns_tab, self.positions_tab)