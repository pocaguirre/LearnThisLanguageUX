am4core.ready(function() {
  $.post("/api/bar_chart", {user: "user"}, function(result) {
    // Themes begin
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
    // Themes end



    // Create chart instance
    var chart = am4core.create("bar-graph", am4charts.XYChart);

    // Add data
    chart.data = result.data;
    chart.legend = new am4charts.Legend();
    chart.legend.position = "right";

    // Create axes
    var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "subreddit";
    categoryAxis.renderer.grid.template.opacity = 0;

    var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
    valueAxis.min = 0;
    valueAxis.renderer.grid.template.opacity = 0;
    valueAxis.renderer.ticks.template.strokeOpacity = 0.5;
    valueAxis.renderer.ticks.template.stroke = am4core.color("#495C43");
    valueAxis.renderer.ticks.template.length = 10;
    valueAxis.renderer.line.strokeOpacity = 0.5;
    valueAxis.renderer.baseGrid.disabled = true;
    valueAxis.renderer.minGridDistance = 40;

  // Create series
    function createSeries(field, name) {
      var series = chart.series.push(new am4charts.ColumnSeries());
      series.dataFields.valueX = field;
      series.dataFields.categoryY = "subreddit";
      series.stacked = true;
      series.name = name;

      var labelBullet = series.bullets.push(new am4charts.LabelBullet());
      labelBullet.locationX = 0.5;
      labelBullet.label.text = "{valueX}";
      labelBullet.label.fill = am4core.color("#fff");
    }
    languages.forEach(function(language){
      createSeries(language, language);
    });
  });
}); // end am4core.ready()