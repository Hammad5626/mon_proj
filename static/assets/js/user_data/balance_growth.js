// JavaScript code for user_data.js

// Wait for the DOM to load
document.addEventListener('DOMContentLoaded', function() {
  initializeChart();
    // Function to initialize the chart
    function initializeChart() {
      // Parse JSON data
      let contextData = contextJson;
      let profitList = contextData.profit_list;
      let typeList = contextData.type_list;
      let openingPriceList = contextData.opening_price_list;
      let openingTimeList = contextData.time_list;
      let totalBalance = [profitList[0]];
      let averageBalance = [profitList[0]];
      am4core.useTheme(am4themes_animated);

      var base = document.createElement("base");
      base.href = "/foo";
      document.head.appendChild(base);
      // Create the chart
      let chart = am4core.create("chartDiv1", am4charts.XYChart);
      chart.width = am4core.percent(100);
      chart.height = am4core.percent(100);
  
      // Calculate total balance and average balance
      for (let i = 0; i < profitList.length; i++) {
        if (i != 0) {
          let currentBalance = totalBalance[i - 1] + profitList[i];
          totalBalance.push(currentBalance);
        }
        let sum = totalBalance.reduce((acc, val) => acc + val, 0);
        let average = sum / (i + 1);
        averageBalance.push(average);
      }
  
      // Set chart data
      chart.data = openingTimeList.map((openingTime, index) => ({
        category: openingTime,
        balance: totalBalance[index],
        average: averageBalance[index],
        type: typeList[index],
        profit: profitList[index],
      }));
  
      // Create category axis
      let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
      categoryAxis.dataFields.category = "category";
  
      // Create value axis
      let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());
  
      // Create balance series
      let balanceSeries = chart.series.push(new am4charts.LineSeries());
      balanceSeries.dataFields.valueY = "balance";
      balanceSeries.dataFields.categoryX = "category";
      balanceSeries.tooltipText = "Balance: {balance}\nTime: {category}";
      balanceSeries.strokeWidth = 2;
      balanceSeries.minBulletDistance = 15;
      balanceSeries.stroke = am4core.color("#1f77b4");
  
      // Drop-shaped tooltips
      balanceSeries.tooltip.background.cornerRadius = 20;
      balanceSeries.tooltip.background.strokeOpacity = 0;
      balanceSeries.tooltip.pointerOrientation = "vertical";
      balanceSeries.tooltip.label.minWidth = 40;
      balanceSeries.tooltip.label.minHeight = 40;
      balanceSeries.tooltip.label.textAlign = "middle";
      balanceSeries.tooltip.label.textValign = "middle";

      // Make bullets grow on hover
      var bullet = balanceSeries.bullets.push(new am4charts.CircleBullet());
      bullet.circle.strokeWidth = 2;
      bullet.circle.radius = 4;
      bullet.circle.fill = am4core.color("#fff");

      var bullethover = bullet.states.create("hover");
      bullethover.properties.scale = 1.3;

      // Make a panning cursor
      chart.cursor = new am4charts.XYCursor();
      chart.cursor.behavior = "panXY";
      chart.cursor.xAxis = categoryAxis;
      chart.cursor.snapToSeries = balanceSeries;

      // Create a horizontal scrollbar with previe and place it underneath the date axis
      chart.scrollbarX = new am4charts.XYChartScrollbar();
      chart.scrollbarX.balanceSeries.push(series);
      chart.scrollbarX.parent = chart.bottomAxesContainer;

      chart.events.on("ready", function () {
        dateAxis.zoom({start:0.79, end:1});
      });
      var i = 0;
      categoryAxis.events.on('rangechangeended', function (ev) {
        i++;
        history.replaceState('', {}, '/bar?i='+i+'#abc')
      });

      // Set stroke color based on data properties
      balanceSeries.propertyFields.stroke = function(dataItem) {
        if (dataItem.type === "Balance" && dataItem.profit < 0) {
          return am4core.color("#8B0000");
        } else if (dataItem.type === "Balance" && dataItem.profit > 0) {
          return am4core.color("#00008B");
        } else {
          return balanceSeries.stroke;
        }
      };
  
      // Create average series
      let averageSeries = chart.series.push(new am4charts.LineSeries());
      averageSeries.dataFields.valueY = "average";
      averageSeries.dataFields.categoryX = "category";
      averageSeries.strokeWidth = 2;
      averageSeries.stroke = am4core.color("#ff7f0e");
  
      // Add chart legend
      chart.legend = new am4charts.Legend();
  
      // Add scrollbar
      let scrollbarX = new am4core.Scrollbar();
      chart.scrollbarX = scrollbarX;
  
      // Enable tooltips
      chart.cursor = new am4charts.XYCursor();
      chart.cursor.behavior = "zoomXY";
      chart.cursor.snapToSeries = [balanceSeries, averageSeries];
    }
  
  });
  