

$(document).ready(function()
{
	$('div.right_inner > h1').click(function(){ $('.main').fadeOut('slow', function(){ 
		
	$.getScript("/static/scripts/scroll/jquery.scrollTo-min.js");
	$.getScript("/static/scripts/scroll/jquery.localscroll-1.2.5.js");
	$.getScript("/static/scripts/scroll/jquery.serialScroll-1.2.1.js");
	$.getScript("/static/scripts/jquery/jquery.animatedcollapse.js");
	choose_proficiency(); 
		
	});  });
    $('div.p_links').click(function(){ choose_proficiency(); });
	$('input#employer_name').preserveDefaultText('type the name of your business');
	
		
	 $('input#employer_name').freebaseSuggest( {ac_param:{type:'/business/company'}})
				.bind("fb-select", function(e, data) {
					set_employer(data);
				})


	
	
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
