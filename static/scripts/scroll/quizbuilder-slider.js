

// when the DOM is ready...
function sliderInit(wrong_answers) {
    
    var $panels = $('.quizbuilder_wrapper .quiz_items > div');

    var $container = $('.quizbuilder_wrapper .quiz_items');

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
    var $scroll = $('.quizbuilder_wrapper .scroller').css('overflow', 'hidden');

    // apply our left + right buttons
    $scroll
        .before('<img class="scrollButtons left" src="/static/stylesheets/img/scroll_left.png" />')
        .after('<img class="scrollButtons right" src="/static/stylesheets/img/scroll_right.png" />');

    // handle nav selection
    function selectNav() {
        $(this)
            .parents('ul:first')
                .find('a')
                    .removeClass('selected')
                .end()
            .end()
            .addClass('selected');
    }

    $('.quizbuilder_wrapper > .item_navigation').find('a').click(selectNav);

    // go find the navigation link that has this target and select the nav
    
    // use: $(container).trigger( 'next' );
    
    function trigger(data) {
    
        	
        var el = $('.item_navigation').find('a[href$="' + data.id + '"]').get(0);
        selectNav.call(el);
        	
    	this_id = data.id - 1;

         if (data.id == 0){ console.log('no more items'); } // -- only if submitting after all items have been edited. 

  
    }

    if (window.location.hash) {
        trigger({ id : window.location.hash.substr(1) });
    } else {
        $('.item_navigation a:first').click();
    }

    // offset is used to move to *exactly* the right place, since I'm using
    // padding on my example, I need to subtract the amount of padding to
    // the offset.  Try removing this to get a good idea of the effect
    var offset = parseInt((horizontal ? 
        $container.css('paddingTop') : 
        $container.css('paddingLeft')) 
        || 0) * -1;
                     

    var scrollOptions = {
        target: $scroll, // the element that has the overflow

        // can be a selector which will be relative to the target
        items: $panels,

        navigation: '.item_navigation a',
        
        cycle: 'false',
        lazy: 'true', // for dynamic content

        // selectors are NOT relative to document, i.e. make sure they're unique
        prev: 'img.left', 
        next: 'input[@name="submit_item"]',

        // allow the scroll effect to run both directions
        axis: 'x',

        onAfter: trigger, // our final callback

        offset: offset,

        // duration of the sliding effect
        duration: 500,

        // easing - can be used with the easing plugin: 
        // http://gsgd.co.uk/sandbox/jquery/easing/
        //easing: 'swing'
    };

    // apply serialScroll to the slider - we chose this plugin because it 
    // supports// the indexed next and previous scroll along with hooking 
    // in to our navigation.
    $('.quizbuilder_wrapper').serialScroll(scrollOptions);

    // now apply localScroll to hook any other arbitrary links to trigger 
    // the effect
    $.localScroll(scrollOptions);

    // finally, if the URL has a hash, move the slider in to position, 
    // setting the duration to 1 because I don't want it to scroll in the
    // very first page load.  We don't always need this, but it ensures
    // the positioning is absolutely spot on when the pages loads.
    scrollOptions.duration = 1;
    $.localScroll.hash(scrollOptions);

 
}
