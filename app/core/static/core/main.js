
// Import required modules
import { initializeMap } from './map.js';
import { initializeBarChart } from './barChart.js';

// Global variables and initialization
var equivalentIncomes, minRange, maxRange;

// Accessing the data
const locationData = data.location_data;

// Calculate equivalent income based on form values
function calculateEquivalentIncomeFromForm(baseLocationName, baseIncome, indexType) {
    var baseLocation = locationData.find(item => item.name == baseLocationName);
    equivalentIncomes = [];
    if (indexType === 'Purchase Power Parity') {
        let baseIndexValue = baseLocation.ppp_usa;
        for (let i = 0; i < locationData.length; i++) {
            if (locationData[i].ppp_usa != null) {
                equivalentIncomes.push({
                    name: locationData[i].name,
                    value: (baseIncome * (baseIndexValue / locationData[i].ppp_usa)).toFixed(0)
                });
            }
        }
    } else if (indexType === 'Big Mac Index') {
        let baseIndexValue = baseLocation.big_mac_dollar;
        for(let i = 0; i < locationData.length; i++) {
            if (locationData[i].big_mac_dollar != null) {
                equivalentIncomes.push({
                    name: locationData[i].name,
                    value: (baseIncome * (locationData[i].big_mac_dollar / baseIndexValue)).toFixed(0)
                });
            }
        }
    }
    equivalentIncomes.sort(function (a, b) {
      return a.value - b.value;
    });
    return equivalentIncomes;
  }
  function calculateExchangeRate(baseLocationName, targetLocationName) {
    var baseLocation = locationData.find(item => item.name == baseLocationName);
    var targetLocation = locationData.find(item => item.name == targetLocationName);
    return (baseLocation.exchange_rate_dollar / targetLocation.exchange_rate_dollar);
  }
  function getCurrencySymbol(locationName) {
    return locationData.find(item => item.name == locationName).currency_symbol;
  }

// Set form values and calculate equivalent incomes
function getFormValuesAndCalculateEquivalentIncomes() {
    // Get form values
    var baseLocationName = document.getElementById('id_country').value;
    var baseCurrencySymbol = getCurrencySymbol(baseLocationName);
    var baseIncome = document.getElementById('id_income').value;
    var indexType = document.getElementById('id_index').value;

    // Calculate equivalent incomes based on form values
    equivalentIncomes = calculateEquivalentIncomeFromForm(baseLocationName, baseIncome, indexType);
    // Calculate min and max range for visual map
    minRange = 0;
    var a = baseIncome > 10000 ? 10000 : 1000;
    maxRange = Math.ceil(Math.max(...equivalentIncomes.map(item => item.value)) / a) * a;

    // Set options for map and bar chart
    myMap.setOption({
        tooltip:{
            formatter: function (params) {
                if (params.data == undefined){
                    return '<b>' + params.name + '<br/>'+ 'Data not available' + '</b>'
                }
                else{
                    return  '<b>' + params.name + '<br/>'+
                        baseCurrencySymbol + params.value.toLocaleString() + '<br>' +
                        getCurrencySymbol(params.name) + (Number((params.value/calculateExchangeRate(baseLocationName, params.name)).toFixed(0))).toLocaleString() + '</b>';
                }
            }
        },
        series: [{
            data: equivalentIncomes
        }],
        visualMap: {
            min: minRange,
            max: maxRange,
            formatter: function (params) {
                return baseCurrencySymbol + params;
            }
        }
        
    });

    myChart.setOption({
        tooltip:{
            formatter: function (params) {
                return  '<b>' + baseCurrencySymbol + Number(params[0].value).toLocaleString() + '</b>';                
            }
        },
        xAxis: {
            data: equivalentIncomes.map(item => item.name)
        },
        yAxis: {
            min: minRange,
            max: maxRange,
            axisLabel: {
                formatter: function (params) {
                    return baseCurrencySymbol + params;
                }
            }
        },
        series: [{
            data: equivalentIncomes.map(item => ({
                value: item.value,
                formatter: baseCurrencySymbol + ' ' + item.value,
                itemStyle: {
                    color: baseLocationName === item.name ? 'green' : '#4575b4'
                }
            }))
        }]
    });
}

// Update map and bar chart on form change
function updateMapAndBarChartOnFormChange() {
    // Call setFormValuesAndCalculateEquivalentIncomes() on form change
    getFormValuesAndCalculateEquivalentIncomes();
}

// Event listeners
function formEventListeners() {
    document.getElementById("myForm").addEventListener("submit", function(event) {
        event.preventDefault();
    });
    document.getElementById('myForm').addEventListener('change', updateMapAndBarChartOnFormChange);
}

// Listen for events on the map chart
function mapEventListeners() {
    myMap.on('mouseover', function (params) {
        if (params.componentType === 'series') {
            myChart.dispatchAction({
                type: 'showTip',
                seriesIndex: 0,  // Assuming you have only one series in the bar chart
                dataIndex: params.dataIndex
            });
        }
    });
}

// Handle resizing of the map chart
function handleMapResize() {
    myMap.resize();
    myMap.setOption({
        visualMap: {
            itemHeight: myMap.getHeight() / 4,
            itemWidth: myMap.getWidth() / 50
            
        }
    }
    );
}
// Handle resizing of the bar chart
function handleBarChartResize() {
    myChart.resize();

}


// Listen for events on the bar chart
function barChartEventListeners() {
    myChart.on('mouseover', function (params) {
        if (params.componentType === 'series') {
            myMap.dispatchAction({
                type: 'showTip',
                seriesIndex: 0,  // Assuming you have only one series in the map chart
                dataIndex: params.dataIndex
            });
        }
    });
}


// Initialization
var myMap = initializeMap();
var myChart = initializeBarChart();
getFormValuesAndCalculateEquivalentIncomes();
mapEventListeners();
barChartEventListeners();
formEventListeners();
window.addEventListener('resize', function() {
    set_map_bar_height()
    handleMapResize();
    handleBarChartResize();
});
