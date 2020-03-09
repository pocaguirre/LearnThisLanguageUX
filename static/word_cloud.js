am4core.ready(function() {
  // Themes begin
  am4core.useTheme(am4themes_animated);
  // Themes end
  $.post("/api/word_cloud", {user: "user"}, function(result){
    var chart = am4core.create("word-cloud", am4plugins_wordCloud.WordCloud);
    chart.fontFamily = "Courier New";
    var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());
    series.randomness = 0.1;
    series.rotationThreshold = 0;
    var data = result;
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
  });
}); // end am4core.ready()