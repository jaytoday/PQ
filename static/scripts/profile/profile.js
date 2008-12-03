

$(function()
{

	
	//$('div#loading_items').fadeIn('slow');
        $('div#right_corner').find('span').text('');
        //tabs
        $('.profile ul').tabs();

        $('.dynacloud').dynaCloud();

        //$("div.dynacloud").dynaCloud();

        // $.merge($.dynacloud.stopwords, [ "der", "die", "das" ]); -- add filters
        
     


});



function ShareProfile() {
	
   
        	$("#share_profile").dialog({ 
    modal: true, 
    overlay: { 
        opacity: 0.5, 
        background: "black" 
    },
        buttons: { 
        "Ok": function() { 
            alert("Ok"); 
        }, 
        "Cancel": function() { 
            $(this).dialog("close"); 
        } 
    } 
     
});
	
}






