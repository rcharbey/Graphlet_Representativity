var w = 500, 
h = 500;
var colorscale = d3.scale.category10();

//Legend titles 
var LegendOptions = ['A-10']; 
//Data 
var d = [
    [
                {axis:"/home/raphael/Graphlets/SVG/pattern10.svg",value:0.947},
                {axis:"/home/raphael/Graphlets/SVG/pattern13.svg",value:0.23},
                {axis:"/home/raphael/Graphlets/SVG/pattern12.svg",value:0.8},
                {axis:"/home/raphael/Graphlets/SVG/pattern11.svg",value:1.479},
                {axis:"/home/raphael/Graphlets/SVG/pattern15.svg",value:0.66},
                {axis:"/home/raphael/Graphlets/SVG/pattern14.svg",value:0.53},
                {axis:"/home/raphael/Graphlets/SVG/pattern18.svg",value:1.39},
                {axis:"/home/raphael/Graphlets/SVG/pattern19.svg",value:0.18},
                {axis:"/home/raphael/Graphlets/SVG/pattern20.svg",value:0.32},
                {axis:"/home/raphael/Graphlets/SVG/pattern16.svg",value:0.86},
                {axis:"/home/raphael/Graphlets/SVG/pattern17.svg",value:0.77},
                {axis:"/home/raphael/Graphlets/SVG/pattern21.svg",value:0.33},
                {axis:"/home/raphael/Graphlets/SVG/pattern22.svg",value:0.21},
                {axis:"/home/raphael/Graphlets/SVG/pattern26.svg",value:1.09},
                {axis:"/home/raphael/Graphlets/SVG/pattern23.svg",value:0.47},
                {axis:"/home/raphael/Graphlets/SVG/pattern24.svg",value:1.56},
                {axis:"/home/raphael/Graphlets/SVG/pattern25.svg",value:0.93},
                {axis:"/home/raphael/Graphlets/SVG/pattern27.svg",value:0.85},
                {axis:"/home/raphael/Graphlets/SVG/pattern28.svg",value:1.62},
                {axis:"/home/raphael/Graphlets/SVG/pattern29.svg",value:1.71},
                {axis:"/home/raphael/Graphlets/SVG/pattern30.svg",value:1.86}
]
 ]; 
 //Options for the Radar chart, other than default
 var mycfg = {
   w: w,
   h: h,
   maxValue: 2,
   levels: 6,
   ExtraWidthX: 300
 }
 
 //Call function to draw the Radar chart
 //Will expect that data is in %'s
 RadarChart.draw("#chart", d, mycfg);
////////////////////////////////////////////
/////////// Initiate legend ////////////////
////////////////////////////////////////////
var svg = d3.select('#body')
     .selectAll('svg')
     .append('svg')
     .attr("width", w+300)
     .attr("height", h+300)
 //Initiate Legend
 var legend = svg.append("g")
     .attr("class", "legend")
     .attr("height", 200)
     .attr("width", 400)
     .attr('transform', 'translate(210,20)') 
     ;
     //Create colour squares
     legend.selectAll('rect')
     .data(LegendOptions)
       .enter()
       .append("rect")
       .attr("x", w - 65)
       .attr("y", function(d, i){ return i * 20;})
       .attr("width", 16)
       .attr("height", 16)
       .style("fill", function(d, i){ return colorscale(i);})
       ;
     //Create text next to squares
     legend.selectAll('text')
       .data(LegendOptions)
       .enter()
       .append("text")
       .attr("x", w - 48)
       .attr("y", function(d, i){ return i * 20 + 15;})
       .attr("font-size", "20px")
       .attr("fill", "#737373")
       .text(function(d) { return d; })
      ;
