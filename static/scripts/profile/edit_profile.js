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


		$(function () {

  
			// Example 1
			$('form.signup input:text').magicpreview('mp_');

			// Example 2
			$('form.signup :text').magicpreview('p_');
			$('form.signup textarea').magicpreview('p_');
			$('form.signup  select').magicpreview('p_');


		/*	$('form.photopreview select').magicpreview('img_', {
				'child': 'img',
				'change': 'src',
				'formatValue': function (value) { 
					return '/magicpreview/images/' + value + '.jpg'
				}
			}); */
			
						$('div#submit_profile').click(function(){
				
	SubmitProfileEdits();
			});
			
			$('div.form_cancel').click(function(){
			onEditCancel()
		});
		
	$('div#cycle_img').click(function(){
			CyclePictures();
		});
		
		/*
  $.MultiFile({ 
   afterFileSelect:function(element,value,master){ 
   	console.log('multi!');
   } 
  }); 
  * */
  
 
 SetupImageUpload();
		
   //start off with no new image data
   $('div#photo').data('new_image', '');
    $('div.cancel').hide();
		
		
		
		});

// Setup RPC methods
var server = {};
var item_count = 0;

InstallFunction(server, 'SubmitProfileEdits', 'accounts');
InstallPostFunction(server, 'SubmitPicture', 'profiles');

 function SubmitProfileEdits() {
// get the different pieces of data, and submit them
  
 var aboutme = $('textarea.aboutme').attr('value');
 var photo = $('div#photo').data('new_image');
 server.SubmitProfileEdits(eval('document.signup.fullname.value'),
 	                          eval('document.signup.email.value'),
	                          eval('document.signup.location.value'), 
	                          eval('document.signup.webpage.value'), 
	                          eval('document.signup.work_status.value'), 
	                          eval('document.signup.aboutme.value'),
	                          photo,
	                          onEditSuccess //-- this would ensure that webpage and email values are valid.
	                          );
                      
	                      
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



function SetupImageUpload(){
	
	 $('div#change_img').jsupload({
  // Location of the serverside upload script
  action: '/profiles/picture_upload/',
  // File upload name
  name: 'img',

  // Function that gets called when file upload is starting
  onSubmit: function(filename) {
    //You can do filename validation here
    //and return false to cancel the upload
  },
  // Function that gets called when file upload is completed
  onComplete: function(result){
    //Result is what we got from server script
    if (result == "error"){ UploadError(); return; }
    RefreshImage(result);
  }
  });
  
}

function CancelPhotoUpload(){
	$('div#photo > img.new').hide();
	$('div#photo > img.old').show();
	$('div#photo').data('new_image', '');
	$('div.cancel').hide();
}



function getNextPicture(photo_keys){
	
	
	var count = jQuery.inArray($('div#photo').data('new_image'), photo_keys) + 1;
	
	if (count >= photo_keys.length) { count = 0; }
	

	var img_id = photo_keys[count]
	RefreshImage(img_id)
	
	
}


	function onEditSuccess(response){
			//TODO make sure that response has no errors
	window.location=profile_path;
}
function onEditCancel(){
window.location=profile_path;
}

function CyclePictures(){

getNextPicture(photo_keys);

}
