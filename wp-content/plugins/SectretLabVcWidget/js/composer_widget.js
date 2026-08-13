jQuery(document).ready(function ($) {
	"use strict";
	
	$('.sl_composer_widget_parent_id').each(function(i, el) {

		var target_el = $(el).parents('.widget').find('.vc_grid-container'),
			vc_data = $(target_el).attr('data-vc-grid-settings'),
			id = $(this).attr('parent_id');

		if ( typeof( vc_data ) == 'string' ) {
		    vc_data = vc_data.replace(/.page_id..[0-9]+/, '"page_id":' + id);
		    $(target_el).attr('data-vc-grid-settings', vc_data);
		}
       
	});
	
});