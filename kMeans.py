# -*- coding: utf-8 -*-
"""
Created on Thu Jan 31 20:27:15 2019

@author: raphael
"""

import csv
import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
from sklearn.metrics import silhouette_samples
from graphlet_computations import Global_frequency, Representativity

class kmeans(object):
    def __init__(self, data, graphlets_per_graph, nb_classes):
        self.data = pd.DataFrame.from_dict(data, orient = 'index')
        self.graph_names = list(self.data.index)
        self.k = {6 : 4, 21 : 5}[len(list(graphlets_per_graph.values())[0])]
        self.graphlets_ok = {0 : [], 1 : [], 2 : [1], 3 : [2,3], 4 : range(4, 10), 5 : range(10, 31)}[self.k]
        self.graphlets_per_graph = graphlets_per_graph
        self.global_freq = Global_frequency(self.graphlets_per_graph)
        self.nb_classes = nb_classes
        
    def to_string(self):
        print('kmeans, k = %s, datasize = %s' % (self.nb_classes, len(self.graph_names)))
        #for gname in self.graph_names:
        #    print gname
            
    def get_class_representativity(self, this_class_graphs):
        class_rep = Representativity(self.graphlets_per_graph, graphs = this_class_graphs).compute_class()        
        return class_rep
        
    def compute(self):        
        s_max, labels_max = 0, False
        cluster_centers_max = False
        for i in range(100):
            kmeans = KMeans(n_clusters = self.nb_classes)
            kmeans.fit(self.data)
            s = np.average(silhouette_samples(self.data, kmeans.labels_))
            if s > s_max:
                labels_max = kmeans.labels_
                cluster_centers_max = kmeans.cluster_centers_
                s_max = s
            
        self.graphs_per_class = {}
        for i in range(self.nb_classes):
            self.graphs_per_class[i] = []
            
        class_per_graph = {}
        for i, graph in enumerate(self.graph_names):
            self.graphs_per_class[labels_max[i]].append(graph)
            class_per_graph[graph] = labels_max[i]
        
        self.cluster_centers = cluster_centers_max  
        return class_per_graph
                    
    def write_results(self, folder):
        self.repr_per_classe = {}
        for classe in self.graphs_per_class:
            self.repr_per_classe[classe] = self.get_class_representativity(self.graphs_per_class[classe])['class']            
                
        with open('%s/kmeans_stats.csv' % folder, 'w') as to_write:
            csv_w = csv.writer(to_write, delimiter = ';')
            csv_w.writerow(['classe', 'effectifs']  + [i for i in self.graphlets_ok])
            classe_par_taille = list(self.graphs_per_class.keys())
            classe_par_taille.sort(key = lambda classe : len(self.graphs_per_class[classe]))
            for classe in classe_par_taille:
                nb = len(self.graphs_per_class[classe])
                csv_w.writerow([classe, nb] + self.repr_per_classe[classe])
    
        with open('%s/typo_per_graph.csv' % folder, 'w') as to_write:
            csv_w = csv.writer(to_write, delimiter =';')
            csv_w.writerow(['ego', 'class'])
            for classe in self.graphs_per_class:
                for graph_name in self.graphs_per_class[classe]:
                    csv_w.writerow([graph_name, classe])