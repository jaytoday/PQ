jQuery.fn.extend({
	preserveDefaultText: function(defaultValue, replaceValue)
	{
		$(this).focus(function()
		{
			if(typeof(replaceValue) == 'undefined')
				replaceValue = '';  
			if($(this).val() == defaultValue)
				$(this).val(replaceValue);
		});

		$(this).blur(function(){  
			if(typeof(replaceValue) == 'undefined')
				replaceValue = '';  
			if($(this).val() == replaceValue)
				$(this).val(defaultValue);
		});
		return this;
	}
});
 
$(document).ready(function()
{
	
	animatedcollapse.addDiv('d_energy_economics', 'fade=1');
	animatedcollapse.addDiv('d_biofuels', 'fade=1');
	animatedcollapse.addDiv('d_solar_energy', 'fade=1');
	animatedcollapse.addDiv('d_energy_efficiency', 'fade=1');
	animatedcollapse.addDiv('d_oil', 'fade=1');
	animatedcollapse.addDiv('d_electricity', 'fade=1');
	animatedcollapse.init();
	






 $(".proficiency").hover(function()
                                        {
                                        	console.log($(this).attr('id'));
                                              animatedcollapse.toggle('d_' + $(this).attr('id'));  
                                        }, function()
                                        {
                                              animatedcollapse.hide('d_' + $(this).attr('id')); 
                                        });




var scroll_width = 170 * $('.proficiency_container').find('.proficiency').length;
$('.proficiency_container').find('.proficiencies').css('width', scroll_width);   

proficiency_sliderInit();


});

     
