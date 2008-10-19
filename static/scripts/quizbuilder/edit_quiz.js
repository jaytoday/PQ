ANSWER_LIMIT = 2; 

function BuildQuizEditor(response){
	
	
	
var raw_quiz_items = parseJSON(response);

if (raw_quiz_items.length == 0) { $('div#loading_items').html('no quiz items returned -- <a href="">try again?</a>'); }  // no items returned
if (raw_quiz_items[0] == "error") { $('div#loading_items').html('error: ' + raw_quiz_items[1]); }  // error


var scroll_width = 950 * raw_quiz_items.length;
$('div#quiz_items').css('width', scroll_width);

 $.each(raw_quiz_items, function(i,item){


$('ul.item_navigation').append('<li><a href="#' + i + '">' + item.index + '</a></li>');
	
 	
// raw item template 	-- use jsrepeater template
 	
var html = '<div class="quiz_item"  id="' + i + '" >';


html += '<div class="quiz_item_content" id="quiz_item_content_' + i + '"><div class="item_inner">'; // start quiz item content

html += '<div class="pre_content">' + item.pre_content + '</div>';

html += '<div class="content" >' + item.content + '</div>';

html += '<div class="post_content">' + item.post_content + '</div>';

html += '</div></div>'; //end quiz item content

html += '<div class="quiz_form"><form id="quiz_data_' + i + '" name="quiz_data_' + i + '"><input type="text" name="slug" class="slug_name" value="slug_name" /><br/><input type="text" name="category" class="category_name" value="category" /><br/><input type="submit" onClick="return false;this.disabled = true;" id="submit_item_' + i + '" class="submit_item" value="Submit Quiz Item" /></form></div>';

html += '<div class="answers_container" id="' + i + '" ><div class="answer_candidates" id="answers_' + i + '"></div></div>';  // Expand answer candidates


html += '<div id="answer_choice_previews_' + i + '" class="answer_choice_previews">';

html += '<div class="answer_preview" ><div class="correct">Correct Answer</div><span class="selection">' + item.index + '</span></div>';



for (w = 0; w < ANSWER_LIMIT; w++){
 	 
html += '<div class="answer_preview"><div class="wrong">Wrong Answer #' + (w + 1) + '</div><span class="selection" id="selection_' + w + '">No Selection</span></div>';

}


html += '<div class="new_answer" id="' + i + '"><div class="submit_new_answer">you can also</div><input type="text" name="new_answer" class="new_answer" value="  write a custom answer" /> </div>';  // User submitted answer


html += '<input type="submit" name="submit_item" class="submit_item" value="submit item" />';  // User submitted answer



html += '</div>';





html +=  '<table id="dpop" class="popup" style="display:none;"></table>'; // pop-up bubble message


// load items
$('div#quiz_items').append(html);
$('div#quiz_items').find('.popup').load('/static/html/quizbuilder/popup.html');
$('div#loading_items').hide();
$('ul.item_navigation').show('slow');
$('div#quiz_items').show('slow');



$('.new_answer').preserveDefaultText('  write a custom answer');
// when something is written in this field, a submit button should appear below




answers =  eval(item.answer_candidates); //item.answer_candidates



 $.each(answers, function(n, answer){
 	
 	
answer_html = '<div id ="' + n + '" class="ac_container"><div id ="' + n + '" class="answer_candidate" >' + answer + '</div></div>';


$('div#answers_' + i).append(answer_html);

});




EditQuizItem(i, item, answers); // Run function after the above code is evaluated.



}); // finished with item loop 



// PopUpBubble(); should be done once and apply to all 


sliderInit();   

}






function EditQuizItem(i, item, answers) {
    
 
  
wrong_answers[i] = [];
answer_in_array[i] = [];    

 $.each(answers, function(n, answer){
 	
 answer_in_array[i][n] = "False"; 
 
});


 
 //$('div#' + i + ' > div#quiz_item_content').jScrollPane();

// $('div#answers_' + i).jScrollPane();
 
// $('#quiz_item_content').markItUp(mySettings);
   
   
 
 $('input[@name="submit_item"]').click(function(){ console.log($(this).parent().parent()); });
 	     

$('#quiz_data_' + i + ' > input[@name="proficiency"]').click(function(){
$('#quiz_data_' + i + ' > input[@name="proficiency"]').setValue($(this).attr("value"));
});


    
$('div#answers_' + i + '').find('.ac_container').click(function(){
			
//    If answer is selected, remove it if it's already in array. 
//    If not, add it to the array, if the limit hasn't been reached. 

answer_text = $(this).text();

n = $(this).attr("id");


for (var a = -1, loopCnt = wrong_answers[i].length; a < loopCnt; a++) {



if (answer_text == wrong_answers[i][a]){   // if answer text is already there


wrong_answers[i].splice(wrong_answers[i].indexOf(answer_text), 1);
UpdatePreviews(wrong_answers, ANSWER_LIMIT);

answer_in_array[i][n] = "False"; // answer not in array anymore


$(this).css("background","#FFFFDB none repeat scroll 0 0"); 
$(this).css("font-weight","normal"); 
$(this).css("font-size","1em"); 

console.log('removed text');
return;


}

}

console.log('array', wrong_answers[i]);

if (answer_in_array[i][n] == "False") {

if (wrong_answers[i].length > (ANSWER_LIMIT - 1)) { console.log("Only 2 Wrong Answers, Please!"); $("div.answers_container").fadeTo(50, 0.5).fadeTo(50, 1); return false; }  // If there are already two answers

wrong_answers[i].splice(wrong_answers[i].length, 0, answer_text);   // add answer to array
UpdatePreviews(wrong_answers, ANSWER_LIMIT);

answer_in_array[i][n] == "True";


  $(this).css("background","#FFFFA1 none repeat scroll 0 0"); 
  $(this).css("font-weight","bold"); 
  $(this).css("font-size",".9em"); 
  
  console.log('added item', answer_text, wrong_answers[i],wrong_answers[i].length);
  return;
  
}

    

			});
			
			
function UpdatePreviews(wrong_answers, ANSWER_LIMIT) {
	console.log($('div#answer_choice_previews_' + i));
for (w=0; w < ANSWER_LIMIT; w++){

if (wrong_answers[i][w]){  $('div#answer_choice_previews_' + i).find('span#selection_' + w).html(wrong_answers[i][w]); }
else{  $('div#answer_choice_previews_' + i).find('span#selection_' + w).html('No Selection'); }

}
	
}			

	

for (w=0; w < ANSWER_LIMIT; w++){

	console.log($('#answer_choice_previews_' + i).find('span#selection_' + w));
	
	//console.log($('div#'+i).find('div#answer_choice_previews_' + i).find('span#selection_' + w));
$('#answer_choice_previews_' + i).find('span#selection_' + w).click(function(){
	console.log($(this).text());
	
	// remove answer in array that matches $(this).text()
	//console.log(wrong_answers[i][w]);
	 //UpdatePreviews(wrong_answers, ANSWER_LIMIT);
    }); }
    
    


PreviewAnswer(i);


EditItemContent(i);

            
        
$('#submit_item_' + i).click(function() {
	
	// Edited quiz item is submitted. 
    

console.log(eval('document.quiz_data_' + i + '.slug.value'));

console.log(eval('document.quiz_data_' + i + '.category.value'));

console.log(wrong_answers[i]);

console.log($('div#quiz_item_content_' + i).html())



 server.SubmitQuizItem(item.index, wrong_answers[i].concat(item.index), eval('document.quiz_data_' + i + '.slug.value'),   eval('document.quiz_data_' + i + '.category.value'), $('div#quiz_item_content_' + i).html(),  onItemAddSuccess);
});
 
 
 
 

function onItemAddSuccess(response)
{
    console.log(response);
}


   
    

}






function UpdateContent(value,i,el){ 
	if (value.length > 0){ el.html(value); }
	else { el.remove(); }

   PreviewAnswer(i);

return(value); }

function EditItemContent(i) { 
	
	//console.log($('#quiz_item_content_' + i));
	
	$('#quiz_item_content_' + i + ' > div.item_inner > div').editable(function(value, id){UpdateContent(value,i, $(this));}, {
      type      : "autogrow",
      autogrow : {
                  lineHeight : 22
                 },
      submit    : "OK",
      onblur    : "submit",
      cancel    : "Cancel",
      tooltip   : "Click to edit...",
      cssclass : "editable"
		}); // this can be rpc call 

}





function PreviewAnswer(i) {
	
	// On a hover over an answer, preview its text in the item content.

 	var answer_span = $('div#quiz_item_content_' + i + ' > div.item_inner').find('.answer_span');
 	var answer_text = answer_span.text();
	$('#answers_' + i + '').find('.ac_container').hover(function()
	
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

