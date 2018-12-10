
(function(){
  var margin = {top: 20, right: 20, bottom: 70, left: 40},
      width = 1000 - margin.left - margin.right,
      height = 300 - margin.top - margin.bottom;


  var div = d3.select("body").append("div")
      .attr("class", "tooltip")
      .style("opacity", 0);

  // Parse the date / time
  // var	parseDate = d3.time.format("%Y-%m").parse;

  var x = d3.scale.ordinal().rangeRoundBands([0, width], .3);

  var y = d3.scale.linear().range([height, 0]);

  var xAxis = d3.svg.axis()
      .scale(x)
      .orient("bottom");
      // .tickFormat();

  var yAxis = d3.svg.axis()
      .scale(y)
      .orient("left")
      .ticks(10);

  var svg_rna = d3.select("#coad_bar_chart")
      .attr("width", width + margin.left + margin.right)
      .attr("height", height + margin.top + margin.bottom)
    .append("g")
      .attr("transform",
            "translate(" + margin.left + "," + margin.top + ")");

  d3.csv("viz_data/rna_weights_COAD_top.csv", function(error, data) {

      data.forEach(function(d) {
        //convert to respective types
          d.value = Math.abs(+d.values);
      });

    x.domain(data.map(function(d) { return d.genes; }));
    y.domain([0, d3.max(data, function(d) { return d.value; })]);

    svg_rna.append("g")
        .attr("class", "x axis")
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis)
      .selectAll("text")
        .style("text-anchor", "end")
        .style('font-size', 'xx-small')
        .attr("dx", "-.8em")
        .attr("dy", "-.55em")
        .attr("transform", "rotate(-70)" );


    svg_rna.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Feature Weight");

    svg_rna.selectAll("bar")
        .data(data)
      .enter().append("rect")
        // .style("fill", "#36D7B3")
        .attr("x", function(d) { return x(d.genes); })
        .attr("width", x.rangeBand())
        .attr("y", function(d) { return y(d.value); })
        .attr("height", function(d) { return height - y(d.value); })
        .on('mouseover', function(d){
          div.transition()
            .duration(200)
            .style("opacity", .9);
          div	.html("<b>GENE:____ </b>" + d.genes + "<br/>" + '<b>WEIGHT: </b>'+'__ ' + d.values)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");
          })
        .on("mouseout", function(d) {
          div.transition()
            .duration(500)
            .style("opacity", 0);
        });

  });

})();
