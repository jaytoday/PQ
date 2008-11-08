

$(document).ready(function()
{
	
	$('div#right_corner').hide();
	
	$('div#take_quiz').hover(function(){ 
		
		$(this).css({"background-color":"#CCCCCC","border-color":"#CCCCCC"});
		$(this).find('h1').css({"color":"#000080"});
	},function(){
	$(this).css({"background-color":"#DDDDDD","border-color":"#DDDDDD"});
	$(this).find('h1').css({"color":"#000040"});
	});
	
	$('div#take_quiz').click(function(){ 
		
	$.getScript("/static/scripts/scroll/jquery.scrollTo-min.js");
	$.getScript("/static/scripts/scroll/jquery.localscroll-1.2.5.js");
	$.getScript("/static/scripts/scroll/jquery.serialScroll-1.2.1.js");
	$.getScript("/static/scripts/jquery/jquery.animatedcollapse.js");
	
	$('.main').fadeOut('slow', function(){ 
	choose_proficiency(); 
		
	});  });
    $('div.p_links').click(function(){ choose_proficiency(); });
	$('input#employer_name').preserveDefaultText("what's the name of your business?");
	
		
	 $('input#employer_name').freebaseSuggest( {ac_param:{type:'/business/company'}})
				.bind("fb-select", function(e, data) { 
					
					window.location = "/preview/employer/profile/";
					return;
						$.getScript("/static/scripts/jquery/jquery.ui.js");
	$.getScript("/static/scripts/profile/tagcloud.js");
					$('.main').fadeOut(1000, function(){ 
	set_employer(data); 
		
	});  })


	
	
	// hover and focus fx        
	$('input').focus(function()
	{
		$(this).addClass('focus');
	})
	.blur(function()
	{
		$(this).removeClass('focus');
	});

	MottoAnimation();	
	
	
});

     



function MottoAnimation()
{
	if ($('#smart').length < 1) { return false; }
	var ml = Number($('#smart').css('marginLeft').replace(/p[xt]/,''));
	ml = (ml == 25) ? 238 : 25;

	setTimeout(function()
	{
		$('#smart').animate({
			opacity: .5
		},
		{
			complete: function()
			{
				$('#smart').animate({
					marginLeft:	ml
				},
				{
					complete: function()
					{
						$('#smart').animate({
							opacity: 1
						});

						setTimeout(MottoAnimation,1800);
					}
				});
			}
		});
	},1400);
}


function set_employer(data){
	

	
	console.log(data);
	
$('.main_wrapper').load("/preview/employer/profile .main_wrapper", function(){
	
		$.getScript("/static/scripts/profile/profile.js");		
			});

	$('.main').fadeIn(2000);
	
	

}


function choose_proficiency(data){	
	/*
	$.getScript("/static/scripts/scroll/jquery.scrollTo-min.js");
	$.getScript("/static/scripts/scroll/jquery.localscroll-1.2.5.js");
	$.getScript("/static/scripts/scroll/jquery.serialScroll-1.2.1.js");
	$.getScript("/static/scripts/jquery/jquery.animatedcollapse.js");
	
	*/

		$('.main_wrapper').load("/preview/proficiency .main_wrapper", function(){
			
	$.getScript("/static/scripts/homepage/proficiency-slider.js");		
	$.getScript("/static/scripts/homepage/proficiency.js");
	$('div.proficiency_container').show('slow');
	// $('.proficiency_container').find('div#biofuels').trigger('click'); -- get this working for shortcuts from homepage
			});

	$('.main').fadeIn(2000);
}
