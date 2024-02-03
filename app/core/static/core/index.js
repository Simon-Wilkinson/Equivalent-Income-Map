var chartDom = document.getElementById('map-container');
var myMap = echarts.init(chartDom);
var option;

console.log(myMap.id);
console.log(min_range);

location_data.sort(function (a, b) {
  return a.value - b.value;
});


echarts.registerMap('World', map_data);
option = {
  title: {
    text: 'World Equivelent Income',
    subtext: 'Data from World Bank, 2012',
    sublink: 'http://www.census.gov/popest/data/datasets.html',
    left: 'right'
  },
  tooltip: {
    trigger: 'item',
    showDelay: 0,
    transitionDuration: 0.2,
  },
  visualMap: {
    left: 'right',
    min: min_range,
    max: max_range,
    inRange: {
      color: [
        '#313695',
        '#4575b4',
        '#74add1',
        '#abd9e9',
        '#e0f3f8',
        '#ffffbf',
        '#fee090',
        '#fdae61',
        '#f46d43',
        '#d73027',
        '#a50026'
      ]
    },
    text: ['High', 'Low'],
    calculable: true
  },
  backgroundColor: '#fff',
  toolbox: {
    show: true,
    //orient: 'vertical',
    left: 'left',
    top: 'top',
    feature: {
      magicType: {
          type: ['line', 'bar'],
          title: {
              line: 'line',
              bar: 'bar'
          },
      },
      saveAsImage: {
          show: true,
          title: 'Save Image',
          pixelRatio: 3
      },
      myTool: { //Custom tool myTool 
          show: true,
          title: 'Full screen',
          icon: 'image://https://img.icons8.com/ios-filled/50/000000/full-screen.png',
          onclick: function() {
              setFullScreenToolBox('map-container', 'myMap.id');
          }
      }
  }
  },
  series: [
    {
      name: 'Equivelent Income',
      type: 'map',
      roam: true,
      map: 'World',
      emphasis: {
        label: {
          show: true
        }
      },
      data: location_data
    }
  ]
};
myMap.setOption(option);

option && myMap.setOption(option);
window.addEventListener('resize', myMap.resize);


var dom = document.getElementById('bar-container');
var myChart = echarts.init(dom, null, {
  renderer: 'canvas',
  useDirtyRect: false
});
var app = {};

var option;

option = {
  title: {
    text: 'Equivelent Income $K',
  },
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
  xAxis: {
    type: 'category',
    axisLabel: {
      rotate: 90
    },
    data: location_data.map(function (item) {
      return item.name;
    })
  },
  yAxis: {
    type: 'value'
  },
  series: [
    {
      data: location_data.map(function (item) {
        if (item.value == base_income)
          return {value: item.value, itemStyle: {color: "#00a900" }};
        else
          return {value: item.value};
      }),
      type: 'bar'
    }
  ]
};

if (option && typeof option === 'object') {
  myChart.setOption(option);
}
window.addEventListener('resize', myChart.resize);

// Listen for the mouseover event on the map chart
myMap.on('mouseover', function (params) {
  console.log(params);
  if (params.componentType === 'series') {
    // Dispatch action to highlight corresponding data point in the bar chart
    myChart.dispatchAction({
      type: 'showTip',
      seriesIndex: 0,  // Assuming you have only one series in the bar chart
      dataIndex: params.dataIndex
    });
  }
});

// Listen for the mouseout event on the bar chart
myChart.on('mouseover', function (params) {
  console.log(params);
  if (params.componentType === 'series') {
    // Dispatch action to highlight corresponding data point in the map chart
    myMap.dispatchAction({
      type: 'showTip',
      seriesIndex: 0,  // Assuming you have only one series in the map chart
      dataIndex: params.dataIndex
    });
  }
});


function GoInFullscreen(element) {
  if (element.requestFullscreen)
      element.requestFullscreen();
  else if (element.mozRequestFullScreen)
      element.mozRequestFullScreen();
  else if (element.webkitRequestFullscreen)
      element.webkitRequestFullscreen();
  else if (element.msRequestFullscreen)
      element.msRequestFullscreen();
}

function GoOutFullscreen() {
  if (document.exitFullscreen)
      document.exitFullscreen();
  else if (document.mozCancelFullScreen)
      document.mozCancelFullScreen();
  else if (document.webkitExitFullscreen)
      document.webkitExitFullscreen();
  else if (document.msExitFullscreen)
      document.msExitFullscreen();
}

function IsFullScreenCurrently() {
  var full_screen_element = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement || null;

  // If no element is in full-screen
  if (full_screen_element === null)
      return false;
  else
      return true;
}

function setFullScreenToolBox(divname, idchart) {
  var classold = document.getElementById(divname).className;
  var idold = document.getElementById(idchart);
  console.log(classold);
  
  if (IsFullScreenCurrently()){
      console.log('exiting full screen');
      GoOutFullscreen();
  idold.style = 'height:300px';
  }
  else {
      // document.getElementById(divname).className = "col-md-12";
      //idold.style = 'height:500px';
      var heights = screen.height;// window.innerHeight;
      //idold.style.height = heights -100 + "px";
      console.log('going full screen');                
      GoInFullscreen($("#" + divname).get(0));
  }
  
  return true;
}