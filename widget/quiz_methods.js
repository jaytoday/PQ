

function loadQuizMethods(html){
	/*
	 * Note: This is run before the quiz frame is loaded.
	 * $.plopquiz.start runs when the quiz frame is loaded
	 * 
	 * TODO: Could use some refactoring.....we shouldn't be rebinding and defining functions with every item load
	 */ 

	// add to body to overlay is in front
$("body").append(html);

// resize overlay to document not window
function drawOverlay(){
$("#quiz_overlay").css("height", $(document).height());
}

drawOverlay();
$(window).resize(drawOverlay); // whenever window is resized, overlay will be drawn. 


// starting and stopping quiz
$("#pq_wrapper")
.bind("quizstarting", function()
{

	// if quiz is loaded from widget, show loading icon on widget. otherwise, immediately show overlay
	if(!$.plopquiz.settings.autoStart) $.plopquiz.widget_wrapper.find('button').hide().end().find('.widget_load').show();
	else { $.event.trigger("displayQuiz");  $('#quiz_inner').hide();  $('#quiz_init').show();  }
	
	// load first item
	$.plopquiz.loadItem();
	
	
	
})
.bind("displayQuiz", function()
{

	$('#widget_wrapper').fadeOut(); $(this).show();
	
})
.bind("answerhover", function()
{
//Fire initial hover event.
if ( $('#quiz_answers .hover_answer', $.pq_wrapper).length > 0 ){ onAnswerHover($('#quiz_answers .hover_answer', $.pq_wrapper)[0]);  }
})
.bind("quizclosing", function()
{
	$(this).hide();
	$('#widget_wrapper').fadeIn().find('button').css('display', 'inline').end().find('.widget_load').hide();
	// wipe quiz session. TODO: this should handle skipping instructions; 
	$.plopquiz.currentItem = 0;
	$.plopquiz.settings.instructions.completed = false;
    // if we want to redirect to the PQ site
    // if($.plopquiz.settings.autoStart) window.location = "{{ http_host }}/login";
});

// close button
$("#quiz_close").click(function()
{
$.event.trigger("quizclosing");

});

// timer controls. listens for startTimer, loadingQuizItem, submitingAnswer
$("#quiz_timer")
.bind("startTimer", function(event, quizItem)
{
	var self = this;

	if(!quizItem || !quizItem.timed || $.plopquiz.settings.noTimer)
			return;

	// reset and start timer.
	var reset = function()
	{
			
$.plopquiz.settings.timer_width = $('.timer_bar').width(); // to calculate score
			 


$.plopquiz.timer.animate({opacity: 1.0}, 2000, function() //temporarily pause the timer 
{
$.plopquiz.answers.removeClass('disabled').data("disabled", false);

$.plopquiz.answer_load_icons.animate({opacity: 0}, 300);

$.plopquiz.answer_text.animate({opacity: 1}, 300);

$.event.trigger("answerhover");
												
			$.plopquiz.timer.animate( // start running the timer down
			{ width: 0 },
			{
					complete: function()
					{
							// this should (could?) be a special, only used on instruction2
							if(quizItem.timeout == "reset")
							{
									if(quizItem.timed)
											$.plopquiz.specialTimers[quizItem.timed]();

									$(self).stop();
									
									return reset();
							}

							// when ever this is reach, fail the question
							$.plopquiz.submitAnswer("skip");
					},
					duration: $.plopquiz.settings.timeoutDuration,
					easing: "linear"
			})
			.show();
			

});
}

	reset();
})
// these probably do the same thing
.bind('loadingQuizItem', function()
{
	$.plopquiz.answers.removeClass('disabled').data("disabled", true);
	$.plopquiz.timer.stop();
})
.bind('submitingAnswer', function()
{
	$.plopquiz.timer.stop();
});

$('#quiz_answers .answer', $.pq_wrapper).hover(
		function(){ onAnswerHover(this); },
		function() { offAnswerHover(this); }  )
.click(function(e) // submit answer
{
	// data("disabled") prevents double submissions
	if($(this).data("disabled") == false){ 	$.plopquiz.submitAnswer($(this).find('div.answertext').text().replace(/\n/g,"")); }
})


$("#quiz_content", $.pq_wrapper)
// when the item is loaded, fade in, then trigger startTimer
.bind("quizItemLoaded", function(e, quizItem)
{
  
   	 // redraw timer
	$.plopquiz.timer.stop().css("width", "100%");
	//Reset the size of blank fields
    $("#blank", $.plopquiz.quiz_content).text($.plopquiz.textHolder).css("cssText", "width: 105px !important;");  
	$("#quiz_content", $.pq_wrapper).animate({opacity: 1},{ duration: 1000, // delay start of timer 
			complete: function()
			{$.event.trigger("startTimer", [ quizItem ]); } });
			
	$.event.trigger("answerhover");		
    

});



//  auto-start
if($.plopquiz.settings.autoStart) $.plopquiz.start();
else $.plopquiz.load_widget();



//confirm setup is finished
$('body').data('pq','True');







} // end of startQuiz


function onAnswerHover(answer) // when answer is hovered
{
	
// skip doesn't have hover
if ($(answer).attr("id") == "skip")
	return;

	// hover event on span
	$(answer).addClass('hover_answer');
	$(".answertext", answer).addClass('hover');


if ($(answer).data('disabled') == false) { 
	
										var blank_width = 15 + (12 * $(".answertext", answer).text().length); //todo: multiplier may need adjustment
										$("#blank", $.plopquiz.quiz_content)
											.html($(".answertext", answer)
											.text().replace(/\ /g, "&nbsp;"))
											.css("cssText", "width: " + blank_width + "px !important;");        
		                                  } 
		                                  
}


function offAnswerHover(answer) {

// replace blank space
$("#blank").text($.plopquiz.textHolder)
	.css("cssText", "width: 105px !important;");  
	 $(answer).removeClass('hover_answer');
	 $(".answertext", answer).removeClass('hover');
}
