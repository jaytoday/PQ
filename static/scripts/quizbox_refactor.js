/*
* Quizbox Library 

*/

(function($)
{
	// garbage
	var opts = {}, 
	imgPreloader = new Image, imgTypes = ['png', 'jpg', 'jpeg', 'gif'], 
	loadingTimer, loadingFrame = 1;

	$.fn.quizbox = {}; //stub

	// When this was declared in $.fn.quizbox (after the extend), where was the first call getting its defaults from? --Morgan

	$.fn.quizbox = function(settings)
	{
		// disabled for now --Morgan
		return;
		opts.settings = $.extend({}, $.fn.quizbox.defaults, settings);

		// mostly debugging, but the global opts could cause problems in the end --Morgan
		$(this).data('opts', opts);

		$.fn.quizbox.init();

		return $(this).each(function() {
				var $this = $(this);
				// is $.metadata every delcared or used anywhere? --Morgan
				var o = $.metadata ? $.extend({}, opts.settings, $this.metadata()) : opts.settings;

				$this.unbind('click').click(function() {
					$.fn.quizbox.start(this, o); return false;
					});
				});
	};
	
	$.fn.quizbox.defaults =
	{
		hideOnContentClick:	false,
		zoomSpeedIn:		500,
		zoomSpeedOut:		500,
		frameWidth:			600,
		frameHeight:		410,
		overlayShow:		false,
		overlayOpacity:		0.4,
		imgDir:			'/static/html/img/',
		itemLoadCallback:	null,
		questionCounter:	0
		// counter only used for demo, this will be controlled in the backend
	};

	// this should be the final and (in the end) only onload
	$(function()
	{
		$('#quiz_loading')
			.bind('quizloading', function()
			{
				$(this)
					.css({
						left: ($(window).width() / 2),
						top: ($(window).height() / 2)
					})
					.show()
			})
			.bind('quizloaded', function()
			{
				$(this).hide();
			});

		$('.quizstart').click($.fn.quizbox.init);
	});

	$.fn.quizbox.fillInBlank = function(question,spaces)
	{
		var blank = $('<span id="quiz_blank"></span>');
		for(;spaces>0;spaces--)
			blank.append('&nbsp;');

		console.log(blank.text());
		blank.data('blankSpace', blank.html());
		
		return question.replace(/$BLANK$/, blank[0]);
	};

	$.fn.quizbox.init = function(el, o)
	{
		$.event.trigger('quizloading');

		$.fn.quizbox.defaults.questionCounter = 0;
		
		$('<div id="quiz_overlay"></div>')
			.css({
				width: $(window.document).width(),
				height: $(window.document).height(),
				opacity: $.fn.quizbox.defaults.overlayOpacity,
			})
			.appendTo(document.body)
			.bind('quizclose', function(e)
			{
				$(this).remove()
			})
			.click(function(e)
			{
				$.event.trigger('quizclose');
			});
		
		

		// The new way should be to load a quiz 'blank', then load info for each question into that
		if(!$.fn.quizbox.quizLoaded)
			$.ajax({
				url: '/static/html/quizbox.html',
				success: function(response, s)
				{
					$(response)
						.bind('quizclose', function()
						{
							$(this).hide();
						})
						.bind('quizloading', function()
						{
							$(this).show();
						})
						.bind('quizreposition', function()
						{
							$(this)
								.css({
									left: (($(window).width() / 4) - ($('#quiz_outer', this).width() / 2)),
									top: (($(window).height() / 4) - ($('#quiz_outer', this).height() / 2))
								});
						})
						.appendTo(document.body)
						.css(
						{
							left: ($(window).width() / 2),
							top: ($(window).height() / 2)
						})
						.find('#quiz_close')
							.click(function()
							{
								$.event.trigger('quizclose');
							});

					$.fn.quizbox.quizLoaded = true;

					$('#skip').click($.fn.quizbox.answerQuestion);

					$('#quiz_content').append('');


					$('#quiz_timer_bar').bind('quizstarted', function()
					{
					console.log('quizloaded?');
						var self = this;
						$(this).animate({
							width: 0,
						},
						{
							duration: 8000,
							easing: 'linear',
							complete: function()
							{
								$(self).width('100%');
								$.fn.quizbox.answerQuestion('skip');
							}
						});
					})
					.bind('questionanswered', function()
					{
						if($(self).is(':animated'))
							$(self).width('99%').stop();
					})
					.bind('quizclose', function()
					{
						$(this).stop();
					});

					$.fn.quizbox.loadQuestion($.fn.quizbox.defaults.questionCounter);	

					$.event.trigger('quizloaded');
					$.event.trigger('quizreposition');
				}
			});
		else
		{
			$('#quiz_wrapper').show();
			$.event.trigger('quizloaded');
		}

		return;
	}; // $.fn.quizbox.init

	// This is the demo version, the backend should push the questions forward
	$.fn.quizbox.loadQuestion = function(n)
	{
		var qi = questions[n];
		if(qi.title)
			$('#titletext').html(qi.title);
		
		if(qi.logo)
			$('#titlelogo').html(
				$('<img />')
					.attr('src', $.fn.quizbox.defaults.imgDir + qi.logo + '.png')
			);

		if(qi.subtitle)
			$('#quiz_subtitle').html(qi.subtitle);

		var blankWidth = 0, blankSpace;
		// buttons look kinda crappy, they need to be build in a better
		// liqiud layout, they keep dropping down, and with only two.
		$('#quiz_buttonbox .button')
			.unbind('click')
			.unbind('hover')
			.each(function(i)
			{
				if(qi.answers[i])
					$(this)
						.html(qi.answers[i].label)
						.show()
						.click((function(e)
						{
							if(qi.answers[i].load)
								return function(e)
								{
									$.fn.quizbox.loadQuestion(qi.answers[i].load);
								};
							else
								return function(e)
								{
									$.fn.quizbox.answerQuestion($(this).text());
								};
						})());

				var thisWidth;
				blankWidth = (blankWidth > (thisWidth = $(this).width())) ? blankWidth : thisWidth;
				blankSpaces = blankWidth / 7;
			})
			.hover(function()
			{
				$('#quiz_blank').html($(this).html());
			},
			function()
			{
				$('#quiz_blank').html($('#quiz_blank').data('blankSpace'));
			});
		
		if(qi.question)
			$('#quiz_question')
				.html(qi.question);

			$('#quiz_blank')
				.html((function()
				{
					blankSpace = "";
					for(var i = 0; i<(blankWidth/7); i++)
						blankSpace += "&nbsp;";
					return blankSpace;
				})())
				.data('blankSpace', blankSpace);


		$.event.trigger('quizstarted');
	}; // $.fn.quizbox.loadQuestion

	$.fn.quizbox.answerQuestion = function(answer)
	{
		$.fn.quizbox.loadQuestion(++$.fn.quizbox.defaults.questionCounter);

		$.event.trigger('questionanswered');
	}; // $.fn.quizbox.answerQuestion

$.fn.init.start_old = function()
{

	if (o.overlayShow) {
		$("#quiz_wrap").prepend('<div id="quiz_overlay"></div>');
		$("#quiz_overlay").css({'width': $(window).width(), 'height': $(document).height(), 'opacity': o.overlayOpacity});

		if ($.browser.msie) {
			$("#quiz_wrap").prepend('<iframe id="quiz_bigIframe" scrolling="no" frameborder="0"></iframe>');
			$("#quiz_bigIframe").css({'width': $(window).width(), 'height': $(document).height(), 'opacity': 0});
		}

		$("#quiz_overlay").click($.fn.quizbox.close);
	}

	opts.itemArray	= [];
	opts.itemNum	= 0;

	if (jQuery.isFunction(o.itemLoadCallback)) {
		o.itemLoadCallback.apply(this, [opts]);

		var c	= $(el).children("img:first").length ? $(el).children("img:first") : $(el);
		var tmp	= {'width': c.width(), 'height': c.height(), 'pos': $.fn.quizbox.getPosition(c)}

		for (var i = 0; i < opts.itemArray.length; i++) {
			opts.itemArray[i].o = $.extend({}, o, opts.itemArray[i].o);

			if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0) {
				opts.itemArray[i].orig = tmp;
			}
		}
		window.opts = opts;
	} else {
		if (!el.rel || el.rel == '') {
			var item = {url: el.href, title: el.title, o: o};

			if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0) {
				var c = $(el).children("img:first").length ? $(el).children("img:first") : $(el);
				item.orig = {'width': c.width(), 'height': c.height(), 'pos': $.fn.quizbox.getPosition(c)}
			}

			opts.itemArray.push(item);
		} else {
			var arr = $("a[@rel=" + el.rel + "]").get();

			for (var i = 0; i < arr.length; i++) {
				var tmp = $.metadata ? $.extend({}, o, $(arr[i]).metadata()) : o;
				var item = {url: arr[i].href, title: arr[i].title, o: tmp};

				if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0) {
					var c = $(arr[i]).children("img:first").length ? $(arr[i]).children("img:first") : $(el);
					item.orig = {'width': c.width(), 'height': c.height(), 'pos': $.fn.quizbox.getPosition(c)}
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

	console.log('loading URL', url);

	if (url.match(/#/)) {
		var target = window.location.href.split('#')[0];
		target = url.replace(target,'');

		$.fn.quizbox.showItem('<div id="quiz_div">' + $(target).html() + '</div>');

		$("#quiz_loading").hide();

	} else if (url.match(imgRegExp)) {
		$(imgPreloader).unbind('load').bind('load', function() {
				$("#quiz_loading").hide();

				opts.itemArray[n].o.frameWidth	= imgPreloader.width;
				opts.itemArray[n].o.frameHeight	= imgPreloader.height;

				$.fn.quizbox.showItem('<img id="quiz_img" src="' + imgPreloader.src + '" />');

				}).attr('src', url + '?rand=' + Math.floor(Math.random() * 999999999) );

	} else {
		$.fn.quizbox.showItem('<div></div>');
	}
};

$.fn.quizbox.showIframe = function()
{
	$("#quiz_loading").hide();
	$("#quiz_frame").show();

	/* preview answer in iframe */

	var blankspan = $('.blank', window.frames[0].document);
	/* if id is skip, don't do this */
	$('.answer').hover(function()
	{
		if (this.id != "skip") {
			blankspan.html("&nbsp;" + $(this).text() + "&nbsp;");
		}

	},
	function()
	{
		blankspan.empty();
		blankspan.html("&nbsp;&nbsp; &nbsp; &nbsp;&nbsp; &nbsp; &nbsp; &nbsp; &nbsp; &nbsp;");
	});
}

$.fn.quizbox.showItem = function(val)
{
	$.fn.quizbox.preloadNeighborImages();

	var viewportPos = $.fn.quizbox.getViewport();
	var itemSize = $.fn.quizbox.getMaxSize(viewportPos[0] - 50, viewportPos[1] - 100, opts.itemArray[opts.itemNum].o.frameWidth, opts.itemArray[opts.itemNum].o.frameHeight);

	var itemLeft = viewportPos[2] + Math.round((viewportPos[0] - itemSize[0]) / 2) - 20;
	var itemTop = viewportPos[3] + Math.round((viewportPos[1] - itemSize[1]) / 2) - 40;


	/* =========== */
	/* = Dimension properties = */
	/* =========== */

	/*  redundant - TODO refactor */

	itemOpts = { top: 0, left: 143 };

	if (opts.active)
	{
		$('#quiz_content').fadeOut("normal", function()
		{
			//$("#quiz_content").empty();

			$("#quiz_outer").animate(itemOpts, "normal", function()
			{
				$("#quiz_content").append($(val)).fadeIn("normal");
				$.fn.quizbox.updateDetails();
			});
		});
	}
	else
	{
		opts.active = true;

		//$("#quiz_content").empty();

		if ($("#quiz_content").is(":animated"))
		{
			console.info('animated!');
		}

		if (opts.itemArray[opts.itemNum].o.zoomSpeedIn > 0)
		{
			opts.animating		= true;
			itemOpts.opacity	= "show";

			$("#quiz_outer").css(
					{
					'top':		opts.itemArray[opts.itemNum].orig.pos.top - 18,
					'left':		opts.itemArray[opts.itemNum].orig.pos.left - 18,
					'height':	opts.itemArray[opts.itemNum].orig.height
					});

			//$("#quiz_content").append($(val)).show();

			$("#quiz_outer").animate(itemOpts, opts.itemArray[opts.itemNum].o.zoomSpeedIn, function()
					{
					opts.animating = false;
					$.fn.quizbox.updateDetails();
					});

		}
		else
		{
			$("#quiz_content").append($(val)).show();
			$("#quiz_outer").css(itemOpts).show();
			$.fn.quizbox.updateDetails();
		}
	}
};



$.fn.quizbox.updateDetails = function() {
	$("#quiz_bg,#quiz_close").show();


	/* =========== */
	/* = Instructions Animations = */
	/* =========== */


	if (opts.itemArray[opts.itemNum].item_type == "instructions") {
		console.log('whatup');
		var hover_count = 0
			var example1 = $('div#example_1', window.frames[0].document);
		var example2 = $('div#example_2', window.frames[0].document);

		$("a#answer1").hover(function()
		{
			hover_count += 1;
			if (hover_count > 1) {
				$('div#example_1').hide();
				$('div#example_2').show();

				example1.hide();
				example2.show();

				console.log('YOO');
			}

		}, 
		function()
		{
		});



		$("a#answer2").hover(function()
		{
			hover_count += 1;
			if (hover_count > 1)
			{
				$('div#example_1').hide();
				$('div#example_2').show();

				example1.hide();
				example2.show();
				console.log('YOO');
			}
		}, function() {
		});
	}
	/* =========== */
	/* = Update Button Display = */
	/* =========== */
	/* Fill in titles for answer keys - redundant! make this more robust before something blows up*/
	if (opts.itemArray[opts.itemNum].item_type == "quiz_item") {
		$('#quiz_title').show();
		$('#quiz_title div#quiz_answers').show();           
		$('#quiz_title div#quiz_intro').hide();  
		$('#quiz_title div#quiz_instructions').hide();
		$('#quiz_title div#quiz_instructions2').hide(); 

		/* TODO change to toggle */
		$('#quiz_answers div#answer1').empty();     
		$('#quiz_answers div#answer2').empty();
		$('#quiz_answers div#answer3').empty();
		$('#quiz_answers div#answer1').html(opts.itemArray[opts.itemNum].answer1);     
		$('#quiz_answers div#answer2').html(opts.itemArray[opts.itemNum].answer2);
		$('#quiz_answers div#answer3').html(opts.itemArray[opts.itemNum].answer3);
		$('#quiz_answers div.arrow').html('<img src="/static/stylesheets/img/pinkarrow.png"/>');

		$.fn.quizbox.startTimer('#timer_bar');
	}else if (opts.itemArray[opts.itemNum].item_type == "intro") {
		/* hide answers and show hidden intro choices */
		$('#quiz_title').show();
		$('#quiz_title div.buttons').hide(); 
		$('#quiz_title div#quiz_intro').show();  
		$('#quiz_intro div#take_quiz').html(opts.itemArray[opts.itemNum].take_quiz);  
		$('#quiz_intro div#choose_quiz').html(opts.itemArray[opts.itemNum].choose_quiz);
	}else if (opts.itemArray[opts.itemNum].item_type == "instructions") {
		$('#quiz_title').show();
		$('#quiz_title div.buttons').hide();   
		$('#quiz_title div#quiz_instructions').show();  
		$('#quiz_instructions div#answer1').html(opts.itemArray[opts.itemNum].answer1);     
		$('#quiz_instructions div#answer2').html(opts.itemArray[opts.itemNum].answer2);
	}else if (opts.itemArray[opts.itemNum].item_type == "instructions2") {
		$('#quiz_title').show();
		$('#quiz_title div.buttons').hide();
		$('#quiz_title div#quiz_instructions2').show();  
		$('#quiz_instructions2 div#answer1').html(opts.itemArray[opts.itemNum].answer1);     
		$('#quiz_instructions2 div#answer2').html(opts.itemArray[opts.itemNum].answer2);
		$.fn.quizbox.startTimer('#timer_bar_instruction');
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

	$(imgPreloader).unbind('load');
	$(document).unbind("keydown");

	$("#quiz_loading,#quiz_title,#quiz_close,#quiz_bg").hide();

	//$("#quiz_nav").empty();

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
				$("#quiz_content").hide(); //.empty();
				$("#quiz_overlay,#quiz_bigIframe").remove();
				opts.animating = false;
				});

	} else {
		$("#quiz_outer").hide();
		$("#quiz_content").hide(); //.empty();
		$("#quiz_overlay,#quiz_bigIframe").fadeOut("fast").remove();
	}
};

$.fn.quizbox.showLoading = function()
{
	clearInterval(loadingTimer);

	var pos = $.fn.quizbox.getViewport();

	$("#quiz_loading").css({'left': ((pos[0] - 40) / 2 + pos[2]), 'top': ((pos[1] - 40) / 2 + pos[3])}).show();
	$("#quiz_loading").bind('click', $.fn.quizbox.close);

	loadingTimer = setInterval($.fn.quizbox.animateLoading, 66);
};

$.fn.quizbox.animateLoading = function(el, o)
{
	if (!$("#quiz_loading").is(':visible'))
	{
		clearInterval(loadingTimer);
		return;
	}

	$("#quiz_loading > div").css('top', (loadingFrame * -40) + 'px');

	loadingFrame = (loadingFrame + 1) % 12;
};

/* =========== */
/* = Create Buttons = */
/* =========== */


$.fn.quizbox.init_old = function() {
	// Make over to templated (static HTML really) AJAX call. --Morgan
	/* Create Answer Buttons */
	/* append timer to iframe */


	/* append score buttons to iframe */


	/* append intro buttons to iframe */
	// This is all really terrible. This should be done in HTML loaded from the server, the use jQuery to replace things like buttons and text
	// There is WAAY to much overhead here.

	// This will be in the HTML very, very soon - James



	/* append instruction buttons to iframe */


	/* initialize automatic countdown...if it reaches zero, changeItem +1 */
	$("#minutes-box").hide();

	/* effect on answer hover */

	$(".answer").hover(function(){
			$(this).css({'font-variant': 'small-caps'});

			},function(){
			$(this).css({'font-variant': 'normal'});
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
	$('#quiz_title').find('a').click(function() {
			submit_answer(this);
			});

	function submit_answer(answer){
		console.log('clicked on link with id:', answer.id);

		//if (answer.id == "#skip") {
		if (answer.id == "skip") {
			var answer_text = "skip_item";
		}else{
			var answer_text = $(answer).text();
		}

		if (opts.itemArray[opts.itemNum].item_type == "quiz_item"){
			var answer_index = opts.itemArray[opts.itemNum].index;
			/* submit using AJAX function doAdd(picked answer, correct answer) */
			doAdd(answer_text, answer_index)
		} /* add doChoose ajax call for choosing quiz */

		if (opts.itemArray[opts.itemNum].item_type == "score"){
			console.log('TODO: Score dialog'); return false;
		}

		if (answer.id == "choose_quiz"){ 
			console.log('changing quizzes'); /* next_quiz(answer.id);  */
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

	var timer =
	{
timeoutId: Number(),
	   timerSelector: String()
	};

	$.fn.quizbox.startTimer = function(timerSelector)
	{
		// Start timer --Morgan
		timer.timerSelector = timerSelector;
		timer.timeoutId = setTimeout(function() {
				// ONE ID PER PAGE! --Morgan
				$(timerSelector).animate(
					{
width:	0
},
{
duration:	8000,
easing:	'linear',
complete:	function()
{
$('#skip').click(); /* not the same as skip - TODO format ajax call for timeout */
$(timerSelector).css('width', '100%');
}
});
				});
}

$.fn.quizbox.stopTimer = function()
{
	clearTimeout(timer.timeoutId);
	$(timer.timerSelector).stop();

	timer =
	{
timeoutId: Number(),
	   timerSelector: String()
	};
}

})(jQuery);
