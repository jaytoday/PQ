
 
$(function()
{



	});

 
 
function PrivacyPolicy() {
	
        	$("#privacy_policy").dialog({ 
    modal: true, 
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
