
function quizItemLoad(quizItem, html, s)
 {
                 	

// set the quiz content -- it can be seen
$.plopquiz.quiz_content.html(html);
// hide the answers for now
$('.answer', $.plopquiz.answer_container).hide();

$.plopquiz.quiz_loader.animate({opacity: 0}, {  duration: 0, complete: function()
{ $.plopquiz.quiz_inner_content.animate({opacity:1},{duration:200}).removeClass('disabled'); } 
}).hide();


// this supports any number of answers.
// Specify custom CSS settings, and delegate answer elements.
$.plopquiz.quiz_content.attr('class', quizItem.item_type + '_content');
$.plopquiz.answer_container.attr('class', quizItem.item_type + '_answers');
$('#quiz_inner', $.pq_wrapper ).attr('class', quizItem.item_type + '_quiz_inner');
$('.quiz_selection', $.plopquiz.quiz_content).attr('id', quizItem.item_type + '_quiz_selection');
		
for ( var i in quizItem.answers )
{

		if (quizItem.item_type == 'intro' || quizItem.item_type == 'begin_quiz' || quizItem.item_type == 'quiz_complete'){  
		var this_answer = $('#confirm', $.plopquiz.answer_container);
		}else{ 
		var this_answer = $('.answer:eq(' + i + ')', $.plopquiz.answer_container); 
		}

		this_answer
		.show()
		// reenable the button, clickity click
		.data("disabled", false)
		.find(".answertext")
		.html(quizItem.answers[i]);
		


} 

// not all items are timed (instructions)
if(quizItem.timed)
$.plopquiz.timer_wrapper.show();
else
$.plopquiz.timer_wrapper.hide();

// not all items need skipping

if(!quizItem.noSkip)
$("#skip", $.plopquiz.answer_container).show();
else
$("#skip", $.plopquiz.answer_container).hide();



/*
 * 
 * 
* Setup special cases for quiz frames
* 
* 
*/



if(quizItem.item_type == "intro")
{
	
	
$('#quiz_answers #confirm', $.plopquiz.answer_container).attr('class', 'answer intro_quiz').find('span.continue_button').text('Practice Quiz');
$('button span#intro_button', $.plopquiz.answer_container).show(); // todo: this is coming late 
$('.intro_frame_content #subject_container_1').show().addClass('selected'); // show first subject

// setup thumbnails
$('div.subject_thumb_container > div', $.plopquiz.quiz_content).each(function(n){
	
	// remove default image if there are custom images (if we will never have subjects without pictures, this isn't necessary)
	if ($(this).find('li').length > 1) { $('#subject_' + $(this).find('li:first').attr('id'), $.plopquiz.quiz_content).find('li:first').remove(); $(this).find('li:first').remove();   }//console.log($('#subject_' + $(this).attr('id'), $.plopquiz.quiz_content) );  }
	 
$('#subject_thumb_' + n, $.plopquiz.quiz_content).s3Slider({ timeOut: $.plopquiz.settings.sliderDuration });  // todo: slight offset
});  

// bind thumbnail clicks
$('div.subject_thumb_container li', $.plopquiz.quiz_content).click(function(){ //TODO: Slider/Coverflow (low priority)
$('div.subject_thumb_container li', $.plopquiz.quiz_content).removeClass('selected_thumb'); $(this).addClass('selected_thumb');
$('.intro_frame_content .subject_container', $.plopquiz.quiz_content).hide('fast');
$('.intro_frame_content #subject_container_' + $(this).attr('id'), $.plopquiz.quiz_content).show('fast');

$('#subject_' + $(this).attr('id'), $.plopquiz.quiz_content).s3Slider({ timeOut: $.plopquiz.settings.sliderDuration }); // initiate a slider for the subject being shown.


});


$('#subject_1 li:first', $.plopquiz.quiz_content).show();

$('#subject_1', $.plopquiz.quiz_content).s3Slider({ timeOut: $.plopquiz.settings.sliderDuration });  // might not be working properly



$('button.summary',$.plopquiz.quiz_content).addClass('clicked'); // summaries are open by default
$('button',$.plopquiz.quiz_content).focus(function(){$(this).blur();}).click(function(){
var this_subject = $('div#subject_container_' + $(this).attr('id'), $.plopquiz.quiz_content)
$('div.subject_panel', this_subject).hide();
$('div#' + $(this).attr('class') + '_' + $(this).attr('id'), this_subject).show();

$(this).parent().find('button').removeClass('clicked'); $(this).addClass('clicked'); // change styles

});


//temporary
$('button.take_test', $.plopquiz.answer_container).show();
$('div.go_to_site', $.plopquiz.answer_container).show();


}






if(quizItem.item_type == "instructions")
{
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
}






if(quizItem.item_type == "instructions2")
{
	
$('#skip', $.plopquiz.answer_container).hide();

$("#skip_tutorial", $.plopquiz.quiz_content).click(function()
{
$.plopquiz.currentItem = 3;
$.plopquiz.loadItem();
});
}





if(quizItem.item_type == "begin_quiz")
{
		/* TEMPORARILY we are just bypassing this frame. Eventually, we want to refactor the functionality of this frame into the intro frame */

var p = {};
$('#confirm', $.plopquiz.answer_container).removeClass('intro_quiz').addClass('begin_quiz').find('span.continue_button').text('Begin Quiz');                    
// this is a bit hacked together, later the proficiencies will be loaded from the server
for(var i in $.plopquiz.proficiencies)
$("#proficiency_choices")
.append('<input type="checkbox" value="' + $.plopquiz.proficiencies[i] + '" checked /><span class="proficiency">' + $.plopquiz.proficiencies[i] + '</span><br />');
}






if(quizItem.item_type == "quiz_item")
{
// reset the blank space
$('#blank', $.plopquiz.quiz_content).empty();
// hide the question until everything is loaded
$.plopquiz.quiz_content.css('opacity', 0);
}






if(quizItem.item_type == "quiz_complete")
{
//update text for Button
$('#quiz_answers #confirm').removeClass('begin_quiz').addClass('quiz_complete').find('span.continue_button').text('See Results').show();
// signup binding
$('div.form_proceed').click(function(){

var current_id  = $(this).attr('id');
var next_id  = parseInt(current_id) + 1;

// last page of signup?
if ($('form.signup').find('ul#' + next_id).length == 0)
{
var args = {};
// form elements to be submited
var aargs = Array("name", " email", " occupation", " work_status", " webpage", " loc")

// this can be refined
for(var i in aargs)
args["arg" + i] = "\"" + $("#" + aargs[i]).val() + "\"";

// submit the registration, all RPC calls should be moved to a single location
$.ajax(
{
url: $.plopquiz.settings.serverUrl + "/quiztaker/rpc",
dataType: "jsonp",
data: $.extend(
{
action: "Register",
}, args),
success: function(obj)
{
console.log(obj);
}
});

return;
}

// are there every more then one page?
$('form.signup').find('ul#' + current_id).fadeOut(200, function()
{
$('form.signup').find('ul#' + next_id).fadeIn(200);
});

$(this).attr('id', next_id);
});      
}                

// start the quiz now
$.event.trigger('quizstarting');

// short delay to ensure everything is loaded
setTimeout(function()
{
$.event.trigger('quizItemLoaded', [ quizItem ]);
},100);








                                
                        } //end of quizitemLoad
                      
   
