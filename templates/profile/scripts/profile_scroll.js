

$.getScript("/static/scripts/scroll/jquery.scrollTo-min.js");
$.getScript("/static/scripts/scroll/jquery.localscroll-1.2.5.js");
$.getScript("/static/scripts/scroll/jquery.serialScroll-1.2.1.js");


$(function()
{


{% if scroll.awards %}
$('#award_scroll_nav').show();
$.getScript("/static/scripts/profile/award_slider.js");
{% endif %}



{% if scroll.sponsors %}
$('#sponsor_scroll_nav').show();
$.getScript("/static/scripts/profile/sponsor_slider.js");
{% endif %}


 });
 







