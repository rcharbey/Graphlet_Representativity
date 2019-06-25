#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 08:40:25 2019

@author: raphael charbey
"""

import argparse
from os import makedirs, listdir
import csv

from igraph import Graph

from enumeration import Enumerate
from graphlet_computations import Representativity
from kMeans import kmeans
from kiviat import kiviat

class Representativity_process(object):
    def __init__(self, args):
        self.Data = args['folder']
        self.k = args['k']
        self.Results = 'Results_%s' % self.k
        makedirs(self.Results + '/Positions', exist_ok = True)
        makedirs(self.Results + '/Clusterings', exist_ok = True)
        self.graphlet_range = {4 : range(3, 9), 5 : range(9, 30)}[self.k]
        self.position_range = {4 : range(4, 15), 5 : range(15, 72)}[self.k]
        self.nb_clusters = args['clusters']
        
    def import_graph(self, graph_loc):
        extension = graph_loc.split('.')[-1]
        if extension == 'edgelist':
            return Graph.Read_Edgelist(graph_loc)
        elif extension == 'gml':
            return Graph.Read_GML(graph_loc)
        elif extension == 'graphml':
            return Graph.Read(graph_loc)
        elif extension == 'dl':
            with open(graph_loc, 'r') as to_read:
                data_reached = False
                edge_list = []
                for line in to_read:
                    if data_reached:
                        edge = line.split(' ')[0:2]
                        if edge in edge_list or [edge[1], edge[0]] in edge_list:
                            continue
                        edge_list.append(edge)
                    elif line == 'data:\n':
                        data_reached = True
            return Graph.TupleList(edge_list, directed = False)
        
    
    def write_header(self):
        if not 'graphlets_per_graph.csv' in listdir(self.Results):
            with open(self.Results + '/graphlets_per_graph.csv', 'w') as to_write:
                csvw = csv.writer(to_write, delimiter = ';')
                csvw.writerow(['graph'] + ['graphlet_%s' % i for i in self.graphlet_range])
    
    def get_already_computed_graphs(self):
        self.graphlets_per_graph = {}
        with open(self.Results + '/graphlets_per_graph.csv', 'r') as to_read:
            csvr = csv.reader(to_read, delimiter = ';')
            next(csvr)
            for line in csvr:
                graph_name, graphlets = line[0], [int(x) for x in line[1:]]
                self.graphlets_per_graph[graph_name] = graphlets
        
    def compute_graphlets(self):
    
        self.write_header()
        self.get_already_computed_graphs()
    
        for graph_file in listdir(self.Data):
            if graph_file in self.graphlets_per_graph:
                continue
                
            graph = self.import_graph(self.Data + '/' + graph_file)
            
            graphlets, positions = Enumerate(graph, self.k).characterize_with_patterns()
            temp_graphlets = [graphlets[i] for i in self.graphlet_range]
            if sum(temp_graphlets) == 0:
                continue
            self.graphlets_per_graph[graph_file] = temp_graphlets
            
            with open(self.Results + '/graphlets_per_graph.csv', 'a') as to_write:
                csvw = csv.writer(to_write, delimiter = ';')
                csvw.writerow([graph_file] + self.graphlets_per_graph[graph_file])
        
            with open(self.Results + '/Positions/%s.csv' % graph_file, 'w') as to_write:
                csvw = csv.writer(to_write, delimiter = ';')
                csvw.writerow(['vertex'] + ['position %i' % i for i in self.position_range])
                for v in graph.vs:
                    name = v['name']
                    csvw.writerow([name] + [positions[v.index][i] for i in self.position_range])
                    
    def compute_representativities(self):
        self.representativities = Representativity(self.graphlets_per_graph).compute()
        
    def produce_clusterings(self): 
        km = kmeans(self.representativities, self.graphlets_per_graph, self.nb_clusters)
        km.to_string()   
        labels = km.compute()
        
        folder = self.Results + '/Clusterings/%s_classes' % self.nb_clusters
        if not '%s_classes' % self.nb_clusters in listdir(self.Results + '/Clusterings/'):
            makedirs(folder, exist_ok = True)    
            
        km.write_results(folder)
        
        radar = kiviat(folder)
        radar.plot_kiviat()
                    
    def process(self):
        self.compute_graphlets()
        self.compute_representativities()
        self.produce_clusterings()
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='graphlet arguments')
    parser.add_argument('folder', type=str,
                        help='the folder containing the graphs')
    parser.add_argument('k', type=int,
                        help='the graphlet size')
    parser.add_argument('clusters', type=int,
                        help='the number of resulting clusters')
    args = vars(parser.parse_args())
    Representativity_process(args).process()
        