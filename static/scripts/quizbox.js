/*
* Quizbox Library 

*/

(function($) {
var opts = {}, 
imgPreloader = new Image, imgTypes = ['png', 'jpg', 'jpeg', 'gif'], 
loadingTimer, loadingFrame = 1;

$.fn.quizbox = function(settings) {
	opts.settings = $.extend({}, $.fn.quizbox.defaults, settings);

	$(this).data('opts', opts);

	$.fn.quizbox.init();

	$.fn.quizbox.defaults =
	{
		hideOnContentClick:	false,
		zoomSpeedIn:		500,
		zoomSpeedOut:		500,
		frameWidth:			600,
		frameHeight:		410,
		overlayShow:		false,
		overlayOpacity:		0.4,
		itemLoadCallback:	null
	};

	return $(this).each(function()
	{
		var $this = $(this);
		var o = $.metadata ? $.extend({}, opts.settings, $this.metadata()) : opts.settings;

		$this.unbind('click').click(function()
		{
			$.fn.quizbox.start(this, o); 
			return false;
		});
	});
};

$.fn.quizbox.start = function(el, o)
{
	if (opts.animating) return false;

	doInit();  /*  Should be when quiz initiates, after intro. DELETES EXISTING DATASTORE ENTRIES - JUST FOR DEMO */

	if (o.overlayShow) {
		$("#quiz_wrap").prepend('<div id="quiz_overlay"></div>');
		$("#quiz_overlay").css({'width': $(window).width(), 'height': $(document).height(), 'opacity': o.overlayOpacity});

		if ($.browser.msie)
		{
			$("#quiz_wrap").prepend('<iframe id="quiz_bigIframe" scrolling="no" frameborder="0"></iframe>');
			$("#quiz_bigIframe").css({'width': $(window).width(), 'height': $(document).height(), 'opacity': 0});
		}

		//$("#quiz_overlay").click($.fn.quizbox.close);
	}

	opts.itemArray	= [];
	opts.itemNum	= 0;

	if (jQuery.isFunction(o.itemLoadCallback))
	{
		o.itemLoadCallback.apply(this, [opts]);

		var c	= $(el).children("img:first").length ? $(el).children("img:first") : $(el);
		var tmp	= {'width': c.width(), 'height': c.height(), 'pos': $.fn.quizbox.getPosition(c)}

		for (var i = 0; i < opts.itemArray.length; i++)
		{
			opts.itemArray[i].o = $.extend({}, o, opts.itemArray[i].o);

			if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0)
				opts.itemArray[i].orig = tmp;
		}
	}
	else
	{
		if (!el.rel || el.rel == '')
		{
			var item = {url: el.href, title: el.title, o: o};

			if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0)
			{
				var c = $(el).children("img:first").length ? $(el).children("img:first") : $(el);
				item.orig =
				{
					'width': c.width(),
					'height': c.height(),
					'pos': $.fn.quizbox.getPosition(c)
				}
			}

		opts.itemArray.push(item);

		}
		else
		{
			var arr = $("a[@rel=" + el.rel + "]").get();

			for (var i = 0; i < arr.length; i++)
			{
				var tmp = $.metadata ? $.extend({}, o, $(arr[i]).metadata()) : o;
				var item =
				{
					url: arr[i].href,
					title: arr[i].title,
					o: tmp
				};

				if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0)
				{
					var c = $(arr[i]).children("img:first").length ? $(arr[i]).children("img:first") : $(el);
					item.orig =
					{
						'width': c.width(),
						'height': c.height(),
						'pos': $.fn.quizbox.getPosition(c)
					};
				}

				if (arr[i].href == el.href) opts.itemNum = i;
					opts.itemArray.push(item);
			}
		}
	}

	$.fn.quizbox.changeItem(opts.itemNum);
	};

	$.fn.quizbox.changeItem = function(n)
	{
		$.fn.quizbox.showLoading();

		opts.itemNum = n;

		$("#quiz_nav").empty();
		$("#quiz_outer").stop();
		$("#quiz_title").hide();
		$(document).unbind("keydown");

		imgRegExp = imgTypes.join('|');
		imgRegExp = new RegExp('\.' + imgRegExp + '$', 'i');

		var url = opts.itemArray[n].url;



		if (url.match(/#/))
		{
			var target = window.location.href.split('#')[0];
			target = url.replace(target,'');

			$.fn.quizbox.showItem('<div id="quiz_div">' + $(target).html() + '</div>');

			$("#quiz_loading").hide();

		} else if (url.match(imgRegExp))
		{
			$(imgPreloader).unbind('load').bind('load', function()
			{
				$("#quiz_loading").hide();

				opts.itemArray[n].o.frameWidth	= imgPreloader.width;
				opts.itemArray[n].o.frameHeight	= imgPreloader.height;

				$.fn.quizbox.showItem('<img id="quiz_img" src="' + imgPreloader.src + '" />');

			})
			.attr('src', url + '?rand=' + Math.floor(Math.random() * 999999999) );
		}
		else
		{
			$.fn.quizbox.showItem('<iframe id="quiz_frame" scrolling="no" onload="$.fn.quizbox.showIframe()" name="quiz_iframe' + Math.round(Math.random()*1000) + '" frameborder="0" hspace="0" src="' + url + '"></iframe>');
		}
	};

$.fn.quizbox.showIframe = function() {
	$("#quiz_loading").hide();
	$("#quiz_frame").show('slow');

	/* preview answer in iframe */

	var blankspan = $('.blank', window.frames[0].document);
	$('.answer').hover(function()
	/* if id is skip, don't do this */
	{
	        if (this.id != "skip") {
            blankspan.fadeTo(1,0.5);
			blankspan.html("&nbsp;" + $(this).text() + "&nbsp;");
        }
	    blankspan.fadeTo("slow", 1);
  
		
			
			
	},
	function()
	{
	    
		blankspan.empty();
		blankspan.html("&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;");
        blankspan.fadeTo(100, 0.5);
	});
}

 $.fn.quizbox.showItem = function(val) {
	 $.fn.quizbox.preloadNeighborImages();

	 var viewportPos = $.fn.quizbox.getViewport();
	 var itemSize = $.fn.quizbox.getMaxSize(viewportPos[0] - 50, viewportPos[1] - 100, opts.itemArray[opts.itemNum].o.frameWidth, opts.itemArray[opts.itemNum].o.frameHeight);

	 var itemLeft = viewportPos[2] + Math.round((viewportPos[0] - itemSize[0]) / 2) - 20;
	 var itemTop = viewportPos[3] + Math.round((viewportPos[1] - itemSize[1]) / 2) - 40;


	 /* =========== */
	 /* = Dimension properties = */
	 /* =========== */

	 /*  redundant - TODO refactor */

	 if (opts.itemArray[opts.itemNum].item_type == "score") {
		 /* score card */
		 var itemOpts = {
			 'left':		143 + 'px', 
			 'top':		0 + 'px', 
			 'width':	380 + 'px', 
			 'height':	370 + 'px'	
		 };
	 }else if (opts.itemArray[opts.itemNum].item_type == "intro"){
		 /* intro */
		 var itemOpts = {
			 'left':		143 + 'px', 
			 'top':		0 + 'px', 
			 'width':	392 + 'px', 
			 'height':	410 + 'px'	
		 };
	 }else if (opts.itemArray[opts.itemNum].item_type == "instructions"){
		 /* instructions */
		 var itemOpts = {
			 'left':		143 + 'px', 
			 'top':		0 + 'px', 
			 'width':	392 + 'px', 
			 'height':	400 + 'px'	
		 };
	 }else if (opts.itemArray[opts.itemNum].item_type == "instructions2"){
		 /* instructions2 */
		 var itemOpts = {
			 'left':		143 + 'px', 
			 'top':		0 + 'px', 
			 'width':	392 + 'px', 
			 'height':	415 + 'px'	
		 };
		 	 }else if (opts.itemArray[opts.itemNum].item_type == "begin_quiz"){
		 var itemOpts = {
			 'left':		143 + 'px', 
			 'top':		0 + 'px', 
			 'width':	370 + 'px', 
			 'height':	410 + 'px'	
		 };
		 
	 }else{   
		 /* during quiz */
		 var itemOpts = {
			 'left':		73 + 'px', 
			 'top':		10 + 'px', 
			 'width':	512 + 'px', 
			 'height':	404 + 'px'	
		 };
	 }
	 
	 if (opts.active) {
		 $('#quiz_content').fadeOut("normal", function() {
				 $("#quiz_content").empty();

				 $("#quiz_outer").animate(itemOpts, "normal", function() {
					 $("#quiz_content").append($(val)).fadeIn("normal");
					 $.fn.quizbox.updateDetails();
					 });
				 });

	 } else {
		 opts.active = true;

		 $("#quiz_content").empty();

		 if ($("#quiz_content").is(":animated")) {
			 
		 }

		 if (opts.itemArray[opts.itemNum].o.zoomSpeedIn > 0) {
			 opts.animating		= true;
			 itemOpts.opacity	= "show";
			 $("#quiz_outer").css({
					 'top':		opts.itemArray[opts.itemNum].orig.pos.top - 18,
					 'left':		opts.itemArray[opts.itemNum].orig.pos.left - 18,
					 'height':	opts.itemArray[opts.itemNum].orig.height,
					 'width':	opts.itemArray[opts.itemNum].orig.width + 50
					 });

			 $("#quiz_content").append($(val)).show();

			 $("#quiz_outer").animate(itemOpts, opts.itemArray[opts.itemNum].o.zoomSpeedIn, function() {
					 opts.animating = false;
					 $.fn.quizbox.updateDetails();
					 });

		 } else {
			 $("#quiz_content").append($(val)).show();
			 $("#quiz_outer").css(itemOpts).show();
			 $.fn.quizbox.updateDetails();
		 }
	 }
 };








 $.fn.quizbox.updateDetails = function() {
	 $("#quiz_bg,#quiz_close").show();
	 
	 

 

		 if (opts.itemArray[opts.itemNum].item_type == "instructions") {
/*
			 var hover_count = 0;
		 
		 $("a#answer1").mouseover(function(){
		    hover_count += 1;
		    console.log(hover_count);
                    if (hover_count > 1) {
		            $('div#example_1', window.frames[0].document).hide();
		            $('div#example_2', window.frames[0].document).show();
			    $('.blank', window.frames[0].document).hide();
		    }
    
         });
         
  
         
          $("a#answer2").mouseover(function(){
		    hover_count += 1;
		    console.log(hover_count);
                    if (hover_count > 1) {
		            $('div#example_1', window.frames[0].document).hide();
		            $('div#example_2', window.frames[0].document).show();
			    $('.blank', window.frames[0].document).hide();
		    }
         });
		*/ 
     }


 /* =========== */
 /* = Update Button Display = */
 /* =========== */
 
	function startTimer(cb)
	{
		 if($.fn.quizbox._t)
		 {
			 clearTimeout($.fn.quizbox._t);
			 $('.timer_bar').stop().css('width', '100%');
		 }
		 // Start timer --Morgan
		 $.fn.quizbox._t = setTimeout(function() {
			$('.timer_bar').animate(
			{
				width:	0
			},
			{
				duration:	16000,
				easing:	'linear',
				complete:	(function()
				{					
					
					if(!cb)
						return function()
						{
							$('#skip').click();  //not the same as skip - TODO format ajax call for timeout /
							$('.timer_bar').css('width', '100%');
							$.fn.quizbox._t = false;
						};
					
					return cb;
				})()
			});
		 },1000);
	};
		 
		 
 
 
	 /* Fill in titles for answer keys - redundant! make this more robust before something blows up*/
	 if (opts.itemArray[opts.itemNum].item_type == "quiz_item") {
		 $('#quiz_title').show();
		 $('#quiz_title div.buttons').hide(); 
		 $('#quiz_title div#quiz_answers').show();           

		 /* TODO change to toggle */
		 $('#quiz_answers div#answer1').empty();     
		 $('#quiz_answers div#answer2').empty();
		 $('#quiz_answers div#answer3').empty();
		 $('#quiz_answers div#answer1').html(opts.itemArray[opts.itemNum].answer1);     
		 $('#quiz_answers div#answer2').html(opts.itemArray[opts.itemNum].answer2);
		 $('#quiz_answers div#answer3').html(opts.itemArray[opts.itemNum].answer3);
		 $('#quiz_answers div.arrow').html('<img src="/static/stylesheets/img/pinkarrow.png"/>');
		startTimer();
        var click_status = [];
        click_status[opts.itemNum] = false;
        
         $('div#quiz_answers').find('a').click(function() {
		 				
                    if (click_status[opts.itemNum] == false) {    
					$.fn.quizbox.submit_answer(this);
					
					
					click_status[opts.itemNum] = true;
					return click_status;
                }
				});
			
	 }else if (opts.itemArray[opts.itemNum].item_type == "intro") {
		 /* hide answers and show hidden intro choices */
		 $('#quiz_title').show();
		 $('#quiz_title div.buttons').hide(); 
		 $('#quiz_title div#quiz_intro').fadeIn('slow');  
		
		 $('#quiz_intro div#choose_quiz').html(opts.itemArray[opts.itemNum].choose_quiz);
	 }else if (opts.itemArray[opts.itemNum].item_type == "instructions") {
		$('#example_2', window.frames[0].document).hide();
		$('#example_1', window.frames[0].document).fadeIn('slow');
		$('#quiz_title').show();
		$('#quiz_title div.buttons').hide();   
		$('#quiz_title div#quiz_instructions').show();  
		$('#quiz_instructions div#answer1').html(opts.itemArray[opts.itemNum].answer1);     
		$('#quiz_instructions div#answer2').html(opts.itemArray[opts.itemNum].answer2);
		$('#answer1,#answer2').mouseover(function(e)
		{
			$(this).not('.hovered').addClass('hovered');
			if($(this).parent().find('.hovered').length > 1 && $('#example_2', window.frames[0].document).is(':hidden'))
			{
				$('#example_1,#example_2', window.frames[0].document).toggle('slow');
				
				$('#quiz_instructions').find('#answer1,#answer2').click(function() {
					$.fn.quizbox.submit_answer(this);
				});
			}
		});
	 }else if (opts.itemArray[opts.itemNum].item_type == "instructions2") {
		//$('#example_1', window.frames[0].document).show();
		$('#example_2', window.frames[0].document).hide();

		$('#quiz_title').show();
		$('#quiz_title div.buttons').hide();
		$('#quiz_title div#quiz_instructions2').show();  

		$('#quiz_instructions2 div#answer1').html(opts.itemArray[opts.itemNum].answer1);

		$('.timer_bar').css('margin-left', '-10px');
		$('.timer_bar').css('width', '112%');

		$('#quiz_instructions2 div#answer2').html(opts.itemArray[opts.itemNum].answer2)
		$('#quiz_instructions2')
		.find('#answer1,#answer2').click(function()
		{
		    
			$('#example_1,#example_3', window.frames[0].document).hide('slow');
			$('#example_2', window.frames[0].document).show('slow');
			clearTimeout($.fn.quizbox._t);
			$('.timer_bar').stop();
			$('.timer_bar').css('width', '112%'); 

			// bind the skip button
			$('#quiz_title').find('#skip').click(function() { $.fn.quizbox.submit_answer(this); });
			$('#quiz_instructions2').find('#answer1,#answer2').unbind('click');
		});

		 
		 var timerCb = function()
		 {
			$('.timer_bar').css('width', '100%');						
			$('#example_1,#example_2', window.frames[0].document).hide();
			$('#example_3', window.frames[0].document).show();
			startTimer(timerCb);
			
		 };
		 startTimer(timerCb);
		 
	 }else if (opts.itemArray[opts.itemNum].item_type == "begin_quiz") {
	     $('#quiz_title').show();
	     $('#quiz_title div.buttons').hide();
	     $('#quiz_title div#quiz_begin_quiz').show();
        $('.timer_bar').css('margin-left', '0px'); 
        $('#quiz_begin_quiz').find('#startquiz').click(function() {
			opts.itemArray = jQuery.grep(opts.itemArray, function(e,i)
			{
				return (
					($('#proficiency_choices', window.frames[0].document).find('[@value=' + e.proficiency + ']:checked').length > 0) ||
					(!e.proficiency)
				);
			});
					$.fn.quizbox.submit_answer(this);
					
				});
	     	 
	 }else if (opts.itemArray[opts.itemNum].item_type == "score") {
		 $('#quiz_title').show();
		 $('#quiz_title div.buttons').hide();
		 $('#quiz_title div#quiz_score').show();
	 }else{
		 $('#quiz_title').hide();
	 }



	 if (opts.itemArray[opts.itemNum].o.hideOnContentClick) {
		 $("#quiz_content").click($.fn.quizbox.close);
		
	 } else {
		 $("#quiz_content").unbind('click');
	 }


	 $(document).keydown(function(event) {
		 if (event.keyCode == 27) {
			 $.fn.quizbox.close();
		 } else if(event.keyCode == 37 && opts.itemNum != 0) {
			 $.fn.quizbox.changeItem(opts.itemNum - 1);
		 } else if(event.keyCode == 39 && opts.itemNum != (opts.itemArray.length - 1)) {
			 $.fn.quizbox.changeItem(opts.itemNum + 1);
		 }
	 });
};

 $.fn.quizbox.preloadNeighborImages = function() {
	 if ((opts.itemArray.length - 1) > opts.itemNum) {
		 preloadNextImage = new Image();
		 preloadNextImage.src = opts.itemArray[opts.itemNum + 1].url;
	 }

	 if (opts.itemNum > 0) {
		 preloadPrevImage = new Image();
		 preloadPrevImage.src = opts.itemArray[opts.itemNum - 1].url;
	 }
 };

 $.fn.quizbox.close = function() {
	 if (opts.animating) return false;

	 // kill animation to window does not reopen on 'skip' --Morgan
	 $('.timer_bar').stop();

	 $(imgPreloader).unbind('load');
	 $(document).unbind("keydown");

	 $("#quiz_loading,#quiz_title,#quiz_close,#quiz_bg").hide();

	 $("#quiz_nav").empty();

	 opts.active	= false;

	 if (opts.itemArray[opts.itemNum].o.zoomSpeedOut > 0) {
		 var itemOpts = {
			 'top':		opts.itemArray[opts.itemNum].orig.pos.top - 18,
			 'left':		opts.itemArray[opts.itemNum].orig.pos.left - 18,
			 'height':	opts.itemArray[opts.itemNum].orig.height,
			 'width':	opts.itemArray[opts.itemNum].orig.width,
			 'opacity':	'hide'
		 };

		 opts.animating = true;

		 $("#quiz_outer").animate(itemOpts, opts.itemArray[opts.itemNum].o.zoomSpeedOut, function() {
				 $("#quiz_content").hide('fast').empty();
				 $("#quiz_overlay,#quiz_bigIframe").remove();
				 opts.animating = false;
				 });

	 } else {
		 $("#quiz_outer").hide();
		 $("#quiz_content").hide().empty();
		 $("#quiz_overlay,#quiz_bigIframe").fadeOut("fast").remove();
	 }
 };

 $.fn.quizbox.showLoading = function() {
	 clearInterval(loadingTimer);

	 var pos = $.fn.quizbox.getViewport();

	 $("#quiz_loading").css({'left': ((pos[0] - 40) / 2 + pos[2]), 'top': ((pos[1] - 40) / 2 + pos[3])}).show();
	 $("#quiz_loading").bind('click', $.fn.quizbox.close);

	 loadingTimer = setInterval($.fn.quizbox.animateLoading, 66);
 };

 $.fn.quizbox.animateLoading = function(el, o) {
	 if (!$("#quiz_loading").is(':visible')){
		 clearInterval(loadingTimer);
		 return;
	 }

	 $("#quiz_loading > div").css('top', (loadingFrame * -40) + 'px');

	 loadingFrame = (loadingFrame + 1) % 12;
 };

 /* =========== */
 /* = Create Buttons = */
 /* =========== */


 $.fn.quizbox.init = function() {


	 /* Create Answer Buttons */
	 if (!$('#quiz_wrap').length) {
		 $('<div id="quiz_wrap"><div id="quiz_loading"><div></div></div><div id="quiz_outer"><div id="quiz_inner"><div id="quiz_nav"></div><div id="quiz_close"></div><div id="quiz_content"></div><div id="quiz_title"></div></div><div id="minutes-boxNOTYET"><div id="minutes-countNOTYET"> </div><div id="minutes-outerNOTYET"> <div id="minutes-innerNOTYET"> </div> </div></div></div></div>').appendTo("body");
		 $('<div id="quiz_bg"><div class="quiz_bg quiz_bg_n"></div><div class="quiz_bg quiz_bg_ne"></div><div class="quiz_bg quiz_bg_e"></div><div class="quiz_bg quiz_bg_se"></div><div class="quiz_bg quiz_bg_s"></div><div class="quiz_bg quiz_bg_sw"></div><div class="quiz_bg quiz_bg_w"></div><div class="quiz_bg quiz_bg_nw"></div></div>').prependTo("#quiz_inner");
		 /* append timer to iframe */


		 /* append score buttons to iframe */
		 $('<div id="quiz_score"  class="buttons"></div>').appendTo('#quiz_title');
	/*	 $('<a id="continue" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_pink_left"></td><td id="quiz_pink_main"><div class="arrow" style="margin-left:12px;"><img src="/static/stylesheets/img/pinkarrow.png" /></div><div class="skipitem" id="skiptext">Continue</div></td><td id="quiz_pink_right"></td></tr></table></a>').appendTo('#quiz_score'); */


		 /* append intro buttons to iframe */
		 // This is all really terrible. This should be done in HTML loaded from the server, the use jQuery to replace things like buttons and text
		 // There is WAAY to much overhead here.
		 
		 // This will be in the HTML very, very soon - James
		 
		 $('<div id="quiz_intro"  class="buttons"></div>').appendTo('#quiz_title');
		 $('<a id="take_quiz" onmouseover="" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr> <td id="quiz_purple_left"></td><td id="quiz_purple_main"><div class="answertext" id="take_quiz" style="width: 170px; font-size: 1.5em;">T<span style="font-size:.7em;"/>ake</span> T<span style="font-size:.7em;"/>his</span> Q<span style="font-size:.7em;"/>uiz</span></div></div></td><td id="quiz_purple_right"></td></tr></table></a>').appendTo('#quiz_intro');
			 // - Choose Between Quizzes $('<a id="choose_quiz" class="answer" style="font-size:13px; margin-left:30px;" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_pink_left"></td><td id="quiz_pink_main" style="width:45px;"><div class="answertext" style="margin: 3px 0pt 0pt 1px; font-size: 13px; width: 36px; line-height: 1.1em;" id="choose_quiz"></div></td><td id="quiz_pink_right"></td></tr></table></a>').appendTo('#quiz_intro');


			 /* append instruction buttons to iframe */
			 $('<div id="quiz_instructions"  class="buttons"></div>').appendTo('#quiz_title');
			 $('<a id="answer1" onmouseover="" class="answer" style="margin-left:53px;" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr> <td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer1"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_instructions');
			 $('<a id="answer2" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" style="margin-left:1px; width:101%;" id="answer2"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_instructions');

			 $('<div id="quiz_instructions2" class="buttons" style="margin-top:7px;margin-left:26px;"></div>').appendTo('#quiz_title');
			 //Arg, this has been getting animated while not visible, one ID per page!
			 $('<div class="timer_wrapper" id="quiz_timer_instruction"><div class="timer_bar timer_inner"></div></div>').appendTo('#quiz_instructions2');
			$('<a id="answer1" onmouseover="" class="answer"  href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr> <td id="quiz_blue_left"></td><td id="quiz_blue_main" style="min-width:60px;"><div class="answertext"  id="answer1"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_instructions2');
			 $('<a id="answer2" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_blue_left"></td><td id="quiz_blue_main" style="min-width:60px;"><div class="answertext" style="margin-left:-12px;" id="answer2"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_instructions2');
			 $('<a id="skip" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_pink_left"></td><td id="quiz_pink_main"><div class="arrow"><img src="/static/stylesheets/img/arrow.png" /></div><div class="skipitem" id="skiptext">Skip</div></td><td id="quiz_pink_right"></td></tr></table></a>').appendTo('#quiz_instructions2');

            $('<div id="quiz_begin_quiz" class="buttons" style=" margin-top:7px"></div>').appendTo('#quiz_title');
             $('<a id="startquiz" class="answer" href="#" style="margin-top:7px; margin-left: 90px"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_purple_left"></td><td id="quiz_purple_main"><div class="skipitem" id="startquiz">S<span style="font-size:.7em;"/>tart</span> Q<span style="font-size:.7em;"/>uiz</span>!</div></td><td id="quiz_purple_right"></td></tr></table></a>').appendTo('#quiz_begin_quiz');



		 /* append quiz buttons to iframe */
		 $('<div id="quiz_answers" class="buttons"></div>').appendTo('#quiz_title');
		 $('<div class="timer_wrapper" id="quiz_timer"><div class="timer_bar timer_inner"></div></div>').appendTo('#quiz_answers');

		 $('<a id="answer1" onmouseover="" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr> <td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer1"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_answers');
		 $('<a id="answer2" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer2"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_answers');
		 $('<a id="answer3" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer3"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_answers');
		 $('<a id="skip" class="answer" href="#"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_pink_left"></td><td id="quiz_pink_main"><div class="arrow"><img src="/static/stylesheets/img/arrow.png" /></div><div class="skipitem" id="skiptext">Skip</div></td><td id="quiz_pink_right"></td></tr></table></a>').appendTo('#quiz_answers');

		 /* initialize automatic countdown...if it reaches zero, changeItem +1 */
		 $("#minutes-box").hide();

		 /* effect on answer hover */

		 $(".answer").hover(function(){
				 $(this).css({
				     'font-variant': 'small-caps',
				     'letter-spacing': '.02em'
				     });
				 

				 },function(){
				 $(this).css({'font-variant': 'normal',
				 'letter-spacing': '.04em'
				 });
				 });


		 function timeleft(timetype){
			 days=0;hours=0;mins=0;
			 var e = new Date(2008,11,25,0,0,0);
			 var now  = new Date();
			 var left = e.getTime() - now.getTime();

			 left = Math.floor(left/1000);
			 days = Math.floor(left/86400);
			 left = left%86400;
			 hours=Math.floor(left/3600);
			 left=left%3600;
			 mins=Math.floor(left/22);
			 left=left%60;
			 secs=Math.floor(left);

			 switch(timetype){
				 case "s":
					 return secs;
				 break;
				 case "m":
					 return mins;
				 break;
				 case "h":
					 return hours;
				 break;
				 case "d":
					 return days;
				 break;
			 }
		 }

		 function set_start_count(){


			 set_minute_count();

		 }

		 function set_minute_count(){
			 m = timeleft('m');
			 $('#minutes-count').text(m.toString()+ ' minute(s)');
		 }


		 function update_minute(){
			 var now = new Date();
			 var mw = $('#minutes-outer').css('width');
			 mw = mw.slice(0,-2);
			 var s = now.getSeconds(); 
			 sleft = (60 - s)
				 if (sleft == 0)
				 {
					 sleft=60;
				 }
			 m = ((sleft/60)*mw).toFixed();
			 $('#minutes-inner').css({width:m});
			 return sleft*1000;
		 }


		 function reset_minute(){
			 $('#minutes-inner').width($('#minutes-outer').width());
			 start_countdown_minute();
		 }


		 function start_countdown_minute(){
			 set_minute_count();
			 $('#minutes-inner').animate({width: 0}, update_minute(),reset_minute);
			 //update_minute());
		 }          



		 /* =========== */
		 /* = Click Binding = */
		 /* =========== */

     
     
     
		 /* submit answers and proceed to next question */
		 $('#quiz_title').find('#take_quiz').click(function() {
				 submit_answer(this);
		});

		 var submit_answer = $.fn.quizbox.submit_answer = function(answer){
			

			 if (answer.id == "#skip") {
				 var answer_text = "skip_item";
			 }else{
				 var answer_text = $(answer).text();
			 }


			 if (opts.itemArray[opts.itemNum].item_type == "quiz_item"){
				 var answer_slug = opts.itemArray[opts.itemNum].slug;
				 /* submit using AJAX function doAdd(picked answer, correct answer) */
				 SubmitScore(answer_text, answer_slug)
			 } /* add doChoose ajax call for choosing quiz */

			 if (opts.itemArray[opts.itemNum].item_type == "score"){
				  return false;
			 }

			 if (answer.id == "choose_quiz"){ 
				 /* TODO cycle through quiz choices */
				 var selection = $('#quiz_selections', window.frames[0].document);
				 selection.find('#quiz_selections').toggle();

				 return false;
			 }
			 /* proceed to next item */
			 $.fn.quizbox.changeItem(opts.itemNum + 1);
			 return false;
		 }        
	 } 

	 if ($.browser.msie) {
		 $("#quiz_inner").prepend('<iframe id="quiz_freeIframe" scrolling="no" frameborder="0"></iframe>');
	 }

	 if (jQuery.fn.pngFix) $(document).pngFix();

	 $("#quiz_close").click($.fn.quizbox.close);
 }; /* end init fn */





 $.fn.quizbox.getPosition = function(el) {
	 var pos = el.offset();

	 pos.top	+= $.fn.quizbox.num(el, 'paddingTop');
	 pos.top	+= $.fn.quizbox.num(el, 'borderTopWidth');

	 pos.left += $.fn.quizbox.num(el, 'paddingLeft');
	 pos.left += $.fn.quizbox.num(el, 'borderLeftWidth');

	 return pos;
 };

 $.fn.quizbox.num = function (el, prop) {
	 return parseInt($.curCSS(el.jquery?el[0]:el,prop,true))||0;
 };

 $.fn.quizbox.getPageScroll = function() {
	 var xScroll, yScroll;

	 if (self.pageYOffset) {
		 yScroll = self.pageYOffset;
		 xScroll = self.pageXOffset;
	 } else if (document.documentElement && document.documentElement.scrollTop) {
		 yScroll = document.documentElement.scrollTop;
		 xScroll = document.documentElement.scrollLeft;
	 } else if (document.body) {
		 yScroll = document.body.scrollTop;
		 xScroll = document.body.scrollLeft;	
	 }

	 return [xScroll, yScroll]; 
 };

 $.fn.quizbox.getViewport = function() {
	 var scroll = $.fn.quizbox.getPageScroll();

	 return [$(window).width(), $(window).height(), scroll[0], scroll[1]];
 };

 $.fn.quizbox.getMaxSize = function(maxWidth, maxHeight, imageWidth, imageHeight) {
	 var r = Math.min(Math.min(maxWidth, imageWidth) / imageWidth, Math.min(maxHeight, imageHeight) / imageHeight);

	 return [Math.round(r * imageWidth), Math.round(r * imageHeight)];
 };
})(jQuery);
