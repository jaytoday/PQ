/* Firebug Degradation */

if (!window.console || !console.firebug)
{
    var names = ["log", "debug", "info", "warn", "error", "assert", "dir", "dirxml",
    "group", "groupEnd", "time", "timeEnd", "count", "trace", "profile", "profileEnd"];

    window.console = {};
    for (var i = 0; i < names.length; ++i)
        window.console[names[i]] = function() {}
}



jQuery.fn.extend({
	preserveDefaultText: function(defaultValue, replaceValue)
	{
		$(this).focus(function()
		{
			if(typeof(replaceValue) == 'undefined')
				replaceValue = '';  
			if($(this).val() == defaultValue)
				$(this).val(replaceValue);
		});

		$(this).blur(function(){  
			if(typeof(replaceValue) == 'undefined')
				replaceValue = '';  
			if($(this).val() == replaceValue)
				$(this).val(defaultValue);
		});
		return this;
	}
});

function list(a)
{
  var o = {};
  for(var i=0;i<a.length;i++)
  {
    o[a[i]]='';
  }
  return o;
}

 
$(document).ready(function()
{
	var viewWidth = $('#viewport').width();
	var viewHeight = $('#viewport').height();
	$('#viewport .layer.near').css({width: (viewWidth * 1.4), height: (viewHeight*1.3)});
	$('#viewport .layer.mid').css({width: (viewWidth * 1.15), height: (viewHeight*1.05)});
	$('#viewport .layer.far').css({width: (viewWidth * 1.04), height: (viewHeight*1.01)});
	jQuery('#viewport').jparallax({});
	$('#viewport').css({overflow: "hidden"});
	
	
	
		$('input[type=button]').focus(function()
	{
		$(this).addClass('focus');
	})
	.focus(function()
	{
		// prevents crawling ants
		$(this).blur();
	}).mousedown(function()
	{
			$(this).addClass('down');
	}).mouseup(function()
	{
		$(this).removeClass('down');
	})
	.blur(function()
	{
		$(this).removeClass('focus');
	});

	$('input[type=button]').hover(function()
	{
		$(this).addClass('hover');      
	},function(){
		$(this).removeClass('hover');
	});
	
	
	$('a.about_dialog').click(function(){ $("div#about_dialog_content").dialog({ 
    modal: true,
    resizable: false,
    draggable: false,
    height: 300,
    width: 405,
    overlay: { 
        opacity: 0.5, 
        background: "black" 
    },
        buttons: { 
        "Introduction": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.about_introduction').show();
        },
         "Profiles": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.about_profiles').show();
        },
         "Sponsers": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.about_sponsors').show();
        }
    } 
     
}).show();

$('div.ui-dialog-buttonpane').find('button:first').addClass('clicked'); // initialize on first button
 $('div.ui-dialog-buttonpane > button').click(function(){
 	$(this).parent().find('button').removeClass('clicked');
 	$(this).addClass('clicked');
});

 });
	
	
	$('a.contact_dialog').click(function(){ $("div#contact_dialog_content").dialog({ 
    modal: true,
    draggable: false,
    resizable: false,
    height: 300,
    width: 405,
    overlay: { 
        opacity: 0.5, 
        background: "black" 
    },
        buttons: { 
        "Feedback": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.contact_feedback').show();
        },
         "Support": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.contact_support').show();
        },
         "Media": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.contact_media').show();
        },
         "Sales": function() { 
            
            $(this).find('div').hide();
            $(this).find('div.contact_sales').show();
        }        
    } 
     
}).show();

$('div.ui-dialog-buttonpane').find('button:first').addClass('clicked'); // initialize on first button
 $('div.ui-dialog-buttonpane > button').click(function(){
 	$(this).parent().find('button').removeClass('clicked');
 	$(this).addClass('clicked');
});


 });
 
 
 


//end ready()
});
