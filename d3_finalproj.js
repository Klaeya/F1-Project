// citation: https://d3-graph-gallery.com/graph/barplot_basic.html
// set the dimensions and margins of the graph
var margin = {top: 30, right: 30, bottom: 100, left: 60},
    width = 1000 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;


// append the svg object to the body of the page
var svg = d3.select("#barplot")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
  .append("g")
    .attr("transform",
          "translate(" + margin.left + "," + margin.top + ")");

d3.csv("constructor_d3_top30.csv").then(function(data){

data.forEach(function(d) {
    d.wins = +d.wins;
});

// X axis
var x = d3.scaleBand()
  .range([ 0, width ])
  .domain(data.map(function(d) {return d.name;}))
  .padding(0.2);
svg.append("g")
  .attr("transform", "translate(0," + height + ")")
  .call(d3.axisBottom(x))
  .selectAll("text")
    .attr("transform", "translate(-10,0)rotate(-45)")
    .style("text-anchor", "end")
    .style("font-family", "Formula1")

// Y axis
var y = d3.scaleLinear()
  .domain([0, 2000])
  .range([ height, 0]);
svg.append("g")
  .call(d3.axisLeft(y));

var color = d3.scaleOrdinal(d3.schemeCategory10);
var nationalities = [...new Set(data.map(d => d.nationality))];

// Y axis label
svg.append("text")
  .attr("transform", "rotate(-90)")  // Rotate text to make it vertical
  .attr("y", 0 - margin.left)        // Position it at the top of the Y-axis
  .attr("x", 0 - height / 2)         // Position it vertically in the middle
  .attr("dy", "1em")                 // Adjust the vertical position
  .style("text-anchor", "middle")    // Center the text horizontally
  .style("font-family", "Formula1")
  .style("font-size", "14px")
  .text("Total Number of Wins");

// Bars
svg.selectAll("mybar")
  .data(data)
  .enter()
  .append("rect")
    .attr("x", function(d) { return x(d.name); })
    .attr("y", function(d) { return y(d.wins); })
    .attr("width", x.bandwidth())
    .attr("height", function(d) {return height - y(d.wins); })
    .attr("fill", function(d) { return color(d.nationality); })
    .attr("stroke", "black")  // Black outline
    .attr("stroke-width", "0.5"); // Outline thickness

// Create a legend
var legend = svg.append("g")
    .attr("transform", `translate(${width - 200}, 0)`); // Position to the right of the chart

// Add legend items
legend.append("text")
    .attr("x", 0)
    .attr("y", -10)
    .style("font-family", "Formula1")
    .style("font-size", "14px")
    .style("font-weight", "bold")
    .text("Nationality of Constructor");

legend.append("line")
    .attr("x1", 0)
    .attr("x2", 300)
    .attr("y1", -5)
    .attr("y2", -5)
    .attr("stroke", "black")
    .attr("stroke-width", 2);

nationalities.forEach((nat, i) => {
    legend.append("rect") 
      .attr("x", 0)
      .attr("y", (i * 25) + 10)
      .attr("width", 12) 
      .attr("height", 12) 
      .style("fill", color(nat));
 

    legend.append("text")
        .attr("x", 20)
        .attr("y", (i * 25) + 16)
        .attr("dy", ".35em")
        .style("font-size", "12px")
        .text(nat);
});
})