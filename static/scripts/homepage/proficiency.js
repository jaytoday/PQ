
 
$(document).ready(function()
{
	

	 
	 
	animatedcollapse.addDiv('d_energy_economics', 'fade=1');
	animatedcollapse.addDiv('d_biofuels', 'fade=1');
	animatedcollapse.addDiv('d_solar_energy', 'fade=1');
	animatedcollapse.addDiv('d_energy_efficiency', 'fade=1');
	animatedcollapse.addDiv('d_oil', 'fade=1');
	animatedcollapse.addDiv('d_electricity', 'fade=1');
	animatedcollapse.addDiv('d_law_and_policy', 'fade=1');
	animatedcollapse.addDiv('d_wind_power', 'fade=1');
	animatedcollapse.addDiv('d_nuclear_energy', 'fade=1');
	animatedcollapse.addDiv('d_tidal_power', 'fade=1');
	animatedcollapse.init();
	






 $(".proficiency").hover(function()
                                        {
                                        	console.log($(this).attr('id'));
                                              animatedcollapse.show('d_' + $(this).attr('id'));  
                                        }, function()
                                        {
                                              animatedcollapse.hide('d_' + $(this).attr('id')); 
                                        });




var scroll_width = 170 * $('.proficiency_container').find('.proficiency').length;
$('.proficiency_container').find('.proficiencies').css('width', scroll_width);   

proficiency_sliderInit();

$('.proficiency_container').find('.proficiency').click( function(){ console.log('you clicked', $(this).attr('id')); });

});

     
