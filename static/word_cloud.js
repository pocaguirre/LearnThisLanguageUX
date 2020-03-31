am4core.ready(function() {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end
  $.post("/api/word_cloud", {user: "FrenchLearnerJHU"}, function(result){
    var chart = am4core.create("word-cloud", am4plugins_wordCloud.WordCloud);
    var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());
    series.randomness = 0.2;
    series.rotationThreshold = 0;
    series.accuracy = 3;
    series.maxFontSize = 40;
    series.minFontSize = 10;
    var data = result.data;
    data.forEach(function(obs){
      obs.color = am4core.color(obs.color);
    });

    series.data = data;

    series.dataFields.word = "tag";
    series.dataFields.value = "weight";

    series.colors = new am4core.ColorSet();
    series.colors.passOptions = {};
    series.labels.template.propertyFields.fill = "color";


    series.labels.template.urlTarget = "_blank";
    series.labels.template.tooltipText = "{word}: {value}";

    var hoverState = series.labels.template.states.create("hover");
    hoverState.properties.fill = am4core.color("#07070e");

    chart.legend = new am4charts.Legend();
    chart.legend.align = "center";
    chart.legend.data = result.legend;
    chart.legend.position = "top";
      });
}); // end am4core.ready()