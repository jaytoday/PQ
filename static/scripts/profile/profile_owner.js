

function ShareProfile() {
	
   
        	$("#share_profile").dialog({ 
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
     
});
	
}
