am4core.ready(function() {

// Themes begin
am4core.useTheme(am4themes_animated);
// Themes end

var chart = am4core.create("word-cloud", am4plugins_wordCloud.WordCloud);
chart.fontFamily = "Courier New";
var series = chart.series.push(new am4plugins_wordCloud.WordCloudSeries());
series.randomness = 0.1;
series.rotationThreshold = 0;

series.data = [{
  "tag": "Breaking News",
  "weight": 60,
  "color": am4core.color("#4A2040")
}, {
  "tag": "Environment",
  "weight": 80,
  "color": am4core.color("#9F6BA0")
}, {
  "tag": "Politics",
  "weight": 90,
  "color": am4core.color("#C880B7")
}, {
  "tag": "Business",
  "weight": 25,
  "color": am4core.color("#EC9DED")
}, {
  "tag": "Lifestyle",
  "weight": 30,
  "color": am4core.color("#DFBAD3")
}, {
  "tag": "World",
  "weight": 45,
  "color": am4core.color("#C880B7")
}, {
  "tag": "Sports",
  "weight": 160,
  "color": am4core.color("#4A2040")
}, {
  "tag": "Fashion",
  "weight": 20,
  "color": am4core.color("#C880B7")
}, {
  "tag": "Education",
  "weight": 78,
  "color": am4core.color("#9F6BA0")
}];

series.dataFields.word = "tag";
series.dataFields.value = "weight";

series.colors = new am4core.ColorSet();
series.colors.passOptions = {};
series.labels.template.propertyFields.fill = "color";


series.labels.template.urlTarget = "_blank";
series.labels.template.tooltipText = "{word}: {value}";

var hoverState = series.labels.template.states.create("hover");
hoverState.properties.fill = am4core.color("#07070e");

// var subtitle = chart.titles.create();
// subtitle.text = "(click to open)";
//
// var title = chart.titles.create();
// title.text = "Most Popular Tags @ StackOverflow";
// title.fontSize = 20;
// title.fontWeight = "800";
}); // end am4core.ready()