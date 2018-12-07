"use-strict";


d3.csv("cis_unnorm_features.csv", render);

function render(data){
  barchart(data);
}
