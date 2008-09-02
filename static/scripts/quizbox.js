/*
* Quizbox Library 

*/

(function($) {
var opts = {}, 
imgPreloader = new Image, imgTypes = ['png', 'jpg', 'jpeg', 'gif'], 
loadingTimer, loadingFrame = 1;

$.fn.quizbox = function(settings) {
opts.settings = $.extend({}, $.fn.quizbox.defaults, settings);

$.fn.quizbox.init();

return this.each(function() {
    var $this = $(this);
    var o = $.metadata ? $.extend({}, opts.settings, $this.metadata()) : opts.settings;

    $this.unbind('click').click(function() {
        $.fn.quizbox.start(this, o); return false;
    });
});
};

$.fn.quizbox.start = function(el, o) {
if (opts.animating) return false;

doInit(); /* DELETES EXISTING DATASTORE ENTRIES - JUST FOR DEMO */



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

} else {
    if (!el.rel || el.rel == '') {
        var item = {url: el.href, title: el.title, o: o};

        if (o.zoomSpeedIn > 0 || o.zoomSpeedOut > 0) {
            var c = $(el).children("img:first").length ? $(el).children("img:first") : $(el);
            item.orig = {'width': c.width(), 'height': c.height(), 'pos': $.fn.quizbox.getPosition(c)}
        }

        opts.itemArray.push(item);

    } else {
        var arr	= $("a[@rel=" + el.rel + "]").get();

        for (var i = 0; i < arr.length; i++) {
            var tmp		= $.metadata ? $.extend({}, o, $(arr[i]).metadata()) : o;
            var item	= {url: arr[i].href, title: arr[i].title, o: tmp};

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

$.fn.quizbox.changeItem = function(n) {
$.fn.quizbox.showLoading();

opts.itemNum = n;

$("#quiz_nav").empty();
$("#quiz_outer").stop();
$("#quiz_title").hide();
$(document).unbind("keydown");

imgRegExp = imgTypes.join('|');
imgRegExp = new RegExp('\.' + imgRegExp + '$', 'i');

var url = opts.itemArray[n].url;

if (url.match(/#/)) {
    var target = window.location.href.split('#')[0]; target = url.replace(target,'');

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
    $.fn.quizbox.showItem('<iframe id="quiz_frame" scrolling="no" onload="$.fn.quizbox.showIframe()" name="quiz_iframe' + Math.round(Math.random()*1000) + '" frameborder="0" hspace="0" src="' + url + '"></iframe>');
}
};

$.fn.quizbox.showIframe = function() {
$("#quiz_loading").hide();
$("#quiz_frame").show();

   /* preview answer in iframe */

var blankspan = $('.blank', window.frames[0].document);
            $('.answer').hover(function()
            
            /* if id is skip, don't do this */
            
            
            
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
                
                
};



          
                
                
                
                

$.fn.quizbox.showItem = function(val) {
$.fn.quizbox.preloadNeighborImages();

var viewportPos	= $.fn.quizbox.getViewport();
var itemSize	= $.fn.quizbox.getMaxSize(viewportPos[0] - 50, viewportPos[1] - 100, opts.itemArray[opts.itemNum].o.frameWidth, opts.itemArray[opts.itemNum].o.frameHeight);

var itemLeft	= viewportPos[2] + Math.round((viewportPos[0] - itemSize[0]) / 2) - 20;
var itemTop		= viewportPos[3] + Math.round((viewportPos[1] - itemSize[1]) / 2) - 40;


 /* redundant - TODO refactor */

if (opts.itemArray[opts.itemNum].item_type == "score") {

    /* score card */
    
var itemOpts = {
    'left':		143 + 'px', 
    'top':		0 + 'px', 
    'width':	332 + 'px', 
    'height':	405 + 'px'	
};



}else if (opts.itemArray[opts.itemNum].item_type == "intro"){
    
     /* intro */
    
    
var itemOpts = {
    'left':		143 + 'px', 
    'top':		0 + 'px', 
    'width':	332 + 'px', 
    'height':	405 + 'px'	
};


}else{   
    
    /* during quiz */
    
    
var itemOpts = {
    'left':		73 + 'px', 
    'top':		10 + 'px', 
    'width':	512 + 'px', 
    'height':	373 + 'px'	
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
        console.info('animated!');
    }

    if (opts.itemArray[opts.itemNum].o.zoomSpeedIn > 0) {
        opts.animating		= true;
        itemOpts.opacity	= "show";

        $("#quiz_outer").css({
            'top':		opts.itemArray[opts.itemNum].orig.pos.top - 18,
            'left':		opts.itemArray[opts.itemNum].orig.pos.left - 18,
            'height':	opts.itemArray[opts.itemNum].orig.height,
            'width':	opts.itemArray[opts.itemNum].orig.width
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

/* Fill in titles for answer keys - redundant! make this more robust before something blows up*/

 
    if (opts.itemArray[opts.itemNum].item_type == "quiz_item") {
    $('#quiz_title div#answer1').empty();     
    $('#quiz_title div#answer2').empty();
    $('#quiz_title div#answer3').empty();
    
    $('#quiz_title div#answer1').html(opts.itemArray[opts.itemNum].answer1);      /*(opts.itemArray[opts.itemNum].title);*/
    $('#quiz_title div#answer2').html(opts.itemArray[opts.itemNum].answer2);
    $('#quiz_title div#answer3').html(opts.itemArray[opts.itemNum].answer3);
    $('#quiz_title').show();
    $('#quiz_title div.arrow').html('<img src="/static/stylesheets/img/pinkarrow.png"/>');
    }else if (opts.itemArray[opts.itemNum].item_type == "intro"){
            $('#quiz_title div#take_quiz').html(opts.itemArray[opts.itemNum].take_quiz);     
    $('#quiz_title div#choose_quiz').html(opts.itemArray[opts.itemNum].choose_quiz);
        
}else{
$('#quiz_title').empty();
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
        $("#quiz_content").hide().empty();
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




$.fn.quizbox.init = function() {
    
    
    /* Create Answer Buttons */
if (!$('#quiz_wrap').length) {
    $('<div id="quiz_wrap"><div id="quiz_loading"><div></div></div><div id="quiz_outer"><div id="quiz_inner"><div id="quiz_nav"></div><div id="quiz_close"></div><div id="quiz_content"></div><div id="quiz_title"></div></div><div id="minutes-boxNOTYET"><div id="minutes-countNOTYET"> </div><div id="minutes-outerNOTYET"> <div id="minutes-innerNOTYET"> </div> </div></div></div></div>').appendTo("body");
    $('<div id="quiz_bg"><div class="quiz_bg quiz_bg_n"></div><div class="quiz_bg quiz_bg_ne"></div><div class="quiz_bg quiz_bg_e"></div><div class="quiz_bg quiz_bg_se"></div><div class="quiz_bg quiz_bg_s"></div><div class="quiz_bg quiz_bg_sw"></div><div class="quiz_bg quiz_bg_w"></div><div class="quiz_bg quiz_bg_nw"></div></div>').prependTo("#quiz_inner");
      /* append timer to iframe */
    $('<div class="timer_wrapper"><!--timer TODO --></div>').appendTo('#quiz_title');
   

    
    /* append quiz items to iframe */
    $('<a id="answer1" onmouseover="" class="answer" href="javascript:;"><table cellspacing="0" cellpadding="0" border="0" ><tr> <td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer1"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_title');
     $('<a id="answer2" class="answer" href="javascript:;"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer2"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_title');
      $('<a id="answer3" class="answer" href="javascript:;"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_blue_left"></td><td id="quiz_blue_main"><div class="answertext" id="answer3"></div></td><td id="quiz_blue_right"></td></tr></table></a>').appendTo('#quiz_title');
     $('<a id="skip" class="answer" href="javascript:;"><table cellspacing="0" cellpadding="0" border="0" ><tr><td id="quiz_pink_left"></td><td id="quiz_pink_main"><div class="arrow"><img src="/static/stylesheets/img/pinkarrow.png" /></div><div class="skipitem" id="skiptext">Skip</div></td><td id="quiz_pink_right"></td></tr></table></a>').appendTo('#quiz_title');
     
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

     
     
     /* submit answers and proceed to next question */
     
        $('#answer1').click(function(){ submit_answer('#answer1'); });
        $('#answer2').click(function(){ submit_answer('#answer2'); });
        $('#answer3').click(function(){ submit_answer('#answer3'); });
        $('#skip').click(function(){ submit_answer('#skip'); });
    
    
function submit_answer(answer){

if (answer == "#skip") {
var answer_text = "skip_item";
}else{
var answer_text = $(answer).text();
}


 if (opts.itemArray[opts.itemNum].item_type == "quiz_item"){
var answer_index = opts.itemArray[opts.itemNum].index;

/* submit using AJAX function doAdd(picked answer, correct answer) */

doAdd(answer_text, answer_index)


} /* add doChoose ajax call for choosing quiz */

/* proceed to next item */ $.fn.quizbox.changeItem(opts.itemNum + 1); return false;


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

$.fn.quizbox.defaults = {
hideOnContentClick:	false,
zoomSpeedIn:		500,
zoomSpeedOut:		500,
frameWidth:			600,
frameHeight:		410,
overlayShow:		false,
overlayOpacity:		0.4,
itemLoadCallback:	null
};
})(jQuery);








