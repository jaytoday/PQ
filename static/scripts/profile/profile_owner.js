


$(function()
{


        
        $('#sponsor_owner').click(function(){
        	
        	        	ShareProfile();
        	});
        
     



});




function ShareProfile() {
	
   
        	$("#share_profile").dialog({ 
    modal: true,
    resizable: false,
    draggable: false,
    height: 250,
    width: 400,
    overlay: { 
        opacity: 0.5, 
        background: "black" 
    },
        buttons: { 
                "Share With Sponsors": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.sponsors').show();
        },
        "Share With Employers": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.employers').show();
        }

    } 
     
}).show();

$('div.ui-dialog-buttonpane').find('button:first').addClass('clicked'); // initialize on first button
 $('div.ui-dialog-buttonpane > button').click(function(){
 	$(this).parent().find('button').removeClass('clicked');
 	$(this).addClass('clicked');
});

	//  $(this).dialog("close"); 
}
