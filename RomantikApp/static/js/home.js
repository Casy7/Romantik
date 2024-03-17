mapboxgl.accessToken = 'pk.eyJ1IjoiY2FzeTciLCJhIjoiY2s1aWl5MXV4MGI5dDNvbW41bm82OGpmdyJ9.t3Er5THaXs9H0hH2JSp-Ww';
const map = new mapboxgl.Map({
container: 'map', // container ID
// Choose from Mapbox's core styles, or make your own style with Mapbox Studio
style: 'mapbox://styles/mapbox/streets-v12', // style URL
center: [30.77, 46.45], // starting position [lng, lat]
zoom: 13 // starting zoom
});

if (window.mobileCheck()) {
	map.flyTo({
		center: [30.751867631916582,  46.44910605734739]
		});
}

const marker1 = new mapboxgl.Marker().setLngLat([30.74983, 46.44903]).addTo(map);



function refresh_news(additionaldata = {}) {
	$.ajax({
		url: "/refresh_news_from_tg/",
		type: 'GET',
		data: {
			'secondary_data': additionaldata
		},
		//DO NOT EDIT!
		beforeSend: function (xhr, settings) {
			function getCookie(name) {
				var cookieValue = null;
				if (document.cookie && document.cookie != '') {
					var cookies = document.cookie.split(';');
					for (var i = 0; i < cookies.length; i++) {
						var cookie = jQuery.trim(cookies[i]);
						// Does this cookie string begin with the name we want?
						if (cookie.substring(0, name.length + 1) == (name + '=')) {
							cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
							break;
						}
					}
				}
				return cookieValue;
			}
			if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
				// Only send the token to relative URLs i.e. locally.
				xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
			}
		},
		//EDITABLE CODE
		success: function a(json) {
			// alert("Updated");

		}
	});
}