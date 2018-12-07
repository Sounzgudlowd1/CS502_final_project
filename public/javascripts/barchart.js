function barchart(data) {

    let symptoms = data.map(d => d.symptoms).filter(symptom => symptom !== 'unknown').flatMap(symptom => symptom.split(';'));

    let symptoms_map = symptoms.reduce((acc, val) => acc.set(val, 1 + (acc.get(val) || 0)), new Map());
    let symptom_keys = [...symptoms_map.keys()];

    let max_y = d3.max([...symptoms_map.values()]);
    max_y = max_y * 1.05; // adding sufficient margin
    max_y = Math.ceil(max_y / 10) * 10; // Rounding to nearest 10

    let aspectRatio = 1;
    var margin = {top: 40, right: 100, bottom: 100, left: 50};
    const width = d3.select('.symptoms_bar_chart').node().clientWidth -  margin.left - margin.right;
// const height = d3.select('#scene').node().clientHeight - 2 * margin;
    const height = (d3.select('.symptoms_bar_chart').node().clientWidth * aspectRatio) - margin.top - margin.bottom;

    d3.select("#symptoms_bar_chart").html("");

    const svg = d3.select('#symptoms_bar_chart');
    svg.attr('height', height + margin.top + margin.bottom);
    svg.attr('width', width + margin.left + margin.right);



    const chart = svg.append('g')
        .attr('transform', `translate(${margin.left}, ${margin.top})`);

    const title = chart.append("text")
        .attr("x", (width / 2))
        .attr("y", 0 - (margin.top * 0.33))
        .attr("text-anchor", "middle")
        .style("font-size", "16px")
        .style("text-decoration", "strong")
        .text("Mostly Logged Symptoms");

    const yScale = d3.scaleLinear()
        .range([height, 0])
        .domain([0, max_y]);

    chart.append('g')
        .call(d3.axisLeft(yScale));

    const xScale = d3.scaleBand()
        .range([0, width])
        .domain(symptom_keys)
        .padding(0.2);

    chart.append('g')
        .attr('transform', `translate(0, ${height})`)
        .call(d3.axisBottom(xScale))
        .selectAll("text")
        .attr("y", 0)
        .attr("x", 9)
        .attr("dy", ".35em")
        .attr("transform", "rotate(30)")
        .style("text-anchor", "start");

    const makeYLines = () => d3.axisLeft()
        .scale(yScale);

    chart.append('g')
        .attr('class', 'symptoms_grid')
        .call(makeYLines()
            .tickSize(-width, 0, 0)
            .tickFormat('')
        );

    const barGroups = chart.selectAll()
        .data(symptom_keys)
        .enter()
        .append('g');

    barGroups
        .append('rect')
        .attr('class', 'symptoms_bar')
        .attr('x', (symptom) => xScale(symptom))
        .attr('y', (symptom) => yScale(symptoms_map.get(symptom)))
        .attr('height', (symptom) => height - yScale((symptoms_map.get(symptom))))
        .attr('width', xScale.bandwidth());
        // .on('mouseenter', function (actual, i) {
        //     d3.selectAll('.value')
        //         .attr('opacity', 0);
        //
        //     d3.select(this)
        //         .transition()
        //         .duration(300)
        //         .attr('opacity', 0.6)
        //         .attr('x', (a) => xScale(a) - 5)
        //         .attr('width', xScale.bandwidth() + 10);
        //
        //     const y = yScale(symptoms_map.get(actual));
        //
        //     // line = chart.append('line')
        //     //     .attr('id', 'limit')
        //     //     .attr('x1', 0)
        //     //     .attr('y1', y)
        //     //     .attr('x2', width)
        //     //     .attr('y2', y);
        //
        //     barGroups.append('text')
        //         .attr('class', 'divergence')
        //         .attr('x', (a) => xScale(a) + xScale.bandwidth() / 2)
        //         .attr('y', (a) => yScale(symptoms_map.get(a)) + 30)
        //         .attr('fill', 'white')
        //         .attr('text-anchor', 'middle')
        //         .text((a, idx) => {
        //             const divergence = (a - actual).toFixed(1);
        //
        //             let text = '';
        //             if (divergence > 0) text += '+';
        //             text += `${divergence}%`;
        //
        //             return idx !== i ? text : '';
        //         })
        //
        // })
        // .on('mouseleave', function () {
        //     d3.selectAll('.value')
        //         .attr('opacity', 1);
        //
        //     d3.select(this)
        //         .transition()
        //         .duration(300)
        //         .attr('opacity', 1)
        //         .attr('x', (a) => xScale(symptoms_map.get(a)))
        //         .attr('width', xScale.bandwidth());
        //
        //     chart.selectAll('#limit').remove();
        //     chart.selectAll('.divergence').remove()
        // });
}
