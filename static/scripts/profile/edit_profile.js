

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
		
		
  $.MultiFile({ 
   afterFileSelect:function(element,value,master){ 
   	console.log('multi!');
   } 
  }); 
  
 
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
 console.log(photo);
 server.SubmitProfileEdits(eval('document.signup.fullname.value'),
 	                          eval('document.signup.email.value'),
	                          eval('document.signup.location.value'), 
	                          eval('document.signup.webpage.value'), 
	                          eval('document.signup.work_status.value'), 
	                          eval('document.signup.aboutme.value'),
	                          photo,
	                          onEditSuccess //-- this would ensure that webpage and email values are valid.
	                          );
/*  Use Loading to Offset Read/Commit Latency
	 $('div.loading').show();
	$('div.main').hide();
$('div.loading').animate({opacity: 1.0}, 500, function(){
onEditSuccess("")
	}); */                        
	                      
}
	


function UploadError() {

// notify the user of the uploading error
console.log('Upload Error!');
	
}


function RefreshImage(img_id){
	
$('div#photo > img').hide();
$('div#photo').append('<img class="new" src="/image/profile/?img_id=' + img_id + '" />');
$('div#photo').data('new_image', img_id);
console.log('image data - ',$('div#photo').data('new_image') );
$('div.cancel').show();
} 



function SetupImageUpload(){
	
	console.log('setting up');
	 $('div#change_img').jsupload({
  // Location of the serverside upload script
  action: '/profiles/picture_upload/',
  // File upload name
  name: 'img',

  // Function that gets called when file upload is starting
  onSubmit: function(filename) {
    //You can do filename validation here
    //and return false to cancel the upload
console.log('sending!');
  },
  // Function that gets called when file upload is completed
  onComplete: function(result){
  	console.log('receiving!');
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
	
	console.log(photo_keys);
	
	var count = jQuery.inArray($('div#photo').data('new_image'), photo_keys) + 1;
	
	if (count >= photo_keys.length) { count = 0; }
	
	console.log(count);
	console.log(photo_keys.length);

	var img_id = photo_keys[count]
	RefreshImage(img_id)
	
	
}
