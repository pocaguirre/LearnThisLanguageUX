am4core.ready(function() {
// Create chart
var chart = am4core.create("bar-graph", am4charts.XYChart);

// The following would work as well:
// var chart = am4core.create("chartdiv", "XYChart");

// Add Data
chart.data = [{
"country": "USA",
"visits": 3025
}, {
  "country": "China",
  "visits": 1882
}, {
  "country": "Japan",
  "visits": 1809
}];

// Add category axis
var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
categoryAxis.dataFields.category = "country";



// Add value axis
var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
valueAxis.dataFields.value = "visits";

// Add series
var series = chart.series.push(new am4charts.ColumnSeries());
series.name = "Web Traffic";
series.dataFields.categoryY = "country";
series.dataFields.valueX = "visits";
});