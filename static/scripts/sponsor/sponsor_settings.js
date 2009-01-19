
		$(function () {


$('#quiz_subjects').change(function(){

            $(this).data('subject', $(this).find('option').filter(':selected').text())

        });



						$('div#submit_form div#submit').click(function(){  SubmitSettingsEdit();   });
			
			$('div#submit_form div#cancel').click(function(){
			CancelSettingsEdit();
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
		success: function(response) { onEditSuccess(response); }
});			


	                      
}
	


function UploadError() {

// notify the user of the uploading error
console.log('Upload Error!');
	
}


function RefreshImage(img_id){
	
$('div#photo > img').hide();
$('div#photo').append('<img class="new" src="/image/profile/?img_id=' + img_id + '&size=large />');
$('div#photo').data('new_image', img_id);
$('div.cancel').show();
} 








	function onEditSuccess(response){

	if (eval(response) != "OK") return false;
			//TODO error message.
			
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
