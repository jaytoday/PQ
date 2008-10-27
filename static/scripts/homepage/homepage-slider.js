// when the DOM is ready...
function proficiency_sliderInit() {
    // need i 
    var $panels = $('.proficiency_container .proficiencies > div');
    var $container = $('.proficiency_container .proficiencies');
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
    var $scroll = $('.proficiency_container .proficiencies_scroll').css('overflow', 'hidden');

    // apply our left + right buttons
    $scroll
        .before('<img class="scrollButtons proficiency_prev" src="/static/stylesheets/img/scroll_left.png" />')
        .after('<img class="scrollButtons proficiency_next" src="/static/stylesheets/img/scroll_right.png" />');


    // go find the navigation link that has this target and select the nav
    function trigger(data) {

    }



    var scrollOptions = {
        target: $scroll, // the element that has the overflow

        // can be a selector which will be relative to the target
        items: $panels,

        // selectors are NOT relative to document, i.e. make sure they're unique
        prev: 'img.proficiency_prev', 
        next: 'img.proficiency_next',

        // allow the scroll effect to run both directions
        axis: 'x',
        
        step: 5,

        onAfter: trigger, // our final callback

        // offset: 0,
        
        exclude: 4,

        // duration of the sliding effect
        duration: 1000,

        // easing - can be used with the easing plugin: 
        // http://gsgd.co.uk/sandbox/jquery/easing/
        easing: 'swing'
    };

    // apply serialScroll to the slider - we chose this plugin because it 
    // supports// the indexed next and previous scroll along with hooking 
    // in to our navigation.
    $('.proficiency_container').serialScroll(scrollOptions);

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
