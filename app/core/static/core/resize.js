function set_map_bar_height(){
  console.log('setting map height');
  var topContainer = document.getElementById('explanation-form');
  var mapContainer = document.getElementById('map-container');
  var barContainer = document.getElementById('bar-container');
  var topContainerHeight = topContainer.offsetHeight;
  mapContainer.style.height = mapContainer.offsetWidth/1.5 + 'px';
  barContainer.style.height = barContainer.offsetWidth/1.5 + 'px';
}
set_map_bar_height();
