$(function()
{
	

	$('select').change(function(){
		console.log($('select#award_type').val());
        console.log($('select#proficiency :selected').text());
	
	$('span.preview_award_type').html($('select#award_type').val());
	$('span.preview_subject').html($('select#proficiency :selected').text());	
		});
	
	var fluency_tip = $('span#fluency_tip').html();
	var excellence_tip = $('span#excellence_tip').html()
	$('div#fluency').tip(fluency_tip, {animate: true});
	$('div#excellence').tip(excellence_tip, {animate: true});
	
	/*
	$('div.award_types').find('div').click(function(){
		$('div.award_types').find('div').removeClass('selected');
		$(this).addClass('selected');
		$('.sponsorship_data').data('award_type', $(this).attr('id'));
		
	});
	*/
	
		$('div.packages').find('div').click(function(){
		$('div.packages').find('div').removeClass('selected');
		$(this).addClass('selected');
		$('.sponsorship_data').data('package', $(this).attr('id'));
		
	});
	
	$('div.packages > div#medium').click(); //medium is default package
	
	$('div#submit_sponsorpledge').click(function(){
				
	SubmitSponsorPledge();
			});
			
			
			// Select Empty Value for Proficiency
			 if (!$("select#proficiency option:selected").length) $("select#proficiency option[value='']").attr('selected', 'selected');



			
			
 });


// Setup RPC methods
var server = {};
var item_count = 0;

InstallFunction(server, 'SubmitSponsorPledge', 'accounts');



 function SubmitSponsorPledge() {
// get the different pieces of data, and submit them

 var target = $('.sponsorship_data').data('target');
 var award_type = $('select#award_type').val();
 var sponsor_package = $('.sponsorship_data').data('package');
 var proficiency = $('select#proficiency').attr('value');

  // var sponsor = $('.sponsorship_data').data('sponsor');  -- Just Using Session
 console.log(target, award_type, sponsor_package, proficiency);
 
 
 server.SubmitSponsorPledge(sponsor_package, award_type, target, proficiency);

	                          
	                      
}

