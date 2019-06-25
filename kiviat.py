# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 18:51:03 2019

@author: raphael
"""

# Scripts adapted from : Copyright (C) 2011  Nicolas P. Rougier

import csv
import os
import pdfkit

class kiviat(object):
    def __init__(self, folder):
        self.folder = folder
        self.file_in = folder+'/kmeans_stats.csv'
        self.svg_folder = 'SVG'
        
        self.list_graphlets = {
                6 : [4,5,6,7,8,9],
                21 : [10, 13, 12, 11, 15, 14, 18, 19, 20, 16, 17, 21, 
                          22, 26, 23, 24, 25, 27, 28, 29, 30]
                }

    def get_data(self):
        clusters = {}
                
        with open(self.file_in, 'r') as to_read:
            csv_r = csv.reader(to_read, delimiter = ';') 
            header = next(csv_r)
            
            self.list_graphlets = self.list_graphlets[len(header) - 2]
                
            graphlet_pos = {}       
            for graphlet in self.list_graphlets:
                graphlet_pos[graphlet] = header.index('%s' % graphlet)
            
            nb_clusters = 0
            for line in csv_r:
                clusters[nb_clusters] = {
                    'name' : line[0],
                    'pop' : int(line[1]),
                    'repr' : {
                                graphlet :
                                    float(line[graphlet_pos[graphlet]]) 
                                for graphlet in self.list_graphlets
                    }
                }
                nb_clusters += 1
                
        all_temp = []
        for i in range(nb_clusters):
            all_temp.append(clusters[i])
        
        self.nb_clusters = nb_clusters
        self.axes = [os.path.expanduser('../../../%s/pattern%s.svg' % (self.svg_folder, graphlet)) for graphlet in self.list_graphlets]
        self.data = all_temp
    
    def copy_script_js(self):
        with open('%s/script.js' % (self.folder), 'w') as to_write:
            to_write.write('var w = 500, \n') 
            to_write.write('h = 500;\n')
            to_write.write('var colorscale = d3.scale.category10();\n')
            to_write.write('\n')
            to_write.write('//Legend titles \n')
            to_write.write('var LegendOptions = [')
            for i in range(self.nb_clusters):
                to_write.write('\'%s-%s\'' % (self.data[i]['name'], self.data[i]['pop']))
                if i < self.nb_clusters-1:
                    to_write.write(',')
            to_write.write(']; \n')
            to_write.write('//Data \n')
            to_write.write('var d = [\n')
            to_write.write('    [\n')
            for i in range(self.nb_clusters):
                cluster = self.data[i]['repr']
                for j, graphlet in enumerate(self.list_graphlets):
                    if j == len(self.list_graphlets)-1:
                        to_write.write('                {axis:"%s",value:%s}\n' % (self.axes[j], cluster[graphlet]))
                        if i == self.nb_clusters-1:
                            to_write.write(']\n')
                        else:
                            to_write.write('],[\n')
                    else:
                        to_write.write('                {axis:"%s",value:%s},\n' % (self.axes[j], cluster[graphlet]))
    
            to_write.write(' ]; \n')
            to_write.write(' //Options for the Radar chart, other than default\n')
            to_write.write(' var mycfg = {\n')
            to_write.write('   w: w,\n')
            to_write.write('   h: h,\n')
            to_write.write('   maxValue: 2,\n')
            to_write.write('   levels: 6,\n')
            to_write.write('   ExtraWidthX: 300\n }\n')
            to_write.write(' \n')
            to_write.write(' //Call function to draw the Radar chart\n')
            to_write.write(' //Will expect that data is in %\'s\n')
            to_write.write('RadarChart.draw("#chart", d, mycfg);\n')
    
            to_write.write('////////////////////////////////////////////\n')
            to_write.write('/////////// Initiate legend ////////////////\n')
            to_write.write('////////////////////////////////////////////\n')
    
            to_write.write('var svg = d3.select(\'#body\')\n ')
            to_write.write('    .selectAll(\'svg\')\n ')
            to_write.write('    .append(\'svg\')\n ')
            to_write.write('    .attr("width", w+300)\n ')
            to_write.write('    .attr("height", h+300)\n ')
            to_write.write('//Initiate Legend\n ')
            to_write.write('var legend = svg.append("g")\n ')
            to_write.write('    .attr("class", "legend")\n ')
            to_write.write('    .attr("height", 200)\n ')
            to_write.write('    .attr("width", 400)\n ')
            to_write.write('    .attr(\'transform\', \'translate(210,20)\') \n ')
            to_write.write('    ;\n ')
            to_write.write('    //Create colour squares\n ')
            to_write.write('    legend.selectAll(\'rect\')\n ')
            to_write.write('    .data(LegendOptions)\n ')
            to_write.write('      .enter()\n ')
            to_write.write('      .append("rect")\n ')
            to_write.write('      .attr("x", w - 65)\n ')
            to_write.write('      .attr("y", function(d, i){ return i * 20;})\n ')
            to_write.write('      .attr("width", 16)\n ')
            to_write.write('      .attr("height", 16)\n ')
            to_write.write('      .style("fill", function(d, i){ return colorscale(i);})\n ')
            to_write.write('      ;\n ')
            to_write.write('    //Create text next to squares\n ')
            to_write.write('    legend.selectAll(\'text\')\n ')
            to_write.write('      .data(LegendOptions)\n ')
            to_write.write('      .enter()\n ')
            to_write.write('      .append("text")\n ')
            to_write.write('      .attr("x", w - 48)\n ')
            to_write.write('      .attr("y", function(d, i){ return i * 20 + 15;})\n ')
            to_write.write('      .attr("font-size", "20px")\n ')
            to_write.write('      .attr("fill", "#737373")\n ')
            to_write.write('      .text(function(d) { return d; })\n')
            to_write.write('      ;')
            
    def copy_radar_chart_js(self):
        with open('%s/../RadarChart.js' % self.folder, 'w') as to_write:
                with open('RadarChart.js', 'r') as to_read:
                    for line in to_read:
                        to_write.write(line) 
                        
    def copy_kiviat(self):            
        with open('%s/Kiviat.html' % (self.folder), 'w') as to_write:
            to_write.write('<!DOCTYPE html>\n')
            to_write.write('<html>\n')
            to_write.write('<head>\n')
            to_write.write('<meta http-equiv="Content-Type" content="text/html;charset=utf-8"/>\n')
            to_write.write('<title>Radar chart</title>\n')
            to_write.write('<script src="http://d3js.org/d3.v3.min.js"></script>\n')
            to_write.write('	<script src="../RadarChart.js"></script>\n')
            to_write.write('	<style>\n')
            to_write.write('		body {\n')
            to_write.write('		  overflow: hidden;\n')
            to_write.write('		  margin: 0;\n')
            to_write.write('		  font-size: 18px;\n')
            to_write.write('		  font-family: "Helvetica Neue", Helvetica;\n')
            to_write.write('		}\n')
            to_write.write('		#chart {\n')
            to_write.write('		  position: absolute;\n')
            to_write.write('		  top: 100px;\n')
            to_write.write('		  left: 100px;\n')
            to_write.write('		}	\n')
            to_write.write('		div.p6 {\n')
            to_write.write('		  position: absolute;\n')
            to_write.write('		  top: 133px;\n')
            to_write.write('		  left: 375px;\n')
            to_write.write('		}	  \n')
            to_write.write('	</style>\n')
            to_write.write('  </head>\n')
            to_write.write('  <body>\n')
            to_write.write('    <div id="body">\n')
            to_write.write('	  <div id="chart"></div>\n')
            to_write.write('    </div>\n')
            to_write.write('	\n')
            to_write.write('    <script type="text/javascript" src="script.js"></script>\n')
            to_write.write('  </body>\n')
            to_write.write('</html>\n')
            
            
    def plot_kiviat(self): 
            
        self.get_data()
        self.copy_script_js()
        self.copy_kiviat()
        self.copy_radar_chart_js()
        file_in = self.folder + '/Kiviat.html'
        file_out = self.folder + '/../Kiviat_%s.pdf' % self.nb_clusters
        pdfkit.from_url(file_in, file_out)
        
        
        
if __name__ == '__main__':
    kiviat('../Classes').plot_kiviat()