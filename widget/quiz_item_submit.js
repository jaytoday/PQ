
$.plopquiz.submitAnswer = function(answer)
{
$.event.trigger("submittingAnswer");
// check the answer for special cases
// this will handle the non-skipping timeout on instructions2,
// the proficiencies, the score, and any other special boxes
switch($.plopquiz.quizItem.item_type)
{

case "intro":

// selected quiz subject is saved
var quiz_subject_choice = $('.intro_frame_content > .selected', $.plopquiz.quiz_content).find('.subject_guide').attr('id');
$.plopquiz.settings.proficiencies = Array(); // clear out proficiencies in case its a restart
$.plopquiz.settings.proficiencies.push(quiz_subject_choice);

$('button.take_test').hide();
$('div.go_to_site', $.plopquiz.answer_container).hide(); // temporary, while in development
$.plopquiz.loadItem();

case "instructions":
	
	if(!$.plopquiz.settings.instructions.i1complete)
			return;
	else
			$.plopquiz.loadItem();
break;

case "instructions2":
	if(!$.plopquiz.settings.instructions.skip_segment)
	{
			$.plopquiz.settings.instructions.i2timedOut = true;
			$.plopquiz.timer.stop();
			$.plopquiz.timer.css('width', '100%'); 
			$('.hover_example', $.plopquiz.quiz_content).hide();
			$('#example_1,#example_3', $.plopquiz.quiz_content).hide('slow');
			$('#example_2', $.plopquiz.quiz_content).show('slow');
			$('#skip', $.plopquiz.answer_container).show('slow');
			
			$('#skip', $.plopquiz.answer_container).show('slow');
			//click binding
			$('#answer1,#answer2', $.plopquiz.answer_container).addClass('disabled');
			$.plopquiz.settings.instructions.skip_segment = "true";

			return;
	}
	else
			$.plopquiz.loadItem();
		   $('#answer1,#answer2', $.plopquiz.answer_container).removeClass('disabled');
break;

case "begin_quiz":

	//$('#proficiency_choices input:checked', $.plopquiz.quiz_content).each(function() { $.plopquiz.settings.proficiencies.push($(this).val()); });
	$.plopquiz.timer.css('width', '100%'); 

	// this start the server session and retrieves the first questions
	// this can be refined
	// all RPC calls should be moved to one location
	$.ajax(
	{
			url: $.plopquiz.settings.serverUrl + "/quiztaker/rpc",
			dataType: "jsonp",
			cache: false,
			data:
			{
					action: "start_quiz",
					arg0: "[\"" + $.plopquiz.settings.proficiencies.join("\",\"") + "\"]"
			},
			success: function(rpc)
			{
					// the session token to submit answers and load quiz content
					if (!rpc.token) return $.plopquiz.fatalError('invalid quiz subject');
					else $.plopquiz.settings.sessionToken = rpc.token;

					// just echo what we send
					// reset the proficiencies here incase the server returns something different
					if(rpc.proficiencies)
							$.plopquiz.proficiencies = rpc.proficiencies;
					
					var q = rpc["quiz_item"];

					// instructions are done, we can skip them if the test is reset
					$.plopquiz.settings.instructions.completed = true;

					// load the first question
					$.plopquiz.loadItem($.extend({timed:true,"item_type":"quiz_item"}, q));
			}
		       // TODO: error  -- this is only for when the call itself doesn't work
	});
break;

case "quiz_item":
	// ajax call to submit -- (answer, key, vendor)
	var this_item = $.plopquiz.quizItem;
	
	var timer_status = $.plopquiz.timer.width()/$.plopquiz.settings.timer_width;
	var vendor = "" //TODO: retrieve vendor token.
	$(".timer_inner", self).stop();
	$.plopquiz.timer.css('width', '100%');
	$.ajax(
	{
			url: $.plopquiz.settings.serverUrl + "/quiztaker/rpc",
			dataType: "jsonp",
			data:
			{
					action: "continue_quiz",
					arg0: "\"" + answer + "\"",
					arg1: timer_status,
					arg2: "\"" + $.plopquiz.settings.sessionToken + "\"",
					arg3: "\"" + vendor + "\""
			},
			success: function(rpc)
			{
					var q = rpc["quiz_item"];
                    // no more quiz items left
					if(q === false) { 
					return $.plopquiz.loadItem({url: "/intro/?page=quiz_complete", item_type:"quiz_complete", noSkip: true, answers: [ "Submit" ]});
					}

					$.plopquiz.loadItem($.extend({timed:true,"item_type":"quiz_item"}, q));
			}
			//todo: ajax error
	});

   
break;

case "quiz_complete":
 $.event.trigger('quizclosing');
 
 /* Open results in new window -- This is turned off for now out of concerns of spamineess.
  * 
if($.plopquiz.settings.autoStart) window.location = "{{ http_host }}/redirect/from_quiz/" + $.plopquiz.settings.sessionToken;
else window.open("{{ http_host }}/redirect/from_quiz/" + $.plopquiz.settings.sessionToken);
  */

window.location = "{{ http_host }}/redirect/from_quiz/" + $.plopquiz.settings.sessionToken; // proceed in this window


  
break;

default:
	$.plopquiz.loadItem();
break;
};
};


