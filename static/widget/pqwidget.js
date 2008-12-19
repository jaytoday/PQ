//      PQ Quiz Client Library 





var iso = function($)
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
                        {url: '/intro/?page=instructions2', item_type:'instructions2', answers: [ 'compilers', 'interpreters' ], timed: "instructions2", timeout: 'reset'},
      /* TODO: We're merging this with the first frame */ {url: '/intro/?page=begin_quiz', item_type:'begin_quiz', answers: [ 'Begin Quiz' ], noSkip: true}
                ],
                quizitemList: Array(),
                currentItem: 0, // use to skip intros
                settings:
                {
                        serverUrl: "{{ http_host }}",
                        autoStart: false, // debugging only?
                        initDone: false,
                        startTime: (new Date()),
                        sliderDuration: 5300,
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
// preload the quiz frame for quick start
$.ajax({
		url: $.plopquiz.settings.serverUrl + '/quiz_frame',
		dataType: "jsonp",
		// error: console.log('quiz frame error'), TODO: error handling
		success: function(html,status) { startQuiz(html, status) } // code in start_quiz.js

});

var jsonpcallback = false;

// this is a jQuery JSONP timeout hack
for(var i in window)
{
// if it starts with jsonp, keep going, we want the last one
if(i.substring(0,5) == "jsonp")
jsonpcallback = i;
}

// this should be the last (if any) jsonp123123 callback
if(jsonpcallback)

// if the callback still exists after 6 seconds, time it out
var timewatch = setTimeout(function()
{
// still there?
if(window[jsonpcallback] != "undefined")

$("#pqwidget").append(
	$("<a href=\"http://www.plopquiz.com\">Visit PlopQuiz</a>").hide().fadeIn()
);


}, 6000);

// second part of the hack, find the script with the same callback in the src and setup onload
$("script").each(function()
{
/*
* This is the part where quiz clients are embedded on the PQ site are failing.
* 
*  This if statement fails from PQ site:  if(this.src.indexOf(jsonpcallback) > -1)  */

if(this.src.indexOf(jsonpcallback) > -1)

this.onload = function()
{
// the script just loaded so stop the timeout
clearTimeout(timewatch);

var widget_html = "{% spaceless %}{{ widget_html }}{% endspaceless %}";

// yay the widget script loaded, setup the start handler
$("#pqwidget").append(
	$(widget_html).hide().fadeIn().click($.plopquiz.start)
);

$('#pqwidget #subject_1').s3Slider({ timeOut: 8300  });  
}


});
        }; 

        $.plopquiz.start = function()
        {
				 // Setup commonly used selectors
				$.pq_wrapper = $("#quiz_wrap");  // the entire interface, including bg and overlay.
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
        }; 






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
 

$.plopquiz.submitAnswer = function(answer)
{
$.event.trigger("submittingAnswer");
// check the answer for special cases
// this will handle the non-skiping timeout on instructions2,
// the proficiencies, the score, and any other special boxes
switch($.plopquiz.quizItem.item_type)
{

case "intro":

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
			$('#example_1,#example_3', $.plopquiz.quiz_content).hide('slow');
			$('#example_2', $.plopquiz.quiz_content).show('slow');
			$('a#skip', $.plopquiz.answer_container).show();
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
	// clear out proficiencies in case its a restart
	$.plopquiz.settings.proficiencies = Array();

	$('#proficiency_choices input:checked', $.plopquiz.quiz_content).each(function() { $.plopquiz.settings.proficiencies.push($(this).val()); });
	$.plopquiz.timer.css('width', '100%'); 

	// this start the server session and retrieves the first questions
	// this can be refined
	// all RPC calls should be moved to one location
	$.ajax(
	{
			url: $.plopquiz.settings.serverUrl + "/quiztaker/rpc",
			dataType: "jsonp",
			data:
			{
					action: "start_quiz",
					arg0: "[\"" + $.plopquiz.settings.proficiencies.join("\",\"") + "\"]"
			},
			success: function(rpc)
			{
					// the session token to submit answers and load quiz content
					if(rpc.token)
							$.plopquiz.settings.sessionToken = rpc.token;

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
			success: function(obj)
			{
					var q = obj["quiz_item"];

					if(q === false)
					{
							return $.plopquiz.loadItem({url: "/intro/?page=quiz_complete", item_type:"quiz_complete", noSkip: true, answers: [ "Submit" ]});
					}

					$.plopquiz.loadItem($.extend({timed:true,"item_type":"quiz_item"}, q));
			}
	});

   
break;

case "quiz_complete":
 $.event.trigger('quizclosing');
  window.location = "{{http_host}}/redirect/from_quiz/" + $.plopquiz.settings.sessionToken;
  
break;

default:
	$.plopquiz.loadItem();
break;
};
};







$.plopquiz.fetchNextItem = function()
{
if($.plopquiz.settings.instructions.completed == false)
		return $.plopquiz.introItems[$.plopquiz.currentItem++]; 

return {
		"url": "/quiz_item/?token=" + $.plopquiz.settings.sessionToken,
		"item_type": "quiz_item",
		"answers": $.plopquiz.proficiencies.answers,
		"timed": true
};
}

 
 

$(function()
{
$.plopquiz.init(); //the init fn is started when the document is ready.
});
};



// Some of these utilities may not be necessary now that we're compiling
// the JS from Django 

var pqjs = document.getElementsByTagName("script");
pqjs = pqjs[pqjs.length - 1];

var widgetSource = pqjs.src.substring(0, pqjs.src.lastIndexOf("/") + 1);

// We only still need this function if there's a reason we can use the include tag
// script should be plain filename ( jqwidget.js not /loc/script.js )
function addScript(script, id)
{
        var s = document.createElement("script");
        s.src = /*widgetSource + */script;
        s.rel = "javascript";
        s.type = "text/javascript";

        var timeout = function()
        {
                console.log('failed to load ' + s.src);
        }

        // six second timeout before throwing error
        setTimeout(function()
        {
                timeout();
        }, 6000);

        s.onload = function()
        {
                timeout = function() {};
        }

        pqjs.parentNode.appendChild(s);
}

function addStyle(src)
{
        var s = document.createElement("link");
        s.href = /*widgetSource + */src;
        s.rel = "stylesheet";
        s.type = "text/css";
        pqjs.parentNode.appendChild(s);
}

function waitForJQ()
{
        // loaded yet? Yes? good continue. No? keep waiting
        if(window.jQuery)
                pqLoad();
        else
                setTimeout(waitForJQ, 60);
}



function pqLoad()
{

        {% include "../scripts/utils/s3slider.js" %} // this is causing an error when run from the site.
        
        // force ready jQuery because page load is (likely?) done
        jQuery.isReady = true;
        // load plopquiz (modified) from within closure
        iso(jQuery); // wtf does iso mean again?
}


addStyle("{{ http_host }}/css/quiz"); // can we use the include tag here?

// do we have jQuery on the page already?
if(window.jQuery)
{
        // yup,
        pqLoad();
}
else
{
        // no? load it from the same location as the widget
        //addScript("{{ http_host }}/static/scripts/jquery/jquery-1.2.6.min.js");
        
        // Load external javascript files
        {% include "../scripts/jquery/jquery.js" %}       // Since this is being done on the server-side, it's much faster than getScript().
        
        // This could also make it easier for us to manage the quiztaking code, since there's no penalty to seperating the code between files. 
        
        

        // check in 6ms
        setTimeout(waitForJQ, 60);
}








/*
 * Longer functions are included from other .js files in /static/widget
 */

{% include "quiz_item_load.js" %}     //quizItemLoad              


{% include "start_quiz.js" %}  //startQuiz     
