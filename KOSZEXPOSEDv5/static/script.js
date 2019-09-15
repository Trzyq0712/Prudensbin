findMeButton.on('click', function(){

  navigator.geolocation.getCurrentPosition(function(position) {

      // Get the coordinates of the current position.
      var lat = position.coords.latitude;
      var lng = position.coords.longitude;

      // Create a new map and place a marker at the device location.
      var map = new GMaps({
          el: '#map',
          lat: lat,
          lng: lng
      });

      map.addMarker({
          lat: lat,
          lng: lng
      });

  });

});
