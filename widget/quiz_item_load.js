/* Settings */
	  var DEFAULT_HEIGHT = 200; // should/can this be looked up? 

	  
function quizItemLoad(quizItem, html, s)
{
	// Remove the existing content
	$.plopquiz.quiz_content.html('');
	
	// hide the answers  and timer for now
	$('.answer', $.plopquiz.answer_container).hide();
	$.plopquiz.timer_wrapper.hide();

	// this occasionally results in things fading in twice...the solution is to fade in the element after a pause.
	$.plopquiz.quiz_loader.attr('class', quizItem.item_type + '_load').animate({opacity: 0}, {  duration: 0, complete: function()
		{ $.plopquiz.quiz_inner_content.animate({opacity:1},{duration:200}).removeClass('disabled'); } 
	}).hide();

	// apply new class for quiz content for item_type - specified in pqwidget.css. Called after the resize
	function setNewStyles() {
		// Display the new content
		$.plopquiz.quiz_content.html(html);
		
		$.plopquiz.quiz_content.attr('class', quizItem.item_type + '_content'); 
		$.plopquiz.answer_container.attr('class', quizItem.item_type + '_answers');
		$('#quiz_inner', $.pq_wrapper ).attr('class', quizItem.item_type + '_quiz_inner');
		$('.quiz_selection', $.plopquiz.quiz_content).attr('id', quizItem.item_type + '_quiz_selection');
		$.plopquiz.timer_wrapper.attr('id', quizItem.item_type);
		
		afterResize();
	}

	currentWidth = $.plopquiz.quiz_content.css('width');
	currentHeight = $.plopquiz.quiz_content.css('height');

	if(currentHeight == 'auto' || currentWidth == 'auto') {
		setNewStyles();

		var margin_left = ( parseInt($.plopquiz.quiz_content.css('width')) / 2 ); 
		var margin_top = ( parseInt($.plopquiz.quiz_content.css('height')) / 2 );
		$.plopquiz.quiz_outer.css({'margin-left': -margin_left, 'margin-top': -margin_top }); 
	}
	else {
		// Add a hidden element with the new style so we can get the new dimensions
		// Not sure why this is needed...
		newStyle = quizItem.item_type + '_content';
		tempElem = jQuery("<div style='display:none' class='" + newStyle + "'/>");
		$.plopquiz.quiz_content.append(tempElem);
		newWidth = tempElem.css('width');
		newHeight = tempElem.css('height');
		tempElem.remove();
		
		var animDuration = 'normal';
		
		// Resize animation
		var margin_left = ( parseInt(newWidth) / 2 ) + 15; 
		var margin_top = ( parseInt(newHeight) / 2 ) + 15;
		$.plopquiz.quiz_outer.animate({'marginLeft': -margin_left, 'marginTop': -margin_top }, {duration: animDuration, queue:false});  
		$.plopquiz.quiz_content.animate({width: newWidth, height: newHeight}, {duration: animDuration, queue:false, complete: setNewStyles});
				// set new quiz frame position -- this should come after quiz item redraw
	}
	

	// Do everything else once we've completed the resize
	function afterResize() {
		for ( var i in quizItem.answers )
		{
				if (quizItem.item_type == 'intro' || quizItem.item_type == 'begin_quiz' || quizItem.item_type == 'quiz_complete'){  
				var this_answer = $('#confirm', $.plopquiz.answer_container);
				}else{ 
				var this_answer = $('.answer:eq(' + i + ')', $.plopquiz.answer_container); 
				}

				this_answer
				.show()
				.data("disabled", false)
				.find(".answertext")
				.html(quizItem.answers[i]);
		} 

		// not all items are timed (instructions)
		if(quizItem.timed)
		$.plopquiz.timer_wrapper.show();
		

		// not all items need skipping
		if(!quizItem.noSkip)
		$("#skip", $.plopquiz.answer_container).show();
		else
		$("#skip", $.plopquiz.answer_container).hide();


		$.plopquiz.answers.removeClass('disabled').data("disabled", false);


		/*
		 * 
		 * 
		* Setup special cases for quiz frames
		* 
		* 
		*/
switch(quizItem.item_type){
case "begin_quiz":

$('#quiz_init').hide();   $('#quiz_inner').show(); 
		$('#confirm', $.plopquiz.answer_container)
		  .removeClass('intro_quiz').addClass('begin_quiz').find('span.continue_button').removeClass('intro_button').addClass('begin_button').text('Start the Quiz').end()
		  .animate({ opacity:0},{duration: 0, 
				                complete: function(){  var $button = $('#confirm', $.plopquiz.answer_container); $button.data('disabled', true);  $("div#begin_quiz_quiz_selection", $.plopquiz.quiz_content).animate({height:170},{ duration: 1000, 
				                complete: function(){  $("#click_below", $.plopquiz.quiz_content).animate({opacity:1},{ duration: 1000,     
				                complete: function(){  $button.animate({opacity:1},{duration: 1000 });  $button.data('disabled', false);  
				                 }});   
				                 }}); 
								 }});        

		
		$.plopquiz.settings.instructions.completed = false; break;
		

		
		
		case "intro": 

		{% include "quiz_intro.js" %} 
		
		break;





case "instructions":

		//special handler for instructions 1 hovering
		var i1mouseOverCount = 0;
		var i1mouseOver = function()
		{
		// unbind is to prevent incrementing on the same button
		$(this).unbind('mouseover',i1mouseOver);
		// both buttons have been hovered? good done
		if(++i1mouseOverCount >= 2)
		{
		$('#example_1,#example_2').toggle();
		$.plopquiz.settings.instructions.i1complete = true;
		i1mouseOverCount = null;
		}
		};


		$("#skip_tutorial", $.plopquiz.quiz_content).click(function()
		{
		$.plopquiz.currentItem = 3;
		$.plopquiz.loadItem();
		});


		$(".answer", $.plopquiz.answer_container).mouseover(i1mouseOver);
		break;


case "instructions2":
	
		$('#skip', $.plopquiz.answer_container).hide();

		$("#skip_tutorial", $.plopquiz.quiz_content).click(function()
		{
		$.plopquiz.currentItem = 3;
		$.plopquiz.loadItem();
		});
		break;





case "quiz_item":

		// reset the blank space
		$('#blank', $.plopquiz.quiz_content).empty();
		// hide the question until everything is loaded
		$.plopquiz.quiz_content.css('opacity', 0);
		$.plopquiz.answer_text.animate({opacity: 0}, 0);
		$.plopquiz.answer_load_icons.animate({opacity: 1}, 300);
		$.plopquiz.answers.data('disabled', true);
		
		
		// adjust tab width
	  var tab_width = 20 + (10 * $.plopquiz.quiz_content.find('div#quiz_category').text().length);
	  $.plopquiz.quiz_content.find('div.tab').css('width', tab_width);
	  $.plopquiz.quiz_content.find('div#quiz_category').css('width', tab_width - 10);
	  
	  
		// reset item size
    $.plopquiz.resetItemSize();
    // adjust item size
	var text_height = $.plopquiz.quiz_content.find('div.quiz_frame_text').height(); 
	if (text_height < DEFAULT_HEIGHT + 10) text_height = text_height + 20;
	var adjust_height = text_height - DEFAULT_HEIGHT;
	//if ( adjust_height > -50 )
	 $.plopquiz.adjustItemSize(adjust_height); 
 
	  break;



case "quiz_complete":
		
		//update text for Button
		$('#quiz_answers #confirm').removeClass('begin_quiz').addClass('quiz_complete').find('span.continue_button').text('See Results').show();
		break;    
	} 


		// short delay to ensure everything is loaded
		setTimeout(function()
		{
		$.event.trigger('quizItemLoaded', [ quizItem ]);
		},100);
	}
                                
} //end of quizitemLoad
