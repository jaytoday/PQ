
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
                        {url: '/intro/?page=intro&subject={{ proficiencies }}', item_type:'intro', answers: ['Take This Quiz'], noSkip: true, vendor: "PlopQuiz"},
                        {url: '/intro/?page=instructions', item_type:'instructions', answers: [ 'dog ate', 'web made' ], noSkip: true},
                        {url: '/intro/?page=instructions2', item_type:'instructions2', answers: [ 'oil', 'battery' ], timed: "instructions2", timeout: 'reset'},
                        { url: '/intro/?page=begin_quiz', item_type:'begin_quiz', answers: [ 'Begin Quiz' ], noSkip: true }
                ],
                quizitemList: Array(),
                currentItem: 0, // use to skip intros
                settings:
                {
                        serverUrl: "{{ http_host }}",
                        autoStart: {{ auto_start }},
                        started: false,
                        initDone: false,
                        startTime: (new Date()),
                        sliderDuration: 5300, // used for subject preview image sliders
                        timeoutDuration: 240000, // time to answer question
                        sessionToken: "", // provided by server to load and answer questions
                        next_item: 'intro', 
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
                quizItem: Object()
                
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
		// error: console.log('quiz frame error'), silent failure - should this show error? 
		success: function(html,status) { loadQuizMethods(html, status); } // code in start_quiz.js

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


$.plopquiz.settings.initDone = true;

        }; 



$.plopquiz.load_widget = function()
{
	
// the script just loaded so stop the timeout
clearTimeout($.plopquiz.timewatch);
$.plopquiz.widget_html = "{% spaceless %}{{ widget_html }}{% endspaceless %}";

                // TODO: visible error if no <body> in document
                $("script", $("body")).each(function() {
                if(this.src.indexOf('{{ http_host }}/js/quiz') > -1) 
                 $(this).after('<div id="pqwidget"><a href="{{ http_host }}/quiz/" class="widget_footer">Take This Quiz at PlopQuiz.Com</a></div>'); } );
                      
                        
// add widget HTML
$.plopquiz.widget_wrapper = $("#pqwidget");

$.plopquiz.widget_wrapper.html($.plopquiz.widget_html).hide().fadeIn().click(function(){ $.plopquiz.load_custom_selectors();  $.plopquiz.start(); });

$('button',$.plopquiz.widget_wrapper).focus(function(){$(this).blur();});

// remove default image if there are custom images (if we will never have subjects without pictures, this isn't necessary)
	if ($.plopquiz.widget_wrapper.find('li').length > 1) $.plopquiz.widget_wrapper.find('li:first').remove();   
	 
	 
$('#pqwidget #subject_1').s3Slider({ timeOut: 8300  }); 


};


$.plopquiz.load_custom_selectors = function(){
					// shortcuts for important elements
					$.pq_wrapper = $("#pq_wrapper");  // the entire interface, including bg and overlay.
					$.plopquiz.quiz_outer = $('div#quiz_outer', $.pq_wrapper);
					$.plopquiz.quiz_inner_content = $('#quiz_inner > div'); // both content and answers
					$.plopquiz.quiz_content = $('#quiz_inner  #quiz_content'); // content loaded from server
					$.plopquiz.quiz_loader = $('#quiz_inner #quiz_loading');
					$.plopquiz.timer_wrapper = $('#quiz_inner #quiz_timer');
					$.plopquiz.timer = $('#timer_bar', $.plopquiz.timer_wrapper);
					$.plopquiz.answer_container = $("#quiz_inner #quiz_answers"); // just answers and buttons
					$.plopquiz.answers = $.plopquiz.answer_container.find('div');
					$.plopquiz.answer_text = $.plopquiz.answers.find('div.answertext:not(#skiptext)');
					$.plopquiz.answer_load_icons = $.plopquiz.answer_container.find("div.mini_loader");
					$.plopquiz.textHolder = '     ';
	};

 $.plopquiz.start = function(){
 	                                        
                // if the click handler is setup before the frame loads, wait for it
					if($.pq_wrapper.length > 0) 
					// start the quiz now 
					$.event.trigger('quizstarting');

                else
                        return setTimeout($.plopquiz.start, 100);
                        
                        				
                

                        
				//lightbox is draggable
				$('#quiz_outer').draggable({ 
				zIndex: 	1000, 
				//opacity: 0.8,
				addClasses: false,
				ghosting: false,
				containment: 'document', 
				cancel: '.no_drag', // Youtube still doesn't work on Safari. quiz_scroll_container also.
			 distance: 90, // this solves scrollbar problem, but it requires 90 pixel drag before draggable() activates.
				cursor: 'pointer'
				 }); 

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

$.plopquiz.quizItem = ((quizItem && quizItem.answers) ? quizItem : $.plopquiz.fetchNextItem());

console.log($.plopquiz.quizItem);
if(!$.plopquiz.quizItem)return; 

// heeaayy, we're loading a quiz item
$.event.trigger('loadingQuizItem');

};







$.plopquiz.fatalError = function(msg) { 
	//TODO: collect error stats
	window.location = '{{ http_host }}/error/quiz'
	console.log('fatal error: ', msg) 
} 
 

$(function()
{
$.plopquiz.init(); //the init fn is started when the document is ready.
});




}; // end of session setup

function pqLoad()
{

        {% include "../static/scripts/utils/s3slider.js" %} // this is causing an error when run from the site.
        
        var load_core = true;
    if (jQuery.ui) { if (jQuery.ui.draggable) { load_core = false; } }
          if (load_core) { {% include "../static/scripts/jquery/ui.core.js" %}  {% include "../static/scripts/jquery/ui.draggable.js" %}   }
                        

        // force ready jQuery because page load is (likely?) done
        // jQuery.isReady = true; -- this was breaking some javascript
        // load plopquiz (modified) from within closure. if it's already loaded, open quiz frame.
       if (!$.plopquiz) session_setup(jQuery);
       else $.plopquiz.start(); 
}



var load_jquery = true;
// do we have jQuery - can we overwrite older versions? 
if(window.jQuery){
	if (jQuery.fn.jquery == '{{ jquery_version }}') load_jquery = false;
             }
             
if (load_jquery == true)
    { 

          {# Dynamically insert the jQuery version  {% include "../static/scripts/jquery/jquery-{{ jquery_version }}.js" %} #}


    	{% comment %}
    	
    	This uses jQuery, but otherwise we have to include jQuery redundantly - if not compile it - for quizzes taken at PlopQuiz.com) 
    	
    	$.getScript("http://ajax.googleapis.com/ajax/libs/jquery/{{ jquery_version }}/jquery.min.js", 
    	function(){
					pqLoad();
				});
				
		{% endcomment %}
	  
	}
	
pqLoad();  



/*
 * Longer functions are included from other .js files in /static/widget
 */

{% include "quiz_item_load.js" %}     //quizItemLoad      -- loading each item type

{% include "quiz_item_submit.js" %}     //plopquiz.submitAnswer    -- submitting each item type  

{% include "quiz_methods.js" %}  //startQuiz.    




{% endspaceless %}
