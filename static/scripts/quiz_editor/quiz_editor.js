
/*
 * 
 * Global Settings
 * 
 */
  
 var DEFAULT_ANSWER_TEXT = 'No Selection';
 var DEFAULT_ANSWER_INPUT_TEXT = 'write a custom answer';
 var DEFAULT_TOPIC_TEXT = 'write a new topic';
 var DEFAULT_QUIZ_ITEM_TEXT = 'Click here to write quiz item text...';
 

$(function(){
    
 var quiz_count = parseInt( $('div.quiz_item:last').attr('id') );
 var scroll_width = 950 * quiz_count;
 $('div#quiz_items').css('width', scroll_width);



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

          // Initiate Item Slider
          item_sliderInit();
   
   
   $('.answer_preview').find('span').click(function(){
    // edit answer value
    var this_answer_span = $(this).parent().find('span.selection'); 
    var this_input = $(this).parent().find('input'); 
    var these_spans = $(this).parent().find('span');
    var edit_div = $(this).parent().find('div.edit_answer');
    if (this_answer_span.text() != DEFAULT_ANSWER_TEXT) { this_input.val(this_answer_span.text()); }
    these_spans.hide();
    edit_div.show(); this_input.focus().keypress(function(evt){ if (evt.keyCode == 13) edit_div.find('button').click(); });
    edit_div.find('button').click(function(){
            // new answer value is submitted
            var new_answer = this_input.val();
            if (new_answer == DEFAULT_ANSWER_INPUT_TEXT || new_answer == '') { var new_value = DEFAULT_ANSWER_TEXT; }
            else { var new_value = new_answer; } 
            if (new_value != this_answer_span.text()) { $(this_answer_span.data('answer_link')).data('preview_index', -10); } //unlink from answer candidate
            $(this).parent().hide();
            this_answer_span.text(new_value); these_spans.show();
                                              return;         });          
          return;  });






          
}); // end of onReady

/*


		

EditItemContent(i);
            
$('form#quiz_data_' + i).find('input[@name="submit_item"]').click(function() {         //moderated=true
	var topic_value = eval('document.quiz_data_' + i + '.item_topic.value');
	if (topic_value == 'Pick a Topic'){ console.info('Pick a Topic!'); return false; }
	if (topic_value == 'New Topic'){ topic_value = eval('document.quiz_data_' + i + '.new_item_topic.value'); }


var submit_answer_previews = [];
for (w=0; w < answer_previews[i].length; w++){
submit_answer_previews.splice(answer_previews[i].length, 0, answer_previews[i][w][0]); 
}

if (submit_answer_previews.length < 2){ console.info('not enough answers!'); return false;  }

if ($('div#quiz_item_content_' + i + ' > div.item_inner').html().length > 500){ console.info('quiz item is too long!'); return false; }

// proceed to next quiz item
$('.quizbuilder_wrapper .scroller').trigger('next');



  //                                                           correct          all answers                            topic value                                     HTML                                                              url         proficiency
 server.SetItemModStatus(item.key, "true", function(response){ server.SubmitQuizItem(item.index, submit_answer_previews.concat(item.index),  topic_value , $('div#quiz_item_content_' + i + ' > div.item_inner').html(), item.page.url, item.page.proficiency.name, onItemAddSuccess); });

});
 
 
 
 

function onItemAddSuccess(response)
{
	
	
console.log('click link below to debug new quiz item key');

$.get('/debug/?quiz_item=' + response);

}




} // end of EditQuizItem()

*/




function initiateItem(item){   
	 
       var answer_previews = item.find('span.wrong', 'div.answer_preview');
       answer_previews.each(function(){ 
       	  var this_input = $(this).parent().find('input');
       	  if ($(this).text().length < 1) { $(this).text(DEFAULT_ANSWER_TEXT); this_input.preserveDefaultText(DEFAULT_ANSWER_TEXT); }
       	  else {  this_input.val($(this).text()); }
	   });

        var correct_answer = item.find('span.correct', 'div.answer_preview');
         correct_answer.each(function(){ 
       	  var this_input = $(this).parent().find('input');
       	  if ($(this).text().length < 1) { $(this).text(DEFAULT_ANSWER_TEXT); this_input.preserveDefaultText(DEFAULT_ANSWER_TEXT); }
       	  else {  this_input.val($(this).text()); }
	   });
	   

       var content = item.find('div.content', 'div.quiz_item_content')
       if (content.text().length < 1) content.text(DEFAULT_QUIZ_ITEM_TEXT);

       	content.editable(function(value, id){ UpdateContent(value, $(this));} , {
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
    //   	if ($(this).text() == DEFAULT_QUIZ_ITEM_TEXT) $(this).text('');
          
          
          
          
// wait until answers are loaded
item.bind("initiateAnswers", function() {
       		
       		
       var answer_candidates = item.find('div.ac_wrapper');
       
        answer_candidates.click(function(){ 
        this_answer = $(this);
        answer_previews.find('button').click();
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


		 $( answer_previews[preview_index] ).text(DEFAULT_ANSWER_TEXT).data('answer_link', false);
		 // next step - for every answer between the answer preview and answerpreview.length, 
		 // move it back one
		for (a=(preview_index + 1); a < answer_previews.length; a++){
			$( answer_previews[a - 1] ).text( $(answer_previews[a]).text() )
									 .data('answer_link', $(answer_previews[a]).data('answer_link') ); 
			$($( answer_previews[a - 1] ).data('answer_link'))
									 .data('preview_index', parseInt(a - 1));
			$(answer_previews[a]).text(DEFAULT_ANSWER_TEXT).data('answer_link', false);
		continue;  } //endfor  */
  return false; } //endif
        
        /*
        *
        * Proceed with adding item
        *
        */
        
        answer_candidates.removeClass('selected').data('selected', false).data('preview_index', -1 ); 

       for (a = (answer_previews.length - 1); a > 0; a-- ){ 

           if ( $(answer_previews[a - 1]).text() == DEFAULT_ANSWER_TEXT) continue;
          $( answer_previews[a] ).text( $(answer_previews[a - 1]).text() ).data('answer_link', $(answer_previews[a - 1]).data('answer_link') ); 
          $($( answer_previews[a] ).data('answer_link'))
                                   .data('preview_index', a).addClass("selected").data('selected', true); 
                     
           continue;  }  
        // add new answer to previews
       $(answer_previews[0]).text(this_answer.text()).data('answer_link', $(this));
        // highlight chosen answer  button
        $(this).addClass("selected").data('selected', true).data('preview_index', 0 );
        
        
        return;
        
    	});



}); // end initiateAnswers		



$('button.submit_item', item).click(function(){  SubmitItem(item); });

                 }  // end initiateItem			
        			





function UpdateContent(value,el){ 
/*
	stripped_value = value.split(' ').join('');
	stripped_value = stripped_value.split('\n').join('');
	if (stripped_value.length > 0){ el.html(value); }
	else { el.remove(); }
*/
  // PreviewAnswer(i);


if (value.length < 1) el.html(DEFAULT_QUIZ_ITEM_TEXT)
else el.html(value);

return(value); 

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


function SubmitItem(item){
  if (item.data('submitting') == true) return false;
  item.data('submitting', true);
  var this_button = $('button.submit_item', item).attr('disabled', true); 
  	
	var subject_name = $('div.subject_name', item).text();
	var topic_name = $('div.item_topic', item).find("option:selected").text();
	var correct_answer = $('span.correct', item).text(); 
	var answers = Array();
	$('span.wrong', item).each(function(){ answers.push($(this).text()); });
	$('span.correct', item).each(function(){ answers.push($(this).text()); });
	var item_text = item.find('div.content', 'div.quiz_item_content').text();
	var item_key = this_button.attr('id');
	
  // do we also want to collect the answer suggestions, or do we let them float away like tears in the rain?

    	$.ajax({
                    
                    type: "POST",
                    url:  "/quizeditor/rpc/post",
                    data:
                    {
                            action: "SubmitItem",
                            subject_name: subject_name,
                            topic_name: topic_name,
                            correct_answer: correct_answer,
                            answers: answers,
                            item_text: item_text,
                            item_key: item_key
                    },
                    success: function(response)
                    { 	item.html(response).data('submitting', false);
                        this_button.attr('disabled', false);	}
               });
               
               return; 
    
}
