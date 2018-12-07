var margin = { top: 50, right: 0, bottom: 100, left: 30 },
  width = 960 - margin.left - margin.right,
  height = 430 - margin.top - margin.bottom,
  gridSize = Math.floor(width / 24),
  legendElementWidth = gridSize*2,
  buckets = 9,
  colors = ["#ffffd9","#edf8b1","#c7e9b4","#7fcdbb","#41b6c4","#1d91c0","#225ea8","#253494","#081d58"], // alternatively colorbrewer.YlGnBu[9]
  datasets = "cis.csv";
  header_row = "header_row.csv";
  header_column = "header_column.csv";



var svg = d3.select("#chart").append("svg")
  .attr("width", width + margin.left + margin.right)
  .attr("height", height + margin.top + margin.bottom)
  .append("g")
  .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

var dayLabels = svg.selectAll(".dayLabel")
  .data(d3.csv(header_column))
  .enter().append("text")
    .text(function (d) { return d; })
    .attr("x", 0)
    .attr("y", function (d, i) { return i * gridSize; })
    .style("text-anchor", "end")
    .attr("transform", "translate(-6," + gridSize / 1.5 + ")")
    .attr("class", function (d, i) { return ((i >= 0 && i <= 4) ? "dayLabel mono axis axis-workweek" : "dayLabel mono axis"); });

var timeLabels = svg.selectAll(".timeLabel")
//gets the headers from the csv for the top lables
  .data(d3.csv(header_row))
  .enter().append("text")
    .text(function(d) { return d; })
    .attr("x", function(d, i) { return i * gridSize; })
    .attr("y", 0)
    .style("text-anchor", "middle")
    .attr("transform", "translate(" + gridSize / 2 + ", -6)")
    .attr("class", function(d, i) { return ((i >= 7 && i <= 16) ? "timeLabel mono axis axis-worktime" : "timeLabel mono axis"); });

var heatmapChart = function(file) {
d3.csv(file,
function(d) {
  return {
    lambda1: +d.lambda1,
    value: +d.values,
    genes: +d.genes
  };
},
function(error, data) {
  var colorScale = d3.scale.quantile()
      .domain([0, buckets - 1, d3.max(data, function (d) { return d.value; })])
      .range(colors);

  var cards = svg.selectAll(".hour")
      .data(data, function(d) {return d.lambda1+':'+d.genes;});

  cards.append("title");

  cards.enter().append("rect")
      .attr("x", function(d) { return (d.lambda1 - 1) * gridSize; })
      .attr("y", function(d) { return (d.genes - 1) * gridSize; })
      .attr("rx", 4)
      .attr("ry", 4)
      .attr("class", "hour bordered")
      .attr("width", gridSize)
      .attr("height", gridSize)
      .style("fill", colors[0]);

  cards.transition().duration(1000)
      .style("fill", function(d) { return colorScale(d.value); });

  cards.select("title").text(function(d) { return d.value; });

  cards.exit().remove();

  var legend = svg.selectAll(".legend")
      .data([0].concat(colorScale.quantiles()), function(d) { return d; });

  legend.enter().append("g")
      .attr("class", "legend");

  legend.append("rect")
    .attr("x", function(d, i) { return legendElementWidth * i; })
    .attr("y", height)
    .attr("width", legendElementWidth)
    .attr("height", gridSize / 2)
    .style("fill", function(d, i) { return colors[i]; });

  legend.append("text")
    .attr("class", "mono")
    .text(function(d) { return "≥ " + Math.round(d); })
    .attr("x", function(d, i) { return legendElementWidth * i; })
    .attr("y", height + gridSize);

  legend.exit().remove();

});
};

heatmapChart(datasets);

var datasetpicker = d3.select("#dataset-picker").selectAll(".dataset-button")
.data(d3.csv(datasets));

datasetpicker.enter()
.append("input")
.attr("value", function(d){ return "Dataset " + d })
.attr("type", "button")
.attr("class", "dataset-button")
.on("click", function(d) {
  heatmapChart(d);
});
