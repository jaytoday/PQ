
 

$(function(){
	
//TODO: Check for invalid chars, like $ and <, etc.


$('input#nickname').preserveDefaultText('your name');
$('input#email_address').preserveDefaultText('your email address');


$('input#nickname').keydown(function(){ $('input#nickname').data('availability', 'unknown') }); // just for sneaky fast people

$('input#nickname').typeWatch( 
 {
    callback:function(){ NicknameCheck(); },
    wait:300,          // milliseconds
    highlight:true
}
);


$('div#submit_nickname').click(function(){ SubmitName(); });

NicknameCheck();


// flyer
console.log($('#flyer a'));
$('#flyer a').css('top', '50%').show().animate({left: "100%"},17000);

});



function SubmitName(){
	console.log($('input#nickname').data('availability'));
	
	if ($('input#nickname').val().length < 3) console.log('nickname is too short'); //Todo error
	
	$('div#signup_reminder').empty();
	
	if($('input#nickname').data('availability') == 'unknown') setTimeout(function(){ SubmitName(); }, 1000);  // still unknown
	
	if($('input#nickname').data('availability') != 'available') { $('#signup_reminder').text("The nickname you've entered isn't available.").show(); $('input#nickname').addClass('invalid'); return false; } //hasn't chosen a valid name yet 
	
	if($('input#email_address').val().indexOf('@') == -1) { $('#signup_reminder').text('Enter a valid e-mail address so you can recover your password.').show(); $('input#email_address').addClass('invalid').focus(); return false; } //hasn't chosen a valid name yet 
	
	$('div.loading').show();
	$('div.main').hide();
	window.location="/register?nickname=" + $('input#nickname').val() + "&email=" + $('input#email_address').val();
	
}

function NicknameCheck(){
	
	
	var nickname = $('input#nickname').val();
	
$.ajax({
		url: http_host + '/accounts/rpc?',
        data:
			{
					action: "nickname_check",
					arg0: '"' + nickname + '"'
			},
		success: function(response) { 
			
			var response =  eval(response);
			
			console.log($('div#notice > span#' + response))
			
			$('div#notice > span').hide();
			$('div#notice > span#' + response).show();
			
			$('input#nickname').data('availability', response) 
			
			} 
		// available or not 

});


}
