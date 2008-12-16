
 

 
 
function PrivacyPolicy() {
	
        	$("#privacy_policy").dialog({ 
    modal: true,
    resizable: false,
    draggable: false, 
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
