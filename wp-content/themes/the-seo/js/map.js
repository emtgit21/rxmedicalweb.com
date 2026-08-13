
	
	jQuery(document).ready(function($){
	    var map = new GMaps({
		    el: '#footermap',
		    lat: 26.166889,
			lng: -80.110815,
			zoom: 17,
			scrollwheel : false,
			zoomControl : true,
			    zoomControlOpt: {
				    style : 'SMALL',
					position: 'TOP_LEFT'
				},
			panControl : false,
            streetViewControl : false,
            mapTypeControl: false,
            overviewMapControl: false
        });	

        map.addMarker({
            lat: 26.166889,
            lng: -80.110815,
			icon: '/wp-content/themes/the-seo/images/map-marker.png'
		});
		var styles = [
		    {
			    stylers: [
				    { hue: "#95a5a6" },
					{ saturation: -100 }
				]
			}, {
					featureType: "road",
					elementType: "geometry",
					stylers: [
						{ lightness: 100 },
						{ visibility: "simplified" }
					]
			}, {
					featureType: "road",
					elementType: "labels",
					stylers: [
						{ visibility: "off" }
					]
				}
            ];

			map.addStyle({
				styledMapName:"Styled Map",
				styles: styles,
				mapTypeId: "map_style"
			});

			map.setStyle("map_style");

		});