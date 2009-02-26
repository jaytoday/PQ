/*
 * 
 * This code is badly in need of a tune-up. It needs more efficient use of:
 * 
 *  selector context,
 * selectors and events in loops, 
 * ID selectors instead of CLASS selectors, wherever possible
 * chaining,
 * no DOM manipulation just for data
 * everything wrapped in a single element for DOM insertion
 * for SEO-important sections, add in unimportant markup in JS
 *
 */ 





jQuery(function($) {


// Setup RPC methods
var server = {};
var item_count = 0;

InstallFunction(server, 'RetrieveProficiencies', 'quizbuilder');

InstallFunction(server, 'GetRawItemsForProficiency', 'quizbuilder');

InstallFunction(server, 'GetTopicsForProficiency', 'quizbuilder');



wrong_answers = [];
answer_in_array = [];

$('.proficiency_name').preserveDefaultText('proficiency');
$('.url_name').preserveDefaultText('url');


server.RetrieveProficiencies("all", AfterRetrieveProficiencies);  // Create list of proficiencies 

// On page load, when quiz subjects are retrieved. 
function AfterRetrieveProficiencies(response){  

var proficiencies = parseJSON(response);


 $.each(proficiencies, function(p, proficiency){

 // Add proficiency to list -- todo: nested list organized by proficiencies

$('div#proficiencies').append('<div class="input_float"><input type="checkbox" id="' + p + '" name="proficiency" value="' + proficiency + '" unchecked ><span class="checkbox">' + proficiency + '</span><br/></div>')


.find('input[name="proficiency"]').click(function(){
	
	$('div#proficiencies').data('subject', $(this).attr("value")); 
   });



proficiency_sum = p + 1;
return proficiency_sum;
});


$('div#proficiencies').data('subject', proficiencies[0]);  // select first option as default


$('#submit_proficiency').click(function () {


    server.GetTopicsForProficiency($('div#proficiencies').data('subject'), function(response){ 
    	var topics = response;
    	server.GetRawItemsForProficiency($('div#proficiencies').data('subject'), function(response){  
    		
    		BuildQuizEditor(response, topics); });
		});
    
    
    
$('form#select_proficiency').fadeOut('slow', function(){  $('div#loading_items').fadeIn('slow'); });

    
});


}



function AfterGetRawItemsForProficiency(response){ BuildQuizEditor(response, topics); }


 
 
 /**************** THIS IS JUST FOR THE DEMOS ********************/

/*

function DemoOnly(){
    var proficiency = 'Electricity';

    server.GetTopicsForProficiency(proficiency, function(response){ 
    	var topics = response;
    	server.GetRawItemsForProficiency(proficiency, function(response){  
    		
    		BuildQuizEditor(response, topics); });
		});

$('form#select_proficiency').fadeOut('slow', function(){  $('div#loading_items').fadeIn('slow'); });
}



DemoOnly()

*/


});

