CmdUtils.CreateCommand({
    name: "quiz",
    icon: "http://www.plopquiz.com/favicon.ico",
    homepage: "http://www.plopquiz.com/preview/homepage",
    author: { name: "Ben Dowling", email: "ben.m.dowling@gmail.com"},
    license: "GPL",
    description: "Generate a PlopQuiz Quiz Item",
    help: "Select the quiz statement, or type it in after the command",
    takes: {"statement": noun_arb_text},
    
    preview: function( pblock, statement ) {
      // Display the quiz statement. Either the user selection or the text they write
      var statement = CmdUtils.getSelection() || statement.text;
      var html = "<p><b>Quiz Statement:</b><br/><div id='statement'>" + statement + "</div></p>"
      pblock.innerHTML = html;
    },
    
    execute: function(statement) {
        var statement = CmdUtils.getSelection() || statement.text;
        var doc = CmdUtils.getDocument();
        var serverUrl = "http://localhost:8080";
      
        
        
        var id = "ubiquity-injected-data";
        
      
        // The code below should be externalised if possible        
        var runCode = function() {
            // A little helper function to get an element by class
            // name from the injected HTML
          var select = function(classname) {
                return jQuery('#' + id + ' .' + classname, doc.body);
            }
          var default_text = 'Double-Click Here to Start Writing the Quiz Item Text...';
            
            //if selection length < 1, initiate edit.
            if ( select('statement').text().length < 1 ) select('statement').text(default_text);
         
                select('statement').bind("dblclick", function(){
                var edit_text = jQuery(this).text();
                if (edit_text == default_text) edit_text = '';
                jQuery(this).hide()
                .parent().find('input').show().val(edit_text)
                .end().find('button').show();
                  });
      
          //select('statement').parent
      select('submit_edit').click(function(){
        var new_text = jQuery(this).parent().find('input').attr('value');
        jQuery(this).parent().find('input').hide().end()   // hide input
                    .find('.statement').show().html(new_text).end().end() //update text
                    .hide(); // hide button
      
        });
          

                     
               
                
            
            var lookupAlternativeAnswers = function(answer, callback) {
                var lookupUrl = "http://www.freebase.com/api/service/search?limit=6&query=" +  encodeURI(answer);
                jQuery.getJSON(lookupUrl, function(data) {
                    var alternatives = new Array();
                    for(var result in data.result) {
                        var suggestion = data.result[result].name;
                        if(suggestion.toLowerCase() == answer.toLowerCase()) continue;
                        alternatives.push(suggestion);
                    }
                    callback.call(this, alternatives);
                });
            }
            
            // Close button event handler
            select('close').click(function() {
                jQuery('#' + id, doc.body).remove();
            });

            // Set button - ideally, this would also be triggered by mouse drag on statement text
            select('set_correct_answer').click(function() {
                var answer = CmdUtils.getSelection();
                if (answer.length < 1) return false;
                select('correct_answer').text(answer);
                select('suggestions').css('display', 'block');
                lookupAlternativeAnswers(answer, function(alternatives) {
                    select('loading').hide();
                    var markup = new Array();
                    for(var alt in alternatives) {
                        markup.push("<div style='height: 13px; margin: 10px 0; cursor:pointer;'><button "    
                                   + "style='float:left; cursor:pointer; margin: -4px 4px 0px 0;'><img src='"
                                    + serverUrl + "/static/stylesheets/img/utils/purple_next_tiny.png"
                                    + "'/></button>"
                                     + alternatives[alt] + "</div>");
                    }
                    select('suggestions').find('div.items').append(markup.join("\n"));
                    answerChoices(); // reset answer choice click event
                });
            });          


         var default_answer_text = "Click to Edit";
         
         select('wrong_answer').find('span').text(default_answer_text).click(function(){
           var new_text  = jQuery(this).text();                           
           if (jQuery(this).text() == default_answer_text) new_text = "";

           jQuery(this).hide().parent().find('div.edit').show().find('input').val(new_text);

                                     });


     // update edited wrong answer
     select('wrong_answer').find('button').click(function(){
       var new_text = jQuery(this).parent().find('input').attr('value');
       if (new_text == "") new_text = default_answer_text;
       jQuery(this).parent().hide().parent().find('span').text(new_text).show();
  });

    // set wrong answer from suggestion
      var answerChoices = function(){
       select('items').find('div').find('button').click(function(){
      var new_answer = jQuery(this).parent().text();
      var first_answer = select('selected_answers').find('.wrong_answer:eq(0)').find('span');
       select('selected_answers').find('.wrong_answer:eq(1)').find('span').text( first_answer.text() );
       first_answer.text(new_answer);

       
  
});
               };



        }; //end of runCode




jQuery.ajax({
        type: "GET",
        url: serverUrl + "/ubiquity/",
        data: "get=html&text=" + escape(statement),
        error: function(data){ jQuery(doc.body).append("<div id='error'></div>"); },
        success: function(data) {
            // Remove existing injected data
            jQuery('#' + id, doc.body).remove();
            // Inject remote data
            jQuery(doc.body).append("<div id='" + id + "'>" + data + "</div>");
            //jQuery.getScript(serverUrl + "/ubiquity/?get=js", function(){ });
            // Run javascript
          // appending to the head doesn't work
          jQuery(doc.head).append(
'<link rel="stylesheet" type="text/css"  href="' + serverUrl + '"static/html/quizbuilder/ubiquity.css" />');
            runCode();
        }

});

    }
});