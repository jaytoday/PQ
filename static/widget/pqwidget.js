/*
* Quizbox Library 

*/



/*
 * 
 * This code is badly in need of a tune-up. It needs more efficient use of:
 * 
 *  selector context,
 * selectors and events in loops, 
 * ID selectors instead of CLASS selectors, wherever possible
 * chaining,
 * no DOM manipulation just for data
 * everything wrapped in a single element for DOM insertion
 * for SEO-important sections, add in unimportant markup in JS
 *
 */ 




// this is a modified version of the quiz from the main site
// at some point they should both be able to run from the exact script
// the widget version will include the widget bootstrapper
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
                        /* needed? */ user_session: "{{ user_token }}",
                        serverUrl: "{{ http_host }}",
                        autoStart: false, // debugging only?
                        initDone: false,
                        startTime: (new Date()),
                        timeoutDuration: 24000, // time to answer question
                        sessionToken: "", // provided by server to load and answer questions
                        instructions: // track progress through instruction
                        {
                                completed: false, // all done?
                                i1complete: false, // first done?
                                i2timedOut: false // second done?
                        }
                },
                specialTimers: // always for special actions on timeout "quiz_item.item_type": function() {}
                {
                        "instructions2": function()
                        {
                        	$("#example_1").hide();
                        	$("#example_2").hide();
                        	$("#example_3").show();
                                
                               // $.plopquiz.specialTimers["instructions2"] = function() {};
                        }
                },
                quizItem: Object(),
                proficiencies: // hardcoded proficiencies, will come from server in the future
              /*  [
                        "Freebase",
                        "Building Webapps",
                        "Startup Financing"
                ] */
                
                {{ proficiencies }} {# proficiencies loaded from handler #}
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
                       // error: console.log('quiz frame error'),
                        success: function(html,status)
                        {
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
                                                        $(".timer_inner", self).stop();
                                                        
                                                        // resize
                                                        $(".timer_inner", self)
                                                                .css("width", "100%");
                                                                
                                                                $.plopquiz.settings.timer_width = $('.timer_bar').width(); // to calculate score
                                                         
                                                         
                                                        if (quizItem.item_type == "quiz_item")
        								{

									$('.timer_inner', self).animate({opacity: 1.0}, 2000, function()
									{
										$('#quiz_answers').find('div').removeClass('disabled').data("disabled", false);
										
										                                                        // start running the timer down
                                                        $(".timer_inner", self).animate(
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
                                                        
						}
                                                reset();
                                        })
                                        // these probably do the same thing
                                        .bind('loadingQuizItem', function()
                                        {
                                                $('.timer_inner', this).stop();
                                        })
                                        .bind('submitingAnswer', function()
                                        {
                                                $('.timer_inner', this).stop();
                                        });
                                
                                // totally useless?
                                //var textHolder = $('#blank').text();
                                var textHolder = '     ';

                                $('#quiz_answers .answer').hover(function()
                                {
                                        // skip doesn't have hover
                                	if ($(this).attr("id") == "skip")
                                                return;
                                                
                                                // hover event on span
                                                $(".answertext", this).addClass('hover');

					var blank_width = 15 + (10 * $(".answertext", this).text().length); //todo: multiplier may need adjustment

					$("#blank")
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
                                               $('#quiz_answers').find('div').addClass('disabled').data("disabled", true);
                                });

                                $("#quiz_content")
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

                                // mostly debugging
                                if($.plopquiz.settings.autoStart)
                                        $.plopquiz.start();
                        }
                });

                var jsonpcallback = false;

                // this is a jQuery JSONP timeout hack
                for(var i in window)
                {
                        // if it starts with jsonp, keep going, we want the last one
                        if(i.substring(0,5) == "jsonp")
                                jsonpcallback = i;
                }
                
                //console.log(jsonpcallback);
                // this should be the last (if any) jsonp123blah123 callback
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
                        /* COMMENTED OUT FOR DEBUGGING  if(this.src.indexOf(jsonpcallback) > -1)  */
                        
                        if(this.src.indexOf(jsonpcallback) > -1)
                	//console.log(this.src.indexOf(jsonpcallback));
                	
                                this.onload = function()
                                {
                                        // the script just loaded so stop the timeout
                                        clearTimeout(timewatch);
   

                        
                        var widget_html = "{% spaceless %}{{ widget_html }}{% endspaceless %}";
    
                        	// yay the widget script loaded, setup the start handler
                                        $("#pqwidget").append(
                                                $(widget_html).hide().fadeIn().click($.plopquiz.start)
                                        );
                                        
                                 $('#subject_1').s3Slider({ //eventually this needs to iterate through multiple subjects
            timeOut: 8300
        });  
                                }
                                
                                
                });
        }; // $.plopquiz.init

        $.plopquiz.start = function()
        {
                // if the click handler is setup before the frame loads, wait for it
                if($("#quiz_wrap").length > 0)
                        $.plopquiz.loadItem();
                else
                        setTimeout($.plopquiz.start, 600);
        }; // $.plopquiz.start









        $.plopquiz.loadItem = function(quizItem)
        {
             
                // this could use some clean up, the transistions between hard code and real quizItem is a bit funky
                var quizItem = $.plopquiz.quizItem = ((quizItem && quizItem.answers) ? quizItem : $.plopquiz.fetchNextItem());

                if(!quizItem)
                        return;
                        
                $('#quiz_inner > div').addClass('disabled').animate({opacity:0},100); 
                	

		
                	$('#quiz_loading').show().animate({opacity: .5}, 100).animate({opacity: .5 }, {duration:1000, complete:function(){ 

                        	
                        
                        	
                        	

                        // hardcoded versus server provided
                quizItem["url"] = quizItem.url ? quizItem.url : "/quiz_item/?token=" + $.plopquiz.settings.sessionToken;

                // heeaayy, we're loading a quiz item
                $.event.trigger('loadingQuizItem');
                
                
                // load from the server not the widget location
                $.ajax({
                        url: $.plopquiz.settings.serverUrl + quizItem.url,
                        dataType: "jsonp",
                        success: function(html, s)
                        {
// set the quiz content -- it can be seen
$('#quiz_content').html(html);
// hide the answers for now
     $('#quiz_answers .answer').hide()

                                $('#quiz_loading').animate({opacity: 0}, { 
                                	duration: 0, complete: function(){ 

                                		$('#quiz_inner > div').animate({opacity:1},{duration:200}).removeClass('disabled');
                                		
                                		 } }).hide();
                                		 
                                
                                for ( var i in quizItem.answers )
                                {
                                        // 1,2 or 3 answers are okay
					/* some settings... */
					
					$('#quiz_content').attr('class', quizItem.item_type + '_content');
					$('#quiz_answers').attr('class', quizItem.item_type + '_answers');
					$('#quiz_inner').attr('class', quizItem.item_type + '_quiz_inner');
					$('.quiz_selection').attr('id', quizItem.item_type + '_quiz_selection');
					
					if (quizItem.item_type == 'intro' || quizItem.item_type == 'quiz_complete'){  
						var this_answer = $('#quiz_answers #confirm');
					}
					else if (quizItem.item_type == 'begin_quiz')
					{
						var this_answer = $('#quiz_answers #confirm');
					}else
					{ 
						var this_answer = $('#quiz_answers .answer:eq(' + i + ')'); 
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
                                        $("#quiz_timer").show();
                                else
                                        $("#quiz_timer").hide();
                                
                                // not all items need skipping
                                if(!quizItem.noSkip)
                                        $("#skip").show();
                                else
                                        $("#skip").hide();

                                /*
                                 * Setup special cases for instructions here
                                 */
                                
				if(quizItem.item_type == "intro")
                                {
                                	 $('#quiz_answers #confirm').attr('class', 'answer intro_quiz').find('span.continue_button').text('Practice Quiz');
                                	 $('button span#intro_button').show(); // todo: this is coming late 
                                	 $('.intro_frame_content #subject_container_1').show().addClass('selected'); // show first subject
                                	 
                                     $('#subject_1').s3Slider({ timeOut: 5300 });  
        
                         $('div.subject_thumb_container > div').each(function(n){ console.log($('#subject_thumb_' + n)); console.log(n);  
                        $('#subject_thumb_' + n).s3Slider({ timeOut: 5300 });  // todo: slight offset
                          });  
        
                                     
                                	 $('div.subject_thumb_container li').click(function(){ //TODO: Slider/Coverflow (low priority)
                                	 	$('div.subject_thumb_container li').removeClass('selected_thumb'); $(this).addClass('selected_thumb');
                                	 	$('.intro_frame_content .subject_container').hide('fast');
                                	 	$('.intro_frame_content #subject_container_' + $(this).attr('id')).show('fast');
                                	 	
                                	 	$('#subject_' + $(this).attr('id')).s3Slider({ timeOut: 5300 }); // initiate a slider for the subject being shown.
                                	 	
                                	 	
                                	 	});
                                	 
                                	 $('button.take_test').show();
                                	 $('div#quiz_answers div.go_to_site').show();
                                	 

					if (quizItem.vendor.length > 1)
                                        {
                                                $('p#employer').find('b').text(quizItem.vendor);
                                        }
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

                                        $("#skip_tutorial").click(function()
                                        {
                                                $.plopquiz.currentItem = 3;
                                                $.plopquiz.loadItem();
                                        });

                                        $("#quiz_answers .answer").mouseover(i1mouseOver);
                                }
                                
				if(quizItem.item_type == "instructions2")
                                {
                                        $('a#skip').hide(); 

                                        $("#skip_tutorial").click(function()
                                        {
                                                $.plopquiz.currentItem = 3;
                                                $.plopquiz.loadItem();
                                        });
                                }

                                if(quizItem.item_type == "begin_quiz")
                                {
					var p = {};
                            $('#quiz_answers #confirm').removeClass('intro_quiz').addClass('begin_quiz').find('span.continue_button').text('Begin Quiz');                    
                                        // this is a bit hacked together, later the proficiencies will be loaded from the server
                                        for(var i in $.plopquiz.proficiencies)
                                                $("#proficiency_choices")
                                                        .append('<input type="checkbox" value="' + $.plopquiz.proficiencies[i] + '" checked /><span class="proficiency">' + $.plopquiz.proficiencies[i] + '</span><br />');
                                }
                                
                                if(quizItem.item_type == "quiz_item")
                                {
                                        // reset the blank space
                                        $('#blank').empty();
                                        // hide the question until everything is loaded
                                        $('#quiz_content')
                                                .css('opacity', 0);
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
                        },
                        error: function(xhr,s)
                        {
                                console.log("Ajax error: ", xhr,s);
                        }
                });
     
     	}});
     
        };









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
                        $('div#quiz_answers div.go_to_site').hide();
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
                                        $('.timer_bar').stop();
                                        $('.timer_bar').css('width', '100%'); 
                                        $('#example_1,#example_3').hide('slow');
                                        $('#example_2').show('slow');
                                        $('a#skip').show();
                                        //click binding
                                        $('#quiz_answers').find('#answer1,#answer2').addClass('disabled');
                                        $.plopquiz.settings.instructions.skip_segment = "true";

                                        return;
                                }
                                else
                                        $.plopquiz.loadItem();
                                       $('#quiz_answers').find('#answer1,#answer2').removeClass('disabled');
                        break;

                        case "begin_quiz":
                                // clear out proficiencies in case its a restart
                                $.plopquiz.settings.proficiencies = Array();

                                $('#proficiency_choices input:checked').each(function() { $.plopquiz.settings.proficiencies.push($(this).val()); });
                                $('.timer_bar').css('width', '100%'); 

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
                                
                                var timer_status = $('.timer_bar').width()/$.plopquiz.settings.timer_width;
                                var vendor = "" //TODO: retrieve vendor token.
                                $(".timer_inner", self).stop();
                                $('.timer_bar').css('width', '100%');
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
                $.plopquiz.init();
        });
};








var pqjs = document.getElementsByTagName("script");
pqjs = pqjs[pqjs.length - 1];

var widgetSource = pqjs.src.substring(0, pqjs.src.lastIndexOf("/") + 1);

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


        //if ($.fn.s3Slider)
        //setTimeout(waitForSlider, 60);
        
function waitForSlider()
{
	
}
