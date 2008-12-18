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
	
	window.location='/preview/proficiency';
	return; 
	// ajax occasionally doesn't work. 	
	$.getScript("/static/scripts/scroll/jquery.scrollTo-min.js");
	$.getScript("/static/scripts/scroll/jquery.localscroll-1.2.5.js");
	$.getScript("/static/scripts/scroll/jquery.serialScroll-1.2.1.js");
	$.getScript("/static/scripts/jquery/jquery.animatedcollapse.js");
	
	$('.main').fadeOut(500, function(){ 
	choose_proficiency(); 
		
	});  });
    //$('div.p_links').click(function(){ choose_proficiency(); });
	$('input#employer_name').preserveDefaultText("what's the name of your business?");
	
		
	 $('input#employer_name').freebaseSuggest( {ac_param:{type:'/business/company'}})
				.bind("fb-select", function(e, data) { 
					
					window.location = "/preview/employer/profile/";
					return;
						$.getScript("/static/scripts/jquery/jquery.ui.js");
	$.getScript("/static/scripts/profile/tagcloud.js");
					$('.main').fadeOut(500, function(){ 
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
	ml = (ml == 25) ? 318 : 25;

	setTimeout(function()
	{
		$('#smart').animate({
			opacity: 0.5
		},
		{
			complete: function()
			{

				$('#smart').animate({
					marginLeft:	100
				},
				{
					complete: function()
					{
						
					var text = $('#smart').text();
					if (ml == 25){$('#smart').text("show")}
					else {$('#smart').text("know")}		
						
			$('#smart').animate({
					marginLeft:	ml
				});
						
						$('#smart').animate({
							opacity: 1
						});

						setTimeout(MottoAnimation,1800);
					}
				});
			}
		});
	},900);
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
	
	$('div.proficiency_container').hide({ complete:function(){ $(this).animate({opacity: 1}).show();  }}); 
			
	$.getScript("/static/scripts/homepage/proficiency-slider.js");		
	$.getScript("/static/scripts/homepage/proficiency.js");
	
	// $('.proficiency_container').find('div#biofuels').trigger('click'); -- get this working for shortcuts from homepage
			});

	
	
}

