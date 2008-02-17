
$.plopquiz.submitAnswer = function(answer)
{
$.event.trigger("submittingAnswer");
// check the answer for special cases
// this will handle the non-skipping timeout on instructions2,
// the proficiencies, the score, and any other special boxes
if ($.plopquiz.answers.data('disabled') == true) return false;


switch($.plopquiz.quizItem.item_type)
{

case "intro":

// selected quiz subject is saved
var quiz_subject_choice = $('.intro_frame_content > .selected', $.plopquiz.quiz_content).find('.subject_guide').attr('id');
$.plopquiz.settings.proficiencies = Array(); // clear out proficiencies in case its a restart
$.plopquiz.settings.proficiencies.push(quiz_subject_choice);

$('button.take_test').hide();
$('div#points', $.plopquiz.quiz_inner_content).hide();

// repeat the tutorial if re-opened
$.plopquiz.settings.instructions.i1complete = false; 
$.plopquiz.settings.instructions.skip_segment = false;
$.plopquiz.settings.instructions.i2timedOut = false;

//if ($.plopquiz.settings.instructions.completed) $.plopquiz.currentItem = 3; // skips tutorial already completed
	 
$.plopquiz.loadItem();



case "instructions":
	
	if(!$.plopquiz.settings.instructions.i1complete)
			return;
	else{
			$('div#instructions_quiz_selection', $.plopquiz.quiz_content).hide(); //fixes safari bug
			$.plopquiz.loadItem();
		}
break;

case "instructions2":
if ($.plopquiz.settings.instructions.skip_segment == false)
	{
			$.plopquiz.settings.instructions.i2timedOut = true;
			$.plopquiz.timer.stop();
			$.plopquiz.timer.css('width', '100%'); 
			$('.hover_example', $.plopquiz.quiz_content).hide();
			$('#example_1,#example_3', $.plopquiz.quiz_content).hide('slow');
			$('#example_2', $.plopquiz.quiz_content).show('slow');
			$.plopquiz.settings.instructions.skip_segment = true;
			$('#skip', $.plopquiz.answer_container).data('disabled', false).show('slow');
			return;
	}
	else{
		  if (answer != "Skip") return false; // must press Skip to continue
		  $.plopquiz.loadItem();
		  $.plopquiz.settings.instructions.skip_segment = false; 
		}
break;

case "begin_quiz":

	if ($.plopquiz.answers.data('disabled') != false) return false; // problems with double submits
	$.plopquiz.answers.data('disabled',true);
	$.plopquiz.quiz_inner_content.addClass('disabled').animate({opacity:0},100); 
	$.plopquiz.quiz_loader.show().animate({opacity: .5 }, {duration:100});
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
					// load the first question (we already have  it from the rpc call)
					$.plopquiz.loadItem($.extend({timed:true,"item_type":"quiz_item"}, q));
			}
		       // TODO: error  -- this is only for when the call itself doesn't work
	});
break;

case "quiz_item":
	if ($.plopquiz.answers.data('disabled') != false) return false; 

	
	// ajax call to submit -- (answer, key, vendor)
	$.plopquiz.timer.stop();
	var timer_status = $.plopquiz.timer.width()/$.plopquiz.settings.timer_width;
	var this_item = $.plopquiz.quizItem;
	var vendor = "" //TODO: retrieve vendor token.
	
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
                    // no moAt the end of a quiz, it should reset so that a new quiz session could be established from the same page. re quiz items left
					if(q === false) { 
					return $.plopquiz.loadItem({url: "/intro/?page=quiz_complete", item_type:"quiz_complete", noSkip: true, answers: [ "Submit" ]});
					}

					$.plopquiz.loadItem($.extend({timed:true,"item_type":"quiz_item"}, q));
			}
			//todo: ajax error
	});

   
break;

case "quiz_complete":

$.plopquiz.quiz_inner_content.addClass('disabled').animate({opacity:0},100); 
	
$.plopquiz.quiz_loader.show().animate({opacity: .5 });
 
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


