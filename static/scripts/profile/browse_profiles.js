		$(function(){

$('div#right_corner').find('span').text('');

	    var scroll_width = 200 * $('.pb_container').find('.user').length;
$('.pb_container').find('.profiles').css('width', scroll_width);  


	    profile_sliderInit();
	    
	    
	    $('input:checkbox').checkbox();


        $('div.embed_code').hide(); // get rid of embed codes

			
		});
