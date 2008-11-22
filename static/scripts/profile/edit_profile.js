

		$(function () {

			// Example 1
			$('form.signup input:text').magicpreview('mp_');

			// Example 2
			$('form.signup :text').magicpreview('p_');
			$('form.signup textarea').magicpreview('p_');
			$('form.signup  select').magicpreview('p_');


			$('form.photopreview select').magicpreview('img_', {
				'child': 'img',
				'change': 'src',
				'formatValue': function (value) { 
					return '/magicpreview/images/' + value + '.jpg'
				}
			});
			
						$('div#submit_profile').click(function(){
				
	//There should be an RPC call here. 
	SubmitProfileEdits();
			});
			
			$('div.form_cancel').click(function(){
			onEditCancel()
		});
			
		
		});

// Setup RPC methods
var server = {};
var item_count = 0;

InstallFunction(server, 'SubmitProfileEdits', 'accounts');

 function SubmitProfileEdits() {
// get the different pieces of data, and submit them
  
 var aboutme = $('textarea.aboutme').attr('value');
 console.log(eval('document.signup.aboutme.value'));
 server.SubmitProfileEdits(eval('document.signup.fullname.value'),
 	                          eval('document.signup.email.value'),
	                          eval('document.signup.location.value'), 
	                          eval('document.signup.webpage.value'), 
	                          eval('document.signup.work_status.value'), 
	                          eval('document.signup.aboutme.value'),
	                          onEditSuccess);

	                          
	                      
}
	
