am4core.ready(function() {
// Themes begin

// Themes end
  $.post("/api/stacked_area", {user: $( "#username" ).attr( "username")}, function(result){
    var languages = result.languages;
    var colors = result.colors;
    function am4themes_myTheme(target) {
      if (target instanceof am4core.ColorSet) {
        colors.forEach(function(obs){
          target.list.push(am4core.color(obs));
        });
      }
    }
    am4core.useTheme(am4themes_myTheme);
    am4core.useTheme(am4themes_animated);


    var chart = am4core.create("stacked-area", am4charts.XYChart);
    chart.data = result.data;


    var dateAxis = chart.xAxes.push(new am4charts.DateAxis());
    dateAxis.renderer.minGridDistance = 60;
    dateAxis.startLocation = 0.5;
    dateAxis.endLocation = 0.5;
    dateAxis.baseInterval = {
      timeUnit: "week",
      count: 1
    };

    var valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
    valueAxis.tooltip.disabled = true;


    for (l in languages) {
      var series = chart.series.push(new am4charts.LineSeries());
      series.dataFields.dateX = "week";
      series.name = languages[l];
      series.dataFields.valueY = languages[l];
      series.tooltipText = "[#000]{valueY.value}[/]";
      // series.fill = am4core.color(colors[l]);
      series.tooltip.background.fill = am4core.color("#FFF");
      series.tooltip.getStrokeFromObject = true;
      series.tooltip.background.strokeWidth = 3;
      series.tooltip.getFillFromObject = false;
      series.fillOpacity = 0.6;
      series.strokeWidth = 2;
      series.stacked = true;
    }
    chart.cursor = new am4charts.XYCursor();
    chart.cursor.xAxis = dateAxis;
    chart.scrollbarX = new am4core.Scrollbar();

    // Add a legend
    chart.legend = new am4charts.Legend();
    chart.legend.position = "top";
  });
}); // end am4core.ready()