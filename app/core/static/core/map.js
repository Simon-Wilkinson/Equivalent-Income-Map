var chartDom = document.getElementById('map-container');
var myMap = echarts.init(chartDom);
var option;

const map_data = data.worldmap_data;

function initializeMap() {
    echarts.registerMap('World', map_data);
    option = {
        tooltip: {
            trigger: 'item',
            showDelay: 0,
            transitionDuration: 0.2,
        },
        scaleLimit: {
            min: 1.2,
            max: 10
        },
        grid:{
            left: '0%',
            right: '0%',
            bottom: '0%',
            top: '0%',
            containLabel: true
        },
        visualMap: {
            left: 'left',
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
            itemWidth: 15,
            itemHeight: 100,
            calculable: true,
        },
        backgroundColor: '#fff',
        toolbox: {
            show: true,
            left: 'left',
            top: 'top',
            feature: {
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
                name: 'Equivalent Income',
                type: 'map',
                roam: true,
                map: 'World',
                emphasis: {
                    label: {
                        show: true
                    }
                },
            }
        ]
    };
    
    myMap.setOption(option);
    return myMap;
}

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
        set_map_bar_height();
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
        GoOutFullscreen();
    idold.style = 'height:300px';
    }
    else {
        GoInFullscreen($("#" + divname).get(0));
    }
    return true;
  }

export { initializeMap};
