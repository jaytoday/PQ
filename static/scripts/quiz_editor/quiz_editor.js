
$(function(){
    
 var quiz_count = parseInt( $('div.quiz_item:last').attr('id') );
 var scroll_width = 950 * quiz_count;
 $('div#quiz_items').css('width', scroll_width);
 
 $('.new_answer').preserveDefaultText('write a custom answer');
 $('.item_topic').preserveDefaultText('        topic');
 
 $("select").change(function() {
            if ($('div#select_topic_' + i).find("select option:selected").text() == "New Topic") { $(this).hide(); $(this).parent().find('input.new_item_topic').show().preserveDefaultText('write a new topic'); } 
          });
          


          item_sliderInit();
          


 //$('ul.item_navigation').append('<li class="index"><a href="#' + i + '" onClick="return false;">' + item.index + '</a></li>');   // href="#' + i + '" -- for navigation. 


// EditQuizItem(i, item, answers); // Run function after the above code is evaluated.


 
 
    
});

/*
function BuildQuizEditor(response, topics){




   


$('ul.item_navigation').show();
$('div#quiz_items').show();

$('div#loading_items').remove();

} // end of  BuildQuizEditor()



*/











/*

function EditQuizItem(i, item, answers) {

// setup for ajax call     
var server = {};
InstallPostFunction(server, 'SubmitQuizItem', 'quizbuilder');  // POST Request
InstallFunction(server, 'SetItemModStatus', 'quizbuilder'); // are we still using this? 

// setup arrays
wrong_answers[i] = [];
answer_in_array[i] = [];   



 

 $.each(answers, function(n, answer){
 	
 answer_in_array[i][n] = "False"; 
 
});


 
 //$('div#' + i + ' > div#quiz_item_content').jScrollPane();

// $('div#answers_' + i).jScrollPane();
 

$('#quiz_data_' + i + ' > input[@name="proficiency"]').click(function(){
$('#quiz_data_' + i + ' > input[@name="proficiency"]').setValue($(this).attr("value"));
});


    
$('div#answers_' + i + ' > div').click(function(){
			
//    If answer is selected, remove it if it's already in array. 
//    If not, add it to the array, if the limit hasn't been reached. 

answer_text = $(this).text();

n = $(this).attr("id");

for (var a = 0, loopCnt = wrong_answers[i].length; a < loopCnt; a++) {


if (answer_text == wrong_answers[i][a][0]){   // if answer text is already there


wrong_answers[i].splice(a, 1);
UpdatePreviews(wrong_answers, ANSWER_LIMIT, i);

answer_in_array[i][n] = "False"; // answer not in array anymore

$(this).removeClass("ac_selected");
$(this).addClass("ac_unselected");


return;


}

}

if (answer_in_array[i][n] == "False") {

if (wrong_answers[i].length > (ANSWER_LIMIT - 1)) { console.log("Only 2 Wrong Answers, Please!"); $("div.answers_container").fadeTo(50, 0.5).fadeTo(50, 1); return false; }  // If there are already two answers

var answer_pair = [answer_text, n];
wrong_answers[i].splice(wrong_answers[i].length, 0, answer_pair);   // add answer to array
UpdatePreviews(wrong_answers, ANSWER_LIMIT, i);

answer_in_array[i][n] == "True"; // this isn't needed.

$(this).removeClass("ac_unselected");
$(this).addClass("ac_selected");

  console.log('added answer:',wrong_answers[i]);
  return;
  
}

			});
			
			
		//submit_new_answer
		$('form#quiz_data_' + i).find('input[@name="new_answer"]').keydown(function(event){	
	$('form#quiz_data_' + i).find('input[@name="submit_new_answer"]').show(); });
	//move answer to array
			$('form#quiz_data_' + i).find('input[@name="submit_new_answer"]').click(function(){
				if (wrong_answers[i].length > (ANSWER_LIMIT - 1)) { console.log("Only 2 Wrong Answers, Please!"); return false; }  // If there are already two answers
var answer_pair = [$('form#quiz_data_' + i).find('input[@name="new_answer"]').attr('value'), 0];
wrong_answers[i].splice(wrong_answers[i].length, 0, answer_pair);   // add answer to array
UpdatePreviews(wrong_answers, ANSWER_LIMIT, i);
$('form#quiz_data_' + i).find('input[@name="submit_new_answer"]').hide();
$('form#quiz_data_' + i).find('input[@name="new_answer"]').attr('value', 'write a custom answer');

			});
			
			
			
		
// Update index value (correct answer)
$('#answer_choice_previews_' + i).find('span#correct').click(function(){ 
	$(this).hide();
	$('#answer_choice_previews_' + i).find('div#new_index').show();
	$('input.new_index').preserveDefaultText($(this).text());
});

// Update index display (correct answer)			
$('#answer_choice_previews_' + i).find('input[@name="submit_new_index"]').click(function(e){
	 item.index = $('#answer_choice_previews_' + i).find('input[@name="new_index"]').attr('value');
	$('#answer_choice_previews_' + i).find('div#new_index').hide();
	$('#answer_choice_previews_' + i).find('span#correct').text(item.index).show();
});
	




	// Clicking answer span preview

for (w=0; w < ANSWER_LIMIT; w++){ $('#answer_choice_previews_' + i).find('span#selection_' + w).click(function(){

for (a=0; a < wrong_answers[i].length; a++){ if ($(this).text() == wrong_answers[i][a][0]){ 
	  
	  ac_index = parseInt(wrong_answers[i][a][1]) + 1; 
	  $('div#answers_' + i + ' > div:nth-child(' + ac_index  + ')').removeClass("ac_selected").addClass("ac_unselected");  //remove highlight from answer choice
	 wrong_answers[i].splice(a, 1); // remove answer in array that matches $(this).text()
	 } 
	  }

	 UpdatePreviews(wrong_answers, ANSWER_LIMIT, i);
    }); }
    


PreviewAnswer(i);

EditItemContent(i);

$('form#quiz_data_' + i).find('input[@name="skip_item"]').click(function() { $('.quizbuilder_wrapper .scroller').trigger('next'); }); // skip item   moderated=ignore
	            
$('form#quiz_data_' + i).find('input[@name="submit_item"]').click(function() {         //moderated=true
	var topic_value = eval('document.quiz_data_' + i + '.item_topic.value');
	if (topic_value == 'Pick a Topic'){ console.info('Pick a Topic!'); return false; }
	if (topic_value == 'New Topic'){ topic_value = eval('document.quiz_data_' + i + '.new_item_topic.value'); }


var submit_wrong_answers = [];
for (w=0; w < wrong_answers[i].length; w++){
submit_wrong_answers.splice(wrong_answers[i].length, 0, wrong_answers[i][w][0]); 
}

if (submit_wrong_answers.length < 2){ console.info('not enough answers!'); return false;  }

if ($('div#quiz_item_content_' + i + ' > div.item_inner').html().length > 500){ console.info('quiz item is too long!'); return false; }

// proceed to next quiz item
$('.quizbuilder_wrapper .scroller').trigger('next');



  //                                                           correct          all answers                            topic value                                     HTML                                                              url         proficiency
 server.SetItemModStatus(item.key, "true", function(response){ server.SubmitQuizItem(item.index, submit_wrong_answers.concat(item.index),  topic_value , $('div#quiz_item_content_' + i + ' > div.item_inner').html(), item.page.url, item.page.proficiency.name, onItemAddSuccess); });

});
 
 
 
 

function onItemAddSuccess(response)
{
	
	
console.log('click link below to debug new quiz item key');

$.get('/debug/?quiz_item=' + response);

}



var scroll_width = 140 * answers.length;
$('#answers_container_' + i).find('.answer_candidates').css('width', scroll_width);   
answers_sliderInit(i);     


} // end of EditQuizItem()

*/


			
function UpdatePreviews(wrong_answers, ANSWER_LIMIT, i) {
for (w=0; w < ANSWER_LIMIT; w++){
if (wrong_answers[i][w]){
	// replace preview html with answer
	  $('div#answer_choice_previews_' + i).find('span#selection_' + w)
	  .html(wrong_answers[i][w][0]).append('<img class="remove_answer" src="/static/stylesheets/img/quiz_closebox_small.png">'); 
	  // add x close icon
	  
}
else{  $('div#answer_choice_previews_' + i).find('span#selection_' + w).html('No Selection'); }

}
	
}



function UpdateContent(value,i,el){ 

	stripped_value = value.split(' ').join('');
	stripped_value = stripped_value.split('\n').join('');
	if (stripped_value.length > 0){ el.html(value); }
	else { el.remove(); }

   PreviewAnswer(i);

return(value); }

function EditItemContent(i) { 
	$('#quiz_item_content_' + i + ' > div.item_inner > div').click(function(){  $(this).html().replace('style="opacity: 1;"', ''); });
	$('#quiz_item_content_' + i + ' > div.item_inner > div').editable(function(value, id){UpdateContent(value,i, $(this));}, {
		//loadurl : "/quizbuilder/rpc?action=Jeditable&arg0=" + $(this),
		type      : "autogrow",
		autogrow : {
		  lineHeight : 22
		 },
		// submit    : "OK",
		indicator : "<img src='/static/stylesheets/img/ajax-loader.gif'>",
		onblur    : "submit",
		// cancel    : "Cancel",
		tooltip   : "Click to edit...",
		width     : '600px',
		cssclass : "editable"
		}); // this can be rpc call 

}





function PreviewAnswer(i) {
	
	// On a hover over an answer, preview its text in the item content.

 	var answer_span = $('div#quiz_item_content_' + i + ' > div.item_inner').find('span');
     var answer_text = $('div#answer_choice_previews_' + i).find('span#correct').text().replace(/ /g, "&nbsp;");
	$('div#answers_' + i + ' > div').hover(function()
	{
        answer_span.html($(this).text().replace(/ /g, "&nbsp;"));
	},
	function()
	{
		answer_span.text('');
		answer_span.html(answer_text);
	});   
    
  
}





