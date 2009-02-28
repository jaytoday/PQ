
/*
 * 
 * Global Settings
 * 
 */
  
 var DEFAULT_ANSWER_TEXT = 'No Selection';
 var DEFAULT_ANSWER_INPUT_TEXT = 'write a custom answer';
 var DEFAULT_TOPIC_TEXT = 'write a new topic';
 
 

$(function(){
    
 var quiz_count = parseInt( $('div.quiz_item:last').attr('id') );
 var scroll_width = 950 * quiz_count;
 $('div#quiz_items').css('width', scroll_width);

 $('input.new_answer').preserveDefaultText(DEFAULT_ANSWER_INPUT_TEXT);

 $('div.item_topic').change(function() {
            var $item_topic = $(this);
            if ($(this).find("option:selected").text() == "New Topic")  {
            $(this).find("select").hide().end()
                   .find('div.edit_topic').show().find('input').preserveDefaultText(DEFAULT_TOPIC_TEXT).end()
                                                 .find('button').click(function(){ return RefreshTopics($item_topic); }); 
          } 
          });
         
         
      		//submit_new_answer
      		$('input.new_answer').keydown(function(event){	
      	$(this).parent().find('input.submit_new_answer').show(); });
// Initialize Each Item
 $('.quiz_item').bind("initiate", function(){ initiateItem( $(this) )  });

          item_sliderInit();
   
   
   $('.answer_preview').find('span').click(function(){
    // edit answer value
    var this_answer_span = $(this).parent().find('span.selection'); 
    var this_input = $(this).parent().find('input'); 
    var these_spans = $(this).parent().find('span');
    var edit_div = $(this).parent().find('div.edit_answer');
    var current_answer = this_answer_span.text();
    if (current_answer != DEFAULT_ANSWER_TEXT) { this_input.val(this_answer_span.text()); }
    these_spans.hide();
    edit_div.show(); this_input.focus().keypress(function(evt){ if (evt.keyCode == 13) edit_div.find('button').click(); });
    edit_div.find('button').click(function(){
            // new answer value is submitted
            var new_answer = this_input.val();
            if (new_answer == DEFAULT_ANSWER_INPUT_TEXT || new_answer == '') { var new_value = DEFAULT_ANSWER_TEXT; }
            else { var new_value = new_answer; }
            if (new_value != current_answer) { $(this_answer_span.data('answer_link')).data('preview_index', -1); } //unlink from answer candidate
            $(this).parent().hide();
            this_answer_span.text(new_value); these_spans.show();
                                                       });          
            });



        	$('div.item_inner > div').editable(function(value, id){ UpdateContent(value, $(this));} , {
        		//loadurl : "/quizbuilder/rpc?action=Jeditable&arg0=" + $(this),
        		type      : "autogrow",
        		autogrow : { lineHeight : 22 },
        		// submit    : "OK",
        		indicator : "<img src='/static/stylesheets/img/ajax-loader.gif'>",
        		onblur    : "submit",
        		// cancel    : "Cancel",
        		tooltip   : "Click to edit...",
        		width     : '600px',
        		cssclass : "editable"
        		}); // this can be rpc call 



          
}); // end of onReady

/*


		

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
 


} // end of EditQuizItem()

*/




function initiateItem(item){    
       var wrong_answers = item.find('span.wrong', 'div.answer_preview').text(DEFAULT_ANSWER_TEXT);
       var answer_candidates = item.find('div.ac_wrapper');
       
        answer_candidates.click(function(){ 
        this_answer = $(this);
        wrong_answers.find('button').click();
        /*
        *
        * Check if answer has already been chosen
        *
        */ 

         if ( this_answer.data('selected') == true ){   
        // if answer text is already there, remove it 
                                              this_answer.removeClass('selected').data('selected', false); 
                                              var preview_index = this_answer.data('preview_index');
                                              if (preview_index < 0) return false; // link has been cancelled
                                              // $( wrong_answers[preview_index] ).text(''); 
                                                     // next step - for every answer between the answer preview and answerpreview.length, 
                                                     // move it back one
                                               for (a=(preview_index + 1);a = (wrong_answers.length - 1); a++){
                                                    $( wrong_answers[a - 1] ).text( $(wrong_answers[a]).text() )
                                                                             .data('answer_link', $(wrong_answers[a]).data('answer_link') ); 
                                                  $($( wrong_answers[a - 1] ).data('answer_link'))
                                                                             .data('preview_index', parseInt(a - 1));
                                                    $(wrong_answers[a]).text(DEFAULT_ANSWER_TEXT).data('answer_link', false);
                                                    return;                          
                                                               } //endfor  */
        return false; } //endif
        
        /*
        *
        * Proceed with adding item
        *
        */
        
        answer_candidates.removeClass('selected').data('selected', false); 
        // push existing answers   
        // TODO: This doesn't work yet  
       for (a = (wrong_answers.length - 1); a = 0; a = (a - 1) ){ 
           console.log('pushing answer: ', $(wrong_answers[a - 1]).text());
          $( wrong_answers[a] ).text( $(wrong_answers[a - 1]).text() ).data('answer_link', $(wrong_answers[a - 1]).data('answer_link') ); 
          $($( wrong_answers[a] ).data('answer_link'))
                                   .data('preview_index', a).addClass("selected").data('selected', true); 
                                                        return; }  
        // add new answer to previews
       $(wrong_answers[0]).text(this_answer.text()).data('answer_link', $(this));
        // highlight chosen answer  button
        $(this).addClass("selected").data('selected', true).data('preview_index', 0 );
        return;
        
    	});


         
                 }  // end initiateItem			
        			




			
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



function UpdateContent(value,el){ 
/*
	stripped_value = value.split(' ').join('');
	stripped_value = stripped_value.split('\n').join('');
	if (stripped_value.length > 0){ el.html(value); }
	else { el.remove(); }
*/
  // PreviewAnswer(i);

el.html(value);

return(value); 

}

function EditItemContent(i) { 
	$('#quiz_item_content_' + i + ' > div.item_inner > div').click(function(){  $(this).html().replace('style="opacity: 1;"', ''); });

}





function PreviewAnswer(i) { // TODO: Make this work again 
	
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


function RefreshTopics(item_topic){
  if (item_topic.data('busy') == true) return false;
  //validate input
  var new_topic = item_topic.find('input').val();
  if (new_topic.length < 1) return false;
  
  item_topic.find('div.edit_topic').hide('fast').end()
  .find('div.loading').show('fast').end()
            .data('busy', true);
            
    	$.ajax({
                    
                    type: "POST",
                    url:  "/quizeditor/rpc/post",
                    data:
                    {
                            action: "NewTopic",
                            subject_name: item_topic.attr('id'),
                            topic_name: new_topic
                    },
                    success: function(response)
                    { 	$('div.item_topic').html(response); item_topic.data('busy', false);	}
               });
               
               return; 
    
}


