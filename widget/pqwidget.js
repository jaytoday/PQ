
{% spaceless %}
{% comment %} 
/*
 *       PQ Quiz Client Library 
 * 
 *  1. jQuery and jQuery ui are loaded, if not already loaded.
 *  2. Quiz session token receieved, and start_quiz runs.
 *  3. Widget HTML is loaded. (unless autostart == true, and we skip to 4.)
 *  4. On widget click, $.plopquiz.start runs and item loop begins.
 *  5. Hard-coded items come first (intro, instructions), and then quiz items.
 *  6. quiz_item_load.js contains loop for loading items (updating content and answers), 
 *     and quiz_item_submit.js contains loop for submitting items.
 * 
 */ 
 
 // TODO: error handling for ajax responses
 
{% endcomment %}


var session_setup = function($)
{
	var opts = {}, 
	imgPreloader = new Image, imgTypes = ['png', 'jpg', 'jpeg', 'gif'], 
	loadingTimer, loadingFrame = 1;

        $.plopquiz =
        {
                // intro and instruction hard coded items
                introItems:
                [
                        {url: '/intro/?page=intro&subject={{ proficiencies }}', item_type:'intro', answers: ['Take This Quiz'], noSkip: true, vendor: "Plopquiz"},
                        {url: '/intro/?page=instructions', item_type:'instructions', answers: [ 'dog ate', 'web made' ], noSkip: true},
                        {url: '/intro/?page=instructions2', item_type:'instructions2', answers: [ 'oil', 'battery' ], timed: "instructions2", timeout: 'reset'},
      /* TODO: We're merging this with the first frame */ {url: '/intro/?page=begin_quiz', item_type:'begin_quiz', answers: [ 'Begin Quiz' ], noSkip: true}
                ],
                quizitemList: Array(),
                currentItem: 0, // use to skip intros
                settings:
                {
                        serverUrl: "{{ http_host }}",
                        autoStart: {{ auto_start }},
                        initDone: false,
                        startTime: (new Date()),
                        sliderDuration: 5300, // used for subject preview image sliders
                        timeoutDuration: 24000, // time to answer question
                        sessionToken: "", // provided by server to load and answer questions
                        instructions: // track progress through instruction
                        {
                                completed: false, // all done?
                                i1complete: false, // first done?
                                i2timedOut: false // second done?
                        }
                },
                specialTimers: // special cases for timeout "quiz_item.item_type": function() {}
                {
                        "instructions2": function()
                        {
                        	$("#example_1", $.plopquiz.quiz_content).hide();
                        	$("#example_2", $.plopquiz.quiz_content).hide();
                        	$("#example_3", $.plopquiz.quiz_content).show();
                        }
                },
                quizItem: Object(),
                proficiencies: {{ proficiencies }} // proficiencies loaded from widget/handler.py 
        };

        // this function setups event handlers and ensure everything is setup properly,
        // then call $.plopquiz.start, which actually deals with CSS and loading the quiz
/*
 * 
 *     Quiz Initialization
 * 
 */        
       
        $.plopquiz.init = function()
        {
        	
//load css
$.plopquiz.loadStyles();                
                
     
      
// preload the quiz frame for quick start, ajax puts it into script element
$.ajax({
		url: $.plopquiz.settings.serverUrl + '/quiz_frame',
		dataType: "jsonp",
		// error: console.log('quiz frame error'), TODO: error handling
		success: function(html,status) { startQuiz(html, status); } // code in start_quiz.js

});

var jsonpcallback = false;

// this is a jQuery JSONP timeout hack
for(var i in window)
{
	// if it starts with jsonp, keep going, we want the last one
if(i.substring(0,5) == "jsonp")jsonpcallback = i;
}

// this should be the last (if any) jsonp123123 callback
if(jsonpcallback)
		// if the callback still exists after 6 seconds, time it out
		$.plopquiz.timewatch = setTimeout(function()
		{
		if(window[jsonpcallback]) 
		$("#pqwidget").append( $("<a href=\"http://www.plopquiz.com\">Take This Quiz At PlopQuiz.Com</a>").hide().fadeIn())
		}, 6000);


        }; 



$.plopquiz.load_widget = function()
{
	

// the script just loaded so stop the timeout
clearTimeout($.plopquiz.timewatch);

var widget_html = "{% spaceless %}{{ widget_html }}{% endspaceless %}";

// yay the widget script loaded, setup the start handler
$("#pqwidget").html(
	$(widget_html).hide().fadeIn().click($.plopquiz.start)
);

$('button',$("#pqwidget")).focus(function(){$(this).blur();})

// remove default image if there are custom images (if we will never have subjects without pictures, this isn't necessary)
	if ($("#pqwidget").find('li').length > 1) $("#pqwidget").find('li:first').remove();   
	 
	 

$('#pqwidget #subject_1').s3Slider({ timeOut: 8300  }); 

};




 $.plopquiz.start = function(){
 	
 	
				 // Setup commonly used selectors
				$.pq_wrapper = $("#pq_wrapper");  // the entire interface, including bg and overlay.
				$.plopquiz.quiz_inner_content = $('#quiz_inner > div'); // both content and answers
				$.plopquiz.quiz_content = $('#quiz_inner  #quiz_content'); // content loaded from server
				$.plopquiz.quiz_loader = $('#quiz_inner #quiz_loading');
				$.plopquiz.timer_wrapper = $('#quiz_inner #quiz_timer');
				$.plopquiz.timer = $('#timer_bar', $.plopquiz.timer_wrapper);
				$.plopquiz.answer_container = $("#quiz_inner #quiz_answers"); // just answers and buttons
				$.plopquiz.answers = $.plopquiz.answer_container.find('div');
				
                
                // if the click handler is setup before the frame loads, wait for it
                if($.pq_wrapper.length > 0)
                        $.plopquiz.loadItem();
                else
                        setTimeout($.plopquiz.start, 600);
                        
                        
				//widget is draggable -- TODO: having trouble with this, more info at http://docs.jquery.com/UI/Draggable/draggable#options
				$('#quiz_outer').draggable(); 

        }; 



// inject quiz css into the document head
$.plopquiz.loadStyles = function(){
var quizStyles = '{{ css }}';
var style = document.createElement('style');
style.rel = "stylesheet"; style.type = "text/css";
$(style).html(quizStyles);
$('head').append(style);
}



/*
 * Transition between items
 * 
*/

$.plopquiz.loadItem = function(quizItem)
{

// this could use some clean up, the transistions between hard code and real quizItem is a bit funky
var quizItem = $.plopquiz.quizItem = ((quizItem && quizItem.answers) ? quizItem : $.plopquiz.fetchNextItem());

if(!quizItem)
		return;
		
$.plopquiz.quiz_inner_content.addClass('disabled').animate({opacity:0},100); 
	
	$.plopquiz.quiz_loader.show().animate({opacity: .5 }, {duration:100, complete:function(){ 


		// hardcoded versus server provided
quizItem["url"] = quizItem.url ? quizItem.url : "/quiz_item/?token=" + $.plopquiz.settings.sessionToken;

// heeaayy, we're loading a quiz item
$.event.trigger('loadingQuizItem');


// load next item from the server
$.ajax({
		url: $.plopquiz.settings.serverUrl + quizItem.url,
		dataType: "jsonp",
		cache: false,
		success: function(html,s){ quizItemLoad(quizItem, html, s)}, // code in quiz_item_load.js
		error: function(xhr,s)
		{
				console.log("Ajax error: ", xhr,s);
		}
});

}});

};




/*
 * This is called when an answer is submitted,
 * even if not during the actual quiz session
 */ 
 
$.plopquiz.fetchNextItem = function()
{
if($.plopquiz.settings.instructions.completed == false) // still in instructions
		return $.plopquiz.introItems[$.plopquiz.currentItem++]; 

return {
		"url": "/quiz_item/?token=" + $.plopquiz.settings.sessionToken,
		"item_type": "quiz_item",
		"answers": $.plopquiz.proficiencies.answers,
		"timed": true
};
}


$.plopquiz.fatalError = function(msg) { 
	//TODO: collect error stats
	window.location = '{{ http_host }}/error/quiz'
	console.log('fatal error: ', msg) 
} 
 

$(function()
{
$.plopquiz.init(); //the init fn is started when the document is ready.
});
};



function pqLoad()
{

        {% include "../static/scripts/utils/s3slider.js" %} // this is causing an error when run from the site.
        
        if (!jQuery.ui) { {% include "../static/scripts/jquery/jquery.ui.js" %}  /* this would have to be an addscript to actually work... */ }
                        

        // force ready jQuery because page load is (likely?) done
        // jQuery.isReady = true; -- this was breaking some javascript
        // load plopquiz (modified) from within closure
        session_setup(jQuery); 
}



// do we have jQuery on the page already?
if(window.jQuery)
{ pqLoad(); }
else
{ {% include "../static/scripts/jquery/jquery.js" %}    pqLoad(); }



/*
 * Longer functions are included from other .js files in /static/widget
 */

{% include "quiz_item_load.js" %}     //quizItemLoad      -- loading each item type

{% include "quiz_item_submit.js" %}     //plopquiz.submitAnswer    -- submitting each item type  

{% include "start_quiz.js" %}  //startQuiz.    




{% endspaceless %}
