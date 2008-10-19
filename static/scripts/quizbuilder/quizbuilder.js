


jQuery(function($) {
	
	
// Setup RPC methods
var server = {};
var item_count = 0;

InstallFunction(server, 'RetrieveTopics');

InstallFunction(server, 'GetRawItemsForTopic');

InstallFunction(server, 'SubmitQuizItem');



wrong_answers = [];
answer_in_array = [];




$('.topic_name').preserveDefaultText('topic');
$('.url_name').preserveDefaultText('url');


server.RetrieveTopics("all", AfterRetrieveTopics);  // Create list of proficiency topics 


function AfterRetrieveTopics(response){  

var topics = parseJSON(response);

 $.each(topics, function(t, topic){
 
 // Add topic to list -- todo: nested list organized by proficiencies
 	
$('div#topics').append('<input type="checkbox" id="' + t + '" name="proficiency" value="' + topic.name + '" unchecked ><span>' + topic.name + '</span><br/>')

.find('input[@name="proficiency"]').click(function(){
$('input[@name="proficiency"]').setValue($(this).attr("value"));    });

topic_sum = t + 1;
return topic_sum;
});

$('input[@name="proficiency"]').setValue(topics[0].name);  // select first option as default


$('#submit_topic').click(function () {

        for (j = 0; j < topic_sum; j++) {
if (eval('document.select_topic.proficiency[' + j + '].checked') == true) {
    var proficiency = eval('document.select_topic.proficiency[' + j + '].value'); }}

    server.GetRawItemsForTopic(proficiency, AfterGetRawItemsForTopic);
    
    
$('form#select_topic').hide();
$('div#loading_items').show();
    
});


}



function AfterGetRawItemsForTopic(response){ BuildQuizEditor(response); }


 

});

