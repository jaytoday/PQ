


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
    draggable: true,
    height: 380,
    width: 515,
    overlay: { 
        opacity: 0.5, 
        background: "black" 
    },
        buttons: { 
                "Upgrade Your Resume": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.sponsors').show();
        },
        "Earn Sponsorships" : function() { 
            
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
