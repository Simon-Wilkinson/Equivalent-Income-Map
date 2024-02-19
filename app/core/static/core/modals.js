document.addEventListener('DOMContentLoaded', function() {
  'use strict';
  // Open modal when span is clicked
  var openModalSpan = document.getElementById('openModalPPP');
  openModalSpan.addEventListener('click', function() {
    var myModal = new bootstrap.Modal(document.getElementById('myModalPPP'));
    myModal.show();
  });
});
