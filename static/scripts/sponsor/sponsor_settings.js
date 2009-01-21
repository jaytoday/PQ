
		$(function () {


$('#quiz_subjects').change(function(){

            $(this).data('subject', $(this).find('option').filter(':selected').text())

        });



						$('div#submit_form div#submit').click(function(){  SubmitSettingsEdit();   });
			
			$('div#submit_form div#cancel').click(function(){
			CancelSettingsEdit();
		});
		


// Take a Quiz link
$('a#preview_quiz').click(function(){ 
	$.getScript("/js/quiz/?autostart=True");
});

		
		});


 function SubmitSettingsEdit() {
// get the different pieces of data, and submit them

// TODO: We can use jQuery.serialize() for fast form serialization

	$.ajax({
		type: "POST", 
		url: '/employer/rpc/post',
		datatype: "json",
		data:
			{
					action: "settings",
					sponsor: this_sponsor, // defined in sponsor_settings.html
					sponsorship_message: $('textarea#sponsor_message').attr('value'),
					quiz_subject: $('#quiz_subjects').data('subject')
			},
		error: function() { },
		success: function(response) { onEditSuccess(response); }
});			


	                      
}
	


function UploadError() {

// TODO: notify the user of the uploading error
console.log('Upload Error!');
	
}


function RefreshImage(img_id){
	
$('div#photo > img').hide();
$('div#photo').append('<img class="new" src="/image/profile/?img_id=' + img_id + '&size=large />');
$('div#photo').data('new_image', img_id);
$('div.cancel').show();
} 








	function onEditSuccess(response){

	if (eval(response) != "OK") { // error message.
		$('div#submit_form').find('#sponsor_form_error').show()
		  .find('a').click(
		  function(){ $('a#contact_dialog').click(); } );
		
		return false; }
			
			
			$('div.loading').show();
	$('div.main').hide();
	window.location=profile_path;
}
function CancelSettingsEdit(){
$('div.loading').show();
	$('div.main').hide();	
window.location=profile_path;
}

function CyclePictures(){

getNextPicture(photo_keys);

}
