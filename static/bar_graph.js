am4core.ready(function() {
  // Create chart
  var chart = am4core.create("bar-graph", am4charts.XYChart);

  $.post("/api/bar_chart", {user: "user"}, function(result) {

    // Add Data
    chart.data = result;

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
});