function set_map_height(){
    var topContainer = document.getElementById('explanation-form');
    var mapContainer = document.getElementById('map-container');
    var topContainerHeight = topContainer.offsetHeight;
    if (window.innerWidth > 1200)
    {
      mapContainer.style.height = (window.innerHeight - topContainerHeight - 100) + 'px';
    }
    else {
      mapContainer.style.height = window.innerHeight/3 + 'px';
    }
  }
  set_map_height();
  document.addEventListener('DOMContentLoaded', function() {
      // Optional: Update the height on window resize
      window.addEventListener('resize', set_map_height);
  });