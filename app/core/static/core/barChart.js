// barChart.js

// Initialize bar chart and set its options
var dom = document.getElementById('bar-container');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var app = {};

var option;

function initializeBarChart() {
    option = {
        tooltip: {
            trigger: 'axis',
            transitionDuration: 0.2,
            axisPointer: {
                type: 'shadow'
            }
        },
        emphasis: {
            itemStyle: {
                borderColor: 'transparent',
                borderWidth: 3
            }
        },
        grid:{
            left: '1%',
            right: '1%',
            bottom: '5%',
            top: '5%',
            containLabel: true
        },
        xAxis: {
            type: 'category',
            z: 10,
            axisLabel: {
                rotate: 90,
                inside: true,
                margin: 5,
                textBorderWidth: 10,
                textStyle: {
                    color: '#fff',
                    fontSize: 12
                },
            },
        },
        yAxis: {
            type: 'value',
            axisLabel: {
                textStyle: {
                    fontSize: 12,
                    color: '#000'
                },
                formatter: '{value}',
            },
        },
        series: [{ 
            type: 'bar',
            barWidth: '90%',
        }]
    };
    
    myChart.setOption(option);
    return myChart;
}


export { initializeBarChart};
