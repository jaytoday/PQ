ANSWER_LIMIT = 2; 



function BuildQuizEditor(response, topics){
var raw_quiz_items = parseJSON(response);

if (raw_quiz_items.length == 0) { $('div#loading_items').html('no quiz items returned -- <a href="">try again?</a>'); return false;}  // no items returned
if (raw_quiz_items[0] == "error") { $('div#loading_items').html('error: ' + raw_quiz_items[1]); return false; }  // error


var scroll_width = 950 * raw_quiz_items.length;
$('div#quiz_items').css('width', scroll_width);

//$('div#quiz_items').append('<div class="quiz_item"></div>');

 $.each(raw_quiz_items, function(i,item){


$('ul.item_navigation').append('<li class="index"><a href="#' + i + '" onClick="return false;">' + item.index + '</a></li>');   // href="#' + i + '" -- for navigation. 
	
 	
// raw item template 	-- use jsrepeater template
 	
var html = '<div class="quiz_item"  id="' + i + '" ><form id="quiz_data_' + i + '" name="quiz_data_' + i + '">';

html += '<div class="quiz_item_content" id="quiz_item_content_' + i + '"><div class="item_inner">'; // start quiz item content

html += '<div class="pre_content">' + item.pre_content + '</div>';

html += '<div class="content" >' + item.content + '</div>';

html += '<div class="post_content">' + item.post_content + '</div>';

html += '</div></div>'; //end quiz item content

html += '<div class="answers_container" id="answers_container_' + i + '" ><div class="answers_scroll"><div class="answer_candidates" id="answers_' + i + '"></div></div></div>';  // Expand answer candidates

html += '<div id="answer_choice_previews_' + i + '" class="answer_choice_previews">';

html += '<div class="answer_preview" ><div class="correct">Correct Answer</div><span class="selection" id="correct">' + item.index + '</span><div id="new_index" style="display:none;"><input type="text" name="new_index" class="new_index" value="" /><input type="submit" name="submit_new_index" class="submit_new_index" onClick="return false;" value="ok" /></div></div>';

// item.page.url is webpage

for (w = 0; w < ANSWER_LIMIT; w++){
 	 
html += '<div class="answer_preview"><div class="wrong">Wrong Answer #' + (w + 1) + '</div><span class="selection" id="selection_' + w + '">No Selection</span></div>';

}


html += '<div class="new_answer" id="' + i + '" ><input type="text" name="new_answer" class="new_answer" value="write a custom answer" /><input type="submit" name="submit_new_answer" class="submit_new_answer" onClick="return false;" value="ok" /> </div>';  // User submitted answer


html += '<div class="select_topic" id="select_topic_' + i + '"><select name="item_topic" class="item_topic"><option>Pick a Topic</option></select><input type="text" name="new_item_topic" maxlength="11" class="new_item_topic" style="display:none;"  value="write a new topic" /></div>';

html += '<input type="submit" name="submit_item" class="submit_item" onClick="return false;" value="submit item" />';  // Submit Item
html += '<input type="submit" name="skip_item" class="skip_item" onClick="return false;" value="skip item" />';  // skip Item


html += '</form></div>';





html +=  '<table id="dpop" class="popup" style="display:none;"></table>'; // pop-up bubble message


// load items
$('div#quiz_items').append(html);
//$('div#quiz_items').find('.popup').load('/static/html/quizbuilder/popup.html');





$('.new_answer').preserveDefaultText('write a custom answer');
//$('.item_topic').preserveDefaultText('        topic');
// when something is written in this field, a submit button should appear below




answers =  eval(item.answer_candidates); //item.answer_candidates

 $.each(answers, function(n, answer){
 	
answer_html = '<div id ="' + n + '" class="ac_unselected"><div id ="' + n + '" class="answer_candidate" >' + answer + '</div></div>';

$('div#answers_' + i).append(answer_html);

});

$.each(eval(topics), function(t, topic){

topic_option = '<option>' + topic.name + '</option>';	

$('div#select_topic_' + i).find('select.item_topic').append(topic_option);

});

$('div#select_topic_' + i).find('select.item_topic').append('<option>New Topic</option>');

$("select").change(function() {
	console.log('changing', $('div#select_topic_' + i).find("select option:selected"));
          if ($('div#select_topic_' + i).find("select option:selected").text() == "New Topic") { $(this).hide(); $(this).parent().find('input.new_item_topic').show().preserveDefaultText('write a new topic'); } 
        })





EditQuizItem(i, item, answers); // Run function after the above code is evaluated.



}); // finished with item loop 



// PopUpBubble(); should be done once and apply to all 


item_sliderInit();   


$('ul.item_navigation').show();
$('div#quiz_items').show();

$('div#loading_items').remove();

} // end of  BuildQuizEditor()






function EditQuizItem(i, item, answers) {

// setup for ajax call     
var server = {};
InstallPostFunction(server, 'SubmitQuizItem', 'quizbuilder');  // POST Request
InstallFunction(server, 'SetItemModStatus', 'quizbuilder');

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


console.log('removed text');
return;


}

}

console.log('array', wrong_answers[i]);

if (answer_in_array[i][n] == "False") {

if (wrong_answers[i].length > (ANSWER_LIMIT - 1)) { console.log("Only 2 Wrong Answers, Please!"); $("div.answers_container").fadeTo(50, 0.5).fadeTo(50, 1); return false; }  // If there are already two answers

var answer_pair = [answer_text, n];
wrong_answers[i].splice(wrong_answers[i].length, 0, answer_pair);   // add answer to array
UpdatePreviews(wrong_answers, ANSWER_LIMIT, i);

answer_in_array[i][n] == "True"; // this isn't needed.

$(this).removeClass("ac_unselected");
$(this).addClass("ac_selected");

  console.log('added item', answer_pair, wrong_answers[i],wrong_answers[i].length);
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
});

$('#answer_choice_previews_' + i).find('input[@name="submit_new_index"]').click(function(){
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

console.log($('div#quiz_item_content_' + i + ' > div.item_inner').html().length);
if ($('div#quiz_item_content_' + i + ' > div.item_inner').html().length > 500){ console.info('quiz item is too long!'); return false; }

// proceed to next quiz item
$('.quizbuilder_wrapper .scroller').trigger('next');



  //                                                           correct          all answers                            topic value                                     HTML                                                              url         proficiency
 server.SetItemModStatus(item.key, "true", function(response){ server.SubmitQuizItem(item.index, submit_wrong_answers.concat(item.index),  topic_value , $('div#quiz_item_content_' + i + ' > div.item_inner').html(), item.page.url, item.page.proficiency.name, onItemAddSuccess); });

});
 
 
 
 

function onItemAddSuccess(response)
{
console.log('new quiz item key:', response);
}



var scroll_width = 140 * answers.length;
$('#answers_container_' + i).find('.answer_candidates').css('width', scroll_width);   
answers_sliderInit(i);     


} // end of EditQuizItem()




			
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
 	var answer_text = answer_span.html();
 	
	$('div#answers_' + i + ' > div').hover(function()
	
	{
        //answer_span.fadeTo(1,0.5);
        answer_span.html($(this).text());
	    answer_span.fadeTo("slow", 1);
	
	},
	function()
	{
	    
		answer_span.empty();
		answer_span.html(answer_text);
        //answer_span.fadeTo(100, 0.5);
	});   
    
  
}






// Pop-up Bubble
function PopUpBubble() {
  $('.answers_container').each(function () {
  	
    // options
    var distance = 10;
    var time = 250;
    var hideDelay = 200;

    var hideDelayTimer = null;

    // tracker
    var beingShown = false;
    var shown = false;
    
    var trigger = $('.answer_candidates', this);
    var popup = $('.popup').css('opacity', 0);

    // set the mouseover and mouseout on both element
    $([trigger.get(0), popup.get(0)]).mouseover(function () {
    	
      // stops the hide event if we move from the trigger to the popup element
      if (hideDelayTimer) clearTimeout(hideDelayTimer);

      // don't trigger the animation again if we're being shown, or already visible
      if (beingShown || shown) {
        return;
      } else {
        beingShown = true;

        // reset position of popup box
        popup.css({
          top: 380,
          left: 183,
          display: 'block' // brings the popup back in to view
        })

        // (we're using chaining on the popup) now animate it's opacity and position
        .animate({
          top: '-=' + distance + 'px',
          opacity: 1
        }, time, 'swing', function() {
          // once the animation is complete, set the tracker variables
          beingShown = false;
          shown = true;
        });
      }
    }).mouseout(function () {
      // reset the timer if we get fired again - avoids double animations
      if (hideDelayTimer) clearTimeout(hideDelayTimer);
      
      // store the timer so that it can be cleared in the mouseover if required
      hideDelayTimer = setTimeout(function () {
        hideDelayTimer = null;
        popup.animate({
          top: '-=' + distance + 'px',
          opacity: 0
        }, time, 'swing', function () {
          // once the animate is complete, set the tracker variables
          shown = false;
          // hide the popup entirely after the effect (opacity alone doesn't do the job)
          popup.css('display', 'none');
        });
      }, hideDelay);
    });
  });
}

