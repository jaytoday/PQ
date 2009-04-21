CmdUtils.CreateCommand({
    name: "quiz",
    icon: "http://www.plopquiz.com/favicon.ico",
    homepage: "http://www.plopquiz.com",
    author: {
        name: "James Alexander Levy",
        email: "jamesalexanderlevy@gmail.com"
    },
    license: "GPL",
    description: "Generate a PlopQuiz Quiz Item",
    help: "Select the quiz statement, or type it in after the command",
    takes: {"statement": noun_arb_text},
    
    preview: function(pblock, statement){
        // Display the quiz statement. Either the user selection or the text they write
        var statement = CmdUtils.getSelection() || statement.text;
        var html = "<p><b>Quiz Statement:</b><br/><div id='statement'>" + statement + "</div></p>"
        pblock.innerHTML = html;
    },
    
    execute: function(statement){

        /*
         *
         * Setup Variables - Abstract differences between ubiquity and portable editor
         *
         */       

        var this_url = CmdUtils.getWindow().location.href;      
        var get_selection = function(){ return CmdUtils.getSelection(); };
        var statement = get_selection() || statement.text;
        var doc = CmdUtils.getDocument();
        var serverUrl = "http://localhost:8080";
        
        function setTimeout(func, time){ return Utils.setTimeout(func, time); };

    var id = "pq-injected-data";

	jQuery.ajax({
	type: "GET",
	url:  serverUrl +"/ubiquity/", 
	dataType: "jsonp",
	data:
	{
	get: "html",
	text: statement
	},
	error: function(data){
		jQuery(doc.body).append("<div id='error'>" + data + "</div>");
	},
	success: function(data){
		// Remove existing injected data
		jQuery('#' + id, doc.body).remove();
		jQuery('head', doc).append('<link rel="stylesheet" type="text/css"  href="' + serverUrl + '/static/html/quizbuilder/ubiquity.css" />');

					//get accompanying javascript
					jQuery.ajax({
					type: "GET",
					url: serverUrl + '/ubiquity/?get=js', 
					dataType: "jsonp",
					success:  function(script){
					eval(script); 
					jQuery(doc.body).append("<div id='" + id + "'>" + data + "</div>");
					runCode(); 
					 } 
						  }); 
							
	},
	complete: function(data){  }
	});


    }
    
    
    
});



        
        
        
 

