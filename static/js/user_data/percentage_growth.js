/* JavaScript code for graph2.html */
document.addEventListener('DOMContentLoaded', function() {
    initializeChart();
    function initializeChart() {
        let contextData = contextJson;
        let profitList = contextData.profit_list;
        let openingTimeList = contextData.time_list;
        let totalBalance = [profitList[0]];
        let percentageTotalBalance = [];
        
        let chart = am4core.create("chartDiv2", am4charts.XYChart);
        chart.height = am4core.percent(100);

        for (let i = 0; i < profitList.length; i++) {
        let percentage = 0;
        let currentBalance;
        if(i !== 0){
            currentBalance = totalBalance[i-1] + profitList[i];
            totalBalance.push(currentBalance);
        }

        if (i !== 0) {
            percentage = ((currentBalance - totalBalance[i-1]) / totalBalance[i-1]) * 100;
        }
        percentageTotalBalance.push(percentage);
        }
        
        chart.data = openingTimeList.map((openingTime, index) => ({
            category: openingTime,
            percentage: percentageTotalBalance[index]
        }));

        let categoryAxis = chart.xAxes.push(new am4charts.CategoryAxis());
        categoryAxis.dataFields.category = "category";

        let valueAxis = chart.yAxes.push(new am4charts.ValueAxis());

        let series = chart.series.push(new am4charts.LineSeries());
        series.dataFields.valueY = "percentage";
        series.dataFields.categoryX = "category";
        series.strokeWidth = 2;
        series.stroke = am4core.color("#1f77b4");

        chart.legend = new am4charts.Legend();

        let scrollbarX = new am4core.Scrollbar();
        chart.scrollbarX = scrollbarX;

        // Enable tooltips
        chart.cursor = new am4charts.XYCursor();
        chart.cursor.behavior = "zoomXY";
        chart.cursor.snapToSeries = [series];
    }
});