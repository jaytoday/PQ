

function RenderProficiencyPanels(prof_dict, buy_buttons){
 
  $.each(buy_buttons, function(b, button){
  	
  	var this_description = $('div#descriptions > div#d_' + button.tag)
$(this_description).append('<div class="buy_button">' + button.html + '</div>');

});
  	
  	
 
	 var proficiencies = $('div.proficiencies').find('div.proficiency');
	  $.each(proficiencies, function(p, proficiency){
	  	
	animatedcollapse.addDiv('d_' + proficiency.id, 'fade=1, group=proficiencies');	
		
	//$(proficiency).append('<div class="buy">{{ proficiencies.checkout_html }}</div>');
	
	

 $(".proficiency").click(function()
                                        {
                                        	 
                                              animatedcollapse.show('d_' + $(this).attr('id'));  
                                        }, function()
                                        {
                                        });


	
	
	
});

animatedcollapse.init();

}
 
$(document).ready(function()
{
	

var scroll_width = 170 * $('.proficiency_container').find('.proficiency').length;
$('.proficiency_container').find('.proficiencies').css('width', scroll_width);   

proficiency_sliderInit();

//$('.proficiency_container').find('.proficiency').click( function(){  });

});

     

