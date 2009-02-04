// Quiz Intro

$('#confirm', $.plopquiz.answer_container).data('disabled', true).attr('class', 'answer intro_quiz')
     .find('span.continue_button').text('Take This Quiz').end()
    .animate({ opacity:0},{ duration: 0, 
                         complete: function(){ $(this).animate({opacity:0},{ duration: 500, 
                                                                              complete: function(){ $(this).animate({opacity:1},{duration: 1000  });  $(this).data('disabled', false); }                       
                                                                            });
                                             } 
                            });
                            
$('button span#intro_button', $.plopquiz.answer_container).show(); 
$('.intro_frame_content #subject_container_1').show().addClass('selected'); // show first subject

// setup thumbnails
$('div.subject_thumb_container > div', $.plopquiz.quiz_content).each(function(n){
	
	// remove default image if there are custom images (if we will never have subjects without pictures, this isn't necessary)
	if ($(this).find('li').length > 1) { $('#subject_' + $(this).find('li:first').attr('id'), $.plopquiz.quiz_content).find('li:first').remove(); $(this).find('li:first').remove();   }
	 
$('#subject_thumb_' + n, $.plopquiz.quiz_content).s3Slider({ timeOut: $.plopquiz.settings.sliderDuration });  // todo: slight offset
});  

// bind thumbnail clicks
$('div.subject_thumb_container li', $.plopquiz.quiz_content).click(function(){ //TODO: Slider/Coverflow (low priority)
$('div.subject_thumb_container li', $.plopquiz.quiz_content).removeClass('selected_thumb'); $(this).addClass('selected_thumb');
$('.intro_frame_content .subject_container', $.plopquiz.quiz_content).hide('fast').removeClass('selected');
$('.intro_frame_content #subject_container_' + $(this).attr('id'), $.plopquiz.quiz_content).show('fast').addClass('selected');

$('#subject_' + $(this).attr('id'), $.plopquiz.quiz_content).s3Slider({ timeOut: $.plopquiz.settings.sliderDuration }); // initiate a slider for the subject being shown.

});


$('#subject_1 li:first', $.plopquiz.quiz_content).show();

$('#subject_1', $.plopquiz.quiz_content).s3Slider({ timeOut: $.plopquiz.settings.sliderDuration });  // might not be working properly


// switch between summary and study guide
$('button.summary',$.plopquiz.quiz_content).addClass('clicked'); // summaries are open by default
$('button',$.plopquiz.quiz_content).focus(function(){$(this).blur();}).click(function(){
	if ($(this).hasClass('clicked')) return false;
		var this_subject = $('div#subject_container_' + $(this).attr('id'), $.plopquiz.quiz_content)
		$('div.subject_panel', this_subject).hide();
		$('div#' + $(this).attr('class') + '_' + $(this).attr('id'), this_subject).show();
		$(this).parent().find('button').removeClass('clicked'); $(this).addClass('clicked'); // change button styles
});

// links all open new windows
$('div.study_guide', $.plopquiz.quiz_content).find('a').attr('target', '_blank');

// in study guide, switch between links and videos
$('.study_header',$.plopquiz.quiz_content).click(function(){
	$(this).parent().find('.study_header').removeClass('selected').end()
	.find('.study_content').hide().end()
	.find('.study_' + $(this).attr('id')).show().end().end()
	.addClass('selected');
	
});

//show buttons - important in case quiz is closed and reopened
$('button.take_test', $.plopquiz.answer_container).show();
$('div#points', $.plopquiz.quiz_inner_content).show();
$('div.go_to_site', $.plopquiz.answer_container).show();


// we haven't display quiz yet if this is a widget, so do it now
if(!$.plopquiz.settings.autoStart) $.event.trigger("displayQuiz");
else { $('#quiz_init').hide();   $('#quiz_inner').show();  }





// Share Quiz 

$('button',  'div.quiz_code').click(function(){

var this_button = $(this); 
var share_popup = $(this).parent().parent().parent().find('div.share_popup');

if ( share_popup.data('last_clicked') == $(this).attr('id') ) { share_popup.animate({opacity: 0 }, {duration:100}); return false; }

	
share_popup.data('last_clicked', $(this).attr('id'));

	
		
		share_popup.animate({opacity: 0 }, {duration:100, complete:function(){  
		
		if (this_button.attr('id') == "embed") {
			$(share_popup).find('div').hide(); $('div.embed', share_popup).show();
			share_popup.animate({opacity: 1 }, {duration:100}); 
		}
		if (this_button.attr('id') == "link") {
			$(share_popup).find('div').hide(); $('div.link', share_popup).show(); 
			share_popup.animate({opacity: 1 }, {duration:100});
	    }
		
		
	} });
	
		
	}); // end click

	

	
