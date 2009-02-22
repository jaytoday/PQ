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
          var select = function(classname) { //TODO: This should only look within our container
                return jQuery('#' + id + ' .' + classname, doc.body);
            }
          var default_text = 'Double-Click Here to Start Writing the Quiz Item Text...';
          var default_correct_answer_text = "none selected";
          var default_answer_text = "Click to Edit";
            
            //if selection length < 1, use text placeholder.
          var initText = function(){ if ( select('statement').text().length < 1 ) select('statement').text(default_text); }
              initText();
         
                select('statement').bind("dblclick", function(){
                var edit_text = jQuery(this).text();
                if (edit_text == default_text) edit_text = '';
                jQuery(this).hide()
                .parent().find('input').show().val(edit_text).focus().keypress(function(evt){
                  if (evt.keyCode == 13) select('submit_edit').click();})
                .end().find('button').show();
                  });
      
          // Submit edit of quiz item text
      select('submit_edit').bind("click", function(){
        var new_text = jQuery(this).parent().find('input').attr('value');
        jQuery(this).parent().find('input').hide().end()   // hide input
                    .find('.statement').show().html(new_text).end().end() //update text
                    .hide(); // hide button
      initText();
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

             select('correct_answer').text(default_correct_answer_text)
            // Set correct answer - TODO: triggered by mouse drag on statement text
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
                    select('suggestions').find('div.items').html(markup.join("\n"));
                    answerChoices(); // reset answer choice click event
                });
            });          


         
         
         // edit wrong answer text
         select('wrong_answer').find('span').text(default_answer_text).click(function(){
           var new_text  = jQuery(this).text();                           
           if (jQuery(this).text() == default_answer_text) new_text = "";

           jQuery(this).hide().parent().find('div.edit').show().find('input').val(new_text).focus()
           .keypress(function(evt){ if (evt.keyCode == 13) jQuery(this).parent().find('button').click();});

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

// show that subject is ready on change(). Check for 'create new' choice.
select('subject').change(function(){
  if (jQuery(this).find("option:selected").attr('id') == "new")
  { jQuery(this).find('select').hide().end().find('input').show().end().find('button').show();
    jQuery(this).data('ready', 'input');     
    return; }
jQuery(this).data('ready', true);
     });
 

// show that subject is ready on change(). Check for 'create new' choice.
select('topic').change(function(){
  if (jQuery(this).find("option:selected").attr('id') == "new")
  { jQuery(this).find('select').hide().end().find('input').show().end().find('button').show();
    jQuery(this).data('ready', 'input');      
    return; }
jQuery(this).data('ready', true);
});
 
select('cancel_input').click(function(){ jQuery(this).hide().parent()
                      .data('ready', false).find('input').hide().end().find('select').show() });

var submit_error = select('submit_error');
//Submit Item
select('submit_item').find('button#submit_item').click(function(){

submit_error.hide().text('');

// quiz item text
   var quiz_item_text = select('statement').text();
if (quiz_item_text == default_text) {
  submit_error.show().text('Specify Quiz Item Text');
  return false; }
// correct answer
  var correct_answer = select('correct_answer').text();
if (correct_answer == default_correct_answer_text) {
  submit_error.show().text('Specify a Correct Answer');
  return false; }
// wrong answers
  var wrong_answers = new Array();
  var all_answers = true;
select('selected_answers').find('.wrong_answer span').each(function(i){
if (jQuery(this).text() == default_answer_text) {
  submit_error.show().text('Specify Wrong Answers'); all_answers = false; }
wrong_answers.push("'" + jQuery(this).text() + "'");
}); if (all_answers == false) return false;

// subject
var subject = select('subject').find('select').attr('value');
if (select('subject').data('ready') != true) {
    if (select('subject').data('ready') == 'input') {  
  var subject = select('subject').find('input').val();
if (subject.length < 5) { submit_error.show().text('Subject Name is Too Short'); return false; }

}
  else {   submit_error.show().text('Choose a Subject');
  return false; }

}
// topic - more specific than subject
var topic = select('topic').find('select').attr('value');
if (select('topic').data('ready') != true) {
  if (select('topic').data('ready') == 'input') {
  var topic = select('topic').find('input').val();
  if (topic.length < 5) { submit_error.show().text('Topic Name is Too Short'); return false; }
}
  else { submit_error.show().text('Choose a Topic');
return false; }
}
// location of current page
var this_url = CmdUtils.getWindow().location.href;

// send quiz item to server
jQuery(this).text("Sending...").attr('disabled', true);
jQuery.ajax({
        type: "GET",
        url: serverUrl + "/quizbuilder/rpc",
        data: 'action=NewQuizItem&arg0="'
                    + quiz_item_text +
              '"&arg1="'
                    + correct_answer +
              '"&arg2="('
                    + wrong_answers +
              ')"&arg3="'
                    + subject +  
              '"&arg4="'
                    + topic +  
              '"&arg5="'
                    + this_url +
              '"',
        error: function(data){  },
        success: function(data) {
         
        }

});




  });
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