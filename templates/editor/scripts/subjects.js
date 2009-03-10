 {% include "../../../static/scripts/utils/s3slider.js" %}
 
{% include "../../../static/scripts/jquery/jquery.jsupload.0.1.min.js" %}

SLIDER_TIMEOUT = 5000;
DEFAULT_NEW_SUBJECT_TEXT = "Subject Name";
DEFAULT_LINK_TITLE = "Link Description"
DEFAULT_LINK_URL = "http://"
DEFAULT_VIDEO_URL = "http://youtube.com/"		
		
		$(function () {

       		

/*
 * 
 *  Initiate Subject
 * 
 */
 
 $('div.subject').each(function(){ $(this).bind("initiate", function() {

 
 	var this_subject = $(this);
 	if (this_subject.data('triggered') == true) return false;
 	this_subject.data('triggered', true);
 	this_subject.name = this_subject.find('div.top_level').attr('id');

 	 
/* Edit Description (re-use when possible) */
$('button.edit', this_subject).click(function(){
    var this_blurb = $(this).parent().parent().find('div.blurb_text'); 
    var blurb_text = this_blurb.html();
    this_blurb.hide().parent().find('textarea').val(blurb_text).show().focus().keyup()
    .end().find('button.edit').hide().end().find('button.save').show(); 
       });
       
       $('button.save', this_subject).click(function(){ 
           var this_textarea = $(this).parent().parent().find('textarea'); 
           var blurb_text = this_textarea.val();
           // save text via ajax call
           SaveBlurb(blurb_text);
           this_textarea.hide().parent().find('div.limit').hide().end()
                                        .find('div.blurb_text').html(blurb_text).show()
           .end().find('button.save').hide().end().find('button.edit').show(); 
              });
              
$('div.blurb_text', this_subject).bind('dblclick', function() { $(this).parent().find('button.edit').click(); })

	// textarea character count for aboutme section
	 	this_subject.find('textarea.description').keyup(function(){
	 	    var limit_id = $(this).parent().find('.limit').show().attr('id');
	limitChars($(this).attr('id'), 450, limit_id);
});
/* End Description */



/* Edit Links */ 
	
// Add Link	
$('button.add_link', this_subject).click(function(){
var add_button = $(this).hide();
var edit_div = $(this).parent().find('div.new_link');
var link_title_input = edit_div.find('input.title').val(DEFAULT_LINK_TITLE).preserveDefaultText(DEFAULT_LINK_TITLE);
var link_url_input = edit_div.find('input.url').val(DEFAULT_LINK_URL).focus();
	
	// Save New Link
	edit_div.show().find('button.save_link').click(function(){
		var link_url = link_url_input.val();
		var link_title = link_title_input.val();		
		AddLink(link_url, link_title, this_subject);		
		edit_div.hide(); 
		add_button.show();		
		}); 

});

this_subject.bind("initiate_links", function(){	
// Remove Link
$('.links_container', this_subject).find('button.remove').click(function(){
var check = confirm("Delete this link?");if (check) { RemoveLink($(this).attr('id'), this_subject);	}		
});

}); this_subject.trigger("initiate_links");


 /* End Links */      


/* Edit Links */ 
	
// Change Video
$('button.change_playlist', this_subject).click(function(){
	var change_button = $(this); change_button.hide();
var edit_div = $(this).parent().find('div.change_playlist'); edit_div.show();
edit_div.find('button').show();
var change_video_input = edit_div.find('input');
edit_div.find('button').click(function(){ edit_div.hide(); change_button.show(); ChangeVideo(change_video_input.val(), this_subject); });	

});

var subject_images = this_subject.find('div.subject_images');

// Upload New Image
$('.upload_picture', this_subject).find('button').jsupload({
    // Location of the serverside upload script
    action: '/editor/rpc/post/subject_img/' + this_subject.name,
    // File upload name
    name: 'subject_img',
    // Function that gets called when file upload is starting
    onSubmit: function(filename) {
      //You can do filename validation here
      //and return false to cancel the upload
    subject_images.find('div').hide().end().find('div.mini_loading').show('fast');
      
    },
    // Function that gets called when file upload is completed
    onComplete: function(response){
      //Result is what we got from server script
      if (response == "error"){ console.log('error uploading image!'); return; }
     subject_images.html(response); this_subject.trigger("initiate_images");  }
    }); 


// Initiate Images - Delete Picture and events with subject frame
this_subject.bind("initiate_images", function() {
this_subject.delete_pictures = this_subject.find('div.delete_pictures > div').click(function(){	
	var this_img = $(this);
	var confirm_delete = confirm("Are you sure you want to delete this image?");	
	if (confirm_delete) { DeleteSubjectImage(this_img, this_subject); }
	});
	
// Initiate Subject Frame
var this_frame = $('.subject_frame', this_subject);
if (this_frame.find('li').length > 1) { $(this).find('li:first').remove();  }
this_frame.s3Slider({ timeOut: SLIDER_TIMEOUT });


}).trigger("initiate_images");




$('ul.subject_nav', this_subject).tabs();

$('div.footer', this_subject).find('button.save').hide();

SetupAdminRights(this_subject);



$('.hide', this_subject).hide();


}); }); // end subject initiate




/*
 * 
 *   setup thumbnails
 * 
 */

$('div#subject_thumb_container > div').each(function(n){
    var this_subject = $('#' + $(this).attr('id'), 'div#subject_frame_container');
    
    
	$(this).click(function(){
		console.log('clicked thumb');
		console.log(this_subject);

      $('h2#subject_selection').text( $(this).text());
      $('div#subject_thumb_container > div').removeClass('selected');
      $(this).addClass('selected'); 
      $('div.subject').hide(); this_subject.show();
      this_subject.trigger("initiate");  });
  	
	// remove default image if there are custom images (if we will never have subjects without pictures, this isn't necessary)
	if ($(this).find('li').length > 1) { $(this).find('li:first').remove();  }

});


$('div:first' ,'div#subject_thumb_container').click(); // Open first subject


// Create New Subject

//create_new_subject
$('button.create_new_subject').click(function(){ CreateNewSubject(); });

		
		}); //end onReady




	
	


function AjaxError() {
console.log('ajax error!');
return;
// TODO...
$('div.loading').hide(); $('div.main').show(); 
		$('.form_error').show()
		  .find('a').click(
		  function(){ $('a#contact_dialog').click(); } );
return false;
}

 








	function onEditSuccess(response){

	if (eval(response) != "OK") { // error message.
		return AjaxError(); }
	
	//window.location=profile_path;
}
function CancelSettingsEdit(){
$('div.main').hide();$('div.loading').show();	
//window.location=profile_path;
}



function limitChars(textid, limit, infodiv)
{
	var text = $('#'+textid).val();	
	var textlength = text.length;
	if(textlength > limit)
	{
		//$('#' + infodiv).html("You've reached the "+limit+" limit ");
		$('#'+textid).val(text.substr(0,limit));
		return false;
	}
	else
	{
		$('#' + infodiv).html((limit - textlength) +' characters left');
		return true;
	}
}


function SaveBlurb(blurb_text)
{


	$.ajax({
		type: "POST", 
		url: '/editor/rpc/post',
		datatype: "json",
		data:
			{
					action: "subject_blurb",
					subject_name: this_subject.name, 
					new_blurb: blurb_text
			},
		error: function() { AjaxError(); },
		success: function(response) {  }
	});  
}


function AddLink(link_url, link_title, this_subject)
{
var links_container = this_subject.find('.links_container');
if (links_container.data('busy') == true) return false;
links_container.data('busy', true);
links_container.find('li').hide().end().find('.mini_loading').show();

	$.ajax({
		type: "POST", 
		url: '/editor/rpc/post',
		datatype: "json",
		data:
			{
					action: "add_link",
					subject_name: this_subject.name, 
					link_url: link_url,
					link_title: link_title
			},
		error: function() { links_container.html("Error Adding Link"); },
		success: function(response) { 
			if (response == "error") return alert("Error adding link");
			links_container.html(response);  },
		complete: function(data) { links_container.data('busy', false); this_subject.trigger("initiate_links"); }
	});  
}


function RemoveLink(link_key, this_subject)
{

var links_container = this_subject.find('.links_container');
if (links_container.data('busy') == true) return false;
links_container.data('busy', true);

links_container.find('li').hide().end().find('.mini_loading').show();

	$.ajax({
		type: "POST", 
		url: '/editor/rpc/post',
		datatype: "json",
		data:
			{
					action: "remove_link",
					subject_name: this_subject.name, 
					link_key: link_key
			},
		error: function() { links_container.html("Error Adding Link"); },
		success: function(response) {  links_container.html(response);  },
		complete: function(data) { links_container.data('busy', false); this_subject.trigger("initiate_links"); }
	});  
}

function ChangeVideo(new_video_url, this_subject)
{

var video_container = this_subject.find('.video_container');
if (video_container.data('busy') == true) return false;
video_container.data('busy', true);

video_container.find('object').hide().end().find('.mini_loading').show();

	$.ajax({
		type: "POST", 
		url: '/editor/rpc/post',
		datatype: "json",
		data:
			{
					action: "change_video",
					subject_name: this_subject.name, 
					new_video_url: new_video_url
			},
		error: function() { video_container.html("Error Adding Video"); },
		success: function(response) { video_container.html(response);  },
		complete: function(data) { video_container.data('busy', false); }
	});  
}


function DeleteSubjectImage(this_img, this_subject)
{

if (this_img.data('busy') == true) return false;
this_img.data('busy', true);
var subject_images = this_subject.find('div.subject_images');
var img_key = this_img.attr('id');

subject_images.find('div').hide().end().find('.mini_loading').show();

	$.ajax({
		type: "POST", 
		url: '/editor/rpc/post',
		datatype: "json",
		data:
			{
					action: "delete_subject_image",
					subject_name: this_subject.name, 
					img_key: img_key
			},
		error: function() { subject_images.html("Error Adding Video"); },
		success: function(response) {  subject_images.html(response); this_subject.trigger("initiate_images");  },
		complete: function(data) { this_img.data('busy', false); }
	});  
}


function SetupAdminRights(this_subject) {
	$('div.lower_level', this_subject).find('button.rights').click(function(){ ChangeRights( $(this) ); });
}

function ChangeRights(button){

	var this_choice = button.parent().find("option:selected");
	if (this_choice.length < 1) return alert("Please select a user"); 
	var user = this_choice.attr('id');
	var rights_action = button.attr("id");
    if (rights_action == "remove_admin") {
	if (user ==  this_choice.parents(".current_admins:first").attr('id')) return alert("E-mail support@plopquiz.com to remove your own administrator status");
    }
	// Todo: loading...
	var container = button.parents(".admin_rights:first");
	var subject_name = container.attr('id');


	$.ajax({
		type: "POST", 
		url: '/editor/rpc/post',
		datatype: "json",
		data:
			{
					action: "change_rights",
					rights_action: rights_action, 
					user: user,
					subject_name: subject_name,
			},
		error: function() { AjaxError(); },
		success: function(response) { container.html(response);  },
		complete: function() { SetupAdminRights(); } 
	});	

	
}



function CreateNewSubject() {

        	$("div#create_new_subject").dialog({ 
    modal: true,
    resizable: false,
    draggable: true,
    dialogClass: 'create_subject', 
    height: 320,
	width: 665,
    overlay: { 
        opacity: 0.8, 
        background: "black" 
    },
        buttons: { 
        "Create This Subject": function() { 
                        var subject_name = $(this).find('input').val();
            console.log(subject_name);
            if (subject_name == DEFAULT_NEW_SUBJECT_TEXT || subject_name == '') console.log('no subject name!'); 
            $(this).dialog("close"); 
        }
    } 
     
}).find('input').val(DEFAULT_NEW_SUBJECT_TEXT).preserveDefaultText(DEFAULT_NEW_SUBJECT_TEXT).end()
  .dialog("open");  // show() is to show hidden dialog 

}
