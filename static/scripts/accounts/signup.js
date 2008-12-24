
 

$(function(){
	
//TODO: Check for invalid chars, like $ and <, etc.


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
});



function SubmitName(){
	console.log($('input#nickname').data('availability'));
	
	if ($('input#nickname').val().length < 3) console.log('nickname is too short'); 
	
	
	if($('input#nickname').data('availability') == 'unknown') setTimeout(function(){ SubmitName(); }, 1000);  // still unknown
	
	if($('input#nickname').data('availability') != 'available') { $('#signup_reminder').show(); return false; } //hasn't chosen a valid name yet 
	
	$('div.loading').show();
	$('div.main').hide();
	window.location="/register?nickname=" + $('input#nickname').val();
	
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
