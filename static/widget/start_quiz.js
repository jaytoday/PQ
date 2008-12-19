

function startQuiz(html, status){
	// add to body to overlay is in front
$("body").append(html);

// resize overlay to document not window
$("#quiz_overlay").css("height", $(document).height());

// stating and stoping quiz
$("#quiz_wrap")
.bind("quizstarting", function()
{
	$(this).show();
})
.bind("quizclosing", function()
{
	$(this).hide();
	$('.widget_w').fadeIn();

	// reset to start of quiz, later this should handle skipping instructions;
	$.plopquiz.currentItem = 0;
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
			// stop to prevent ghost run outs
			$.plopquiz.timer.stop();
			
			// resize
			$.plopquiz.timer
					.css("width", "100%");
					
					$.plopquiz.settings.timer_width = $('.timer_bar').width(); // to calculate score
			  
			 

$.plopquiz.timer.animate({opacity: 1.0}, 2000, function()
{
$.plopquiz.answers.removeClass('disabled').data("disabled", false);

													// start running the timer down
			$.plopquiz.timer.animate(
			{
					width: 0
			},
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
	$.plopquiz.timer.stop();
})
.bind('submitingAnswer', function()
{
	$.plopquiz.timer.stop();
});

// totally useless?
//var textHolder = $('#blank').text();
var textHolder = '     ';

$('#quiz_answers .answer', $.pq_wrapper).hover(function()
{
// skip doesn't have hover
if ($(this).attr("id") == "skip")
	return;
	
	// hover event on span
	$(".answertext", this).addClass('hover');

var blank_width = 15 + (10 * $(".answertext", this).text().length); //todo: multiplier may need adjustment

$("#blank", $.plopquiz.quiz_content)
	.html($(".answertext", this)
	.text().replace(/\ /g, "&nbsp;"))
	.css("cssText", "width: " + blank_width + "px !important;");                                        
},
function()
{

// replace blank space
$("#blank").text(textHolder)
//.css({"padding": "0px 34px"});
	.css("width", "100px");
	
	 $(".answertext", this).removeClass('hover');
})
.click(function(e)
{

// data("disabled") prevents double submissions
if ($(this).hasClass('disabled')){ return false; }
if($(this).data("disabled") != true){
	$.plopquiz.submitAnswer($(this).find('div.answertext').text().replace(/\n/g,"")); 

}
// disable all the answers
$.event.trigger("disableAnswers");
})
.bind("disableAnswers", function()
{
// reset in loadItem
if($.plopquiz.quizItem.item_type == "quiz_item" || $.plopquiz.quizItem.item_type == "begin_quiz")
   $.plopquiz.answers.addClass('disabled').data("disabled", true);
});

$("#quiz_content", $.pq_wrapper)
// when the item is loaded, opac fade in, then trigger startTimer
.bind("quizItemLoaded", function(e, quizItem)
{
 
	$('#quiz_content').animate(
	{
			opacity: 1
	},
	{
			duration: 1000,
			complete: function()
			{
			$.event.trigger("startTimer", [ quizItem ]);
					
			}
	});
	

});

//  is this deprecated?
if($.plopquiz.settings.autoStart)
$.plopquiz.start();




} // end of startQuiz

