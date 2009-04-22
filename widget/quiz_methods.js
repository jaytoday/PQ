

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
	if ($.plopquiz.settings.started == true) return false;
	$.plopquiz.settings.started = true;
// hide flash elements and dialogs	
$('object').hide().addClass('hidden'); 
$("div.ui-dialog-content").bind("dialogclose", function(){ $('.main').find('object').show(); });

	// if quiz is loaded from widget, show loading icon on widget. otherwise, immediately show overlay
	 $.event.trigger("displayQuiz"); $('#quiz_inner').hide();  $('#quiz_init').show();
	 /*
	if(!$.plopquiz.settings.autoStart) $.plopquiz.widget_wrapper.find('button').hide().end().find('.widget_load').show();
	else { $.event.trigger("displayQuiz");  $('#quiz_inner').hide();  $('#quiz_init').show();  }
	*/

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
	$('object.hidden').removeClass('hidden').show(); 
	$('#widget_wrapper').fadeIn().find('button').css('display', 'inline').end().find('.widget_load').hide();
	// wipe quiz session. TODO: this should handle skipping instructions; 
	$.plopquiz.currentItem = 0;
	$.plopquiz.settings.paused = false;
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


	 

$.plopquiz.timer_wrapper.show();	
$.plopquiz.timer.animate({opacity: 1.0}, 2000, function() //temporarily pause the timer 
{
				
$.plopquiz.settings.timer_width = $('#timer_bar', $.plopquiz.timer_wrapper).width(); // to calculate score

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
		$.plopquiz.quiz_inner_content.addClass('disabled').animate({opacity:0},0); 

	$.plopquiz.quiz_loader.show().animate({opacity: .5 }, { duration:100, complete:function(){ 


	// hardcoded versus server provided
	$.plopquiz.quizItem.url = $.plopquiz.quizItem.url ? $.plopquiz.quizItem.url : "/quiz_item/?token=" + $.plopquiz.settings.sessionToken;


	// load next item from the server
			$.ajax({
			url: $.plopquiz.settings.serverUrl + $.plopquiz.quizItem.url,
			dataType: "jsonp",
			cache: false,
			success: function(html,s){ quizItemLoad($.plopquiz.quizItem, html, s)}, // code in quiz_item_load.js
			error: function(xhr,s)
			{
					//console.log("Ajax error: ", xhr,s);
			}
			});

			}});

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
});


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



/*
 * This is called when an answer is submitted,
 * even if not during the actual quiz session
 */ 
 
$.plopquiz.fetchNextItem = function()
{

switch($.plopquiz.settings.next_item)
{


case "begin_quiz":

	return { url: '/intro/?page=begin_quiz', item_type:'begin_quiz', answers: [ 'Begin Quiz' ], noSkip: true }; break;
	

case "intro":

return  { url: '/intro/?page=intro&subject={{ proficiencies }}', item_type:'intro', answers: ['Take This Quiz'], noSkip: true, vendor: "PlopQuiz"}; break;
	

case "instructions":

return  {url: '/intro/?page=instructions', item_type:'instructions', answers: [ 'dog ate', 'web made' ], noSkip: true}; break;


case "instructions2":

return  {url: '/intro/?page=instructions2', item_type:'instructions2', answers: [ 'oil', 'battery' ], timed: "instructions2", timeout: 'reset'}; break;

case "quiz":

	return {
			"url": "/quiz_item/?token=" + $.plopquiz.settings.sessionToken,
			"item_type": "quiz_item",
			"answers": $.plopquiz.proficiencies.answers,
			"timed": true
	}; break;
	
}

};










function onAnswerHover(answer) // when answer is hovered
{
	
// skip doesn't have hover
if ($(answer).attr("id") == "skip")
	return;

	// hover event on span
	$(answer).addClass('hover_answer');
	$(".answertext", answer).addClass('hover');


if ($(answer).data('disabled') == false) { 
	
										var blank_width = 22 + (13 * $(".answertext", answer).text().length); //todo: multiplier may need adjustment
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




$.plopquiz.adjustItemSize = function(adjustment) {
$.pq_wrapper.sc = $.pq_wrapper.find('div.quiz_scroll_container');
$.pq_wrapper.qfc = $.pq_wrapper.find('div.quiz_frame_content');
$.pq_wrapper.tw = $.pq_wrapper.find('div.timer_wrapper');
$.pq_wrapper.qia = $.pq_wrapper.find('div.quiz_item_answers');
$.pq_wrapper.qc = $.pq_wrapper.find('div#quiz_content');


$.pq_wrapper.sc.height( $.pq_wrapper.sc.height() + adjustment);

$.pq_wrapper.qfc.height( $.pq_wrapper.qfc.height() + adjustment);

$.pq_wrapper.tw.css({'margin-top': $.pq_wrapper.tw.css('margin-top') + adjustment }); 

$.pq_wrapper.qia.css({'margin-top': $.pq_wrapper.qia.css('margin-top') + adjustment }); 

$.pq_wrapper.qc.height( $.pq_wrapper.qc.height() + adjustment); // check to make sure it's smaller than window.height ?


};


$.plopquiz.resetItemSize = function() {
	
$.pq_wrapper.quiz_el = [$.pq_wrapper.sc, $.pq_wrapper.qfc, $.pq_wrapper.tw, $.pq_wrapper.qia, $.pq_wrapper.qc];
$.each($.pq_wrapper.quiz_el, function(i, obj){ 
$(obj).attr('style', '');
});

};





} // end of Quiz Methods


