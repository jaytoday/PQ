$(document).ready(function()
{
	
	// Show messages based on whether user has awards and sponsorships
	var has_awards = "False";	
{% for award in user.awards %}
if ("{{ forloop.first }}") has_awards = "True";
 if (!$('.{{ forloop.counter }}_has_subject_image')) $('li#{{ forloop.counter }}_default_subject_image').show(); {# show default image, no slider #}
 else  $('#award_{{ forloop.counter }}').s3Slider({ timeOut: 3300 });  {# load slider for this award#} 
{% endfor %}  

{% if not user.is_sponsor %}
if (has_awards != "True") $('#main_nav').find('a[href="#report_card"]').click();
{% endif %}

if ($('div.is_sponsor').length == 0) $('div#no_sponsorship_note').show();


if (($('div.award_img').length == 0)) $('div#no_award_note').show();


 });
 
