
 
$(function(){
	
	$('div#pq_login_link a').click(function(){
		if ($(this).attr('id') == "email") {
			
			$(this).hide('slow');
			$(this).parent().find('a#proxy').show('slow');
			
		}
		
		if ($(this).attr('id') == "proxy"){
			
			$(this).hide('slow');
			$(this).parent().find('a#email').show('slow');
			
		}
});
 
});
 
function PrivacyPolicy() {
	
        	$("#privacy_policy").dialog({ 
    modal: true,
    resizable: false,
    draggable: true, 
    height: 380,
	width: 535,
    overlay: { 
        opacity: 0.5, 
        background: "black" 
    },
        buttons: { 
        "Ok": function() { 
            $(this).dialog("close"); 
        }
    } 
     
}).show();  // show() is to show hidden dialog 

}
