
/*
 * 
 *  Load Answers
 * 
 */

function loadAnswers(item) {
	console.log('loading answers...');
	var these_answers = $('div.answer_candidates', item);
	var answers_container = these_answers.parents('.answers_container:first');
	if (these_answers.data('busy') == true) return false;
	answers_container.data('busy', true)
	                 .find('div.answers_scroll').hide('fast').end()
	                 .find('div.loading').show('fast');
	
	    	$.ajax({
                    
                    type: "POST",
                    url:  "/quizeditor/rpc/post",
                    data:
                    {
                            action: "LoadAnswers",
                            correct_answer: $('span.correct', item).text(),
                            item_text: $('div.quiz_item.content', item).text()
                    },
                    success: function(response)
                    {  
                    	
                    	answers_container.html(response).data('busy', false);
                       
                       item.trigger("initiate");
                       answerSliderInit(these_answers, answers_container);	
                       }
               });
	
	
	
	
	
}


/*
 * 
 * Answer Slider
 * 
 */

function answerSliderInit(wrong_answers, answers_container) {
	
	 

    var $panels = $(wrong_answers).find('div.ac_wrapper');
    var scroll_width = 160 * $panels.length; wrong_answers.css('width', scroll_width);  
    var $container = answers_container;
    var $index = $container.attr('id');

console.log(wrong_answers, $panels,  $container);

    // if false, we'll float all the panels left and fix the width 
    // of the container
    var horizontal = true;

    // float the panels left if we're going horizontal
    if (horizontal) {
        $panels.css({
            'float' : 'left',
            'position' : 'relative' // IE fix to ensure overflow is hidden
        });

    }

    // collect the scroll object, at the same time apply the hidden overflow
    // to remove the default scrollbars that will appear
    var $scroll = $('.answers_scroll', $container).css('overflow', 'hidden');

    // apply our left + right buttons
    $scroll
        .before('<img class="scrollButtons answer_prev answer_prev' + $index + '" src="/static/stylesheets/img/utils/scroll_left.png" />')
        .after('<img class="scrollButtons answer_next answer_next' + $index + '" src="/static/stylesheets/img/utils/scroll_right.png" />');



   // $('#slider .navigation').find('a').click(selectNav);

    // go find the navigation link that has this target and select the nav
    function trigger(data) {
 
    }

console.log('prev ', $('img.answer_prev' + $index));

    var scrollOptions = {
        target: $scroll, // the element that has the overflow

        // can be a selector which will be relative to the target
        items: $panels,

        // selectors are NOT relative to document, i.e. make sure they're unique
        prev: 'img.answer_prev' + $index, 
        next: 'img.answer_next' + $index,

        // allow the scroll effect to run both directions
        axis: 'x',
        
        step: 5,
        
        exclude: 4,

        onAfter: trigger, // our final callback

        // offset: 0,

        // duration of the sliding effect
        duration: 500,

        // easing - can be used with the easing plugin: 
        // http://gsgd.co.uk/sandbox/jquery/easing/
        easing: 'swing'
    };

    // apply serialScroll to the slider - we chose this plugin because it 
    // supports// the indexed next and previous scroll along with hooking 
    // in to our navigation.
    $container.serialScroll(scrollOptions);

    // now apply localScroll to hook any other arbitrary links to trigger 
    // the effect
  //  $.localScroll(scrollOptions);

    // finally, if the URL has a hash, move the slider in to position, 
    // setting the duration to 1 because I don't want it to scroll in the
    // very first page load.  We don't always need this, but it ensures
    // the positioning is absolutely spot on when the pages loads.
   // scrollOptions.duration = 1;
   // $.localScroll.hash(scrollOptions);

}
