$(function()
{
	
	
	
	
	var fluency_tip = $('span#fluency_tip').html();
	var excellence_tip = $('span#excellence_tip').html()
	$('div#fluency').tip(fluency_tip, {animate: true});
	$('div#excellence').tip(excellence_tip, {animate: true});
	
	
	$('div.award_types').find('div').click(function(){
		$('div.award_types').find('div').removeClass('selected');
		$(this).addClass('selected');
		$('.sponsorship_data').data('award_type', $(this).attr('id'));
		
	});
	
		$('div.packages').find('div').click(function(){
		$('div.packages').find('div').removeClass('selected');
		$(this).addClass('selected');
		$('.sponsorship_data').data('package', $(this).attr('id'));
		
	});
	

 });
