


jQuery(function($) {
	
	
// Setup RPC methods
var server = {};
var item_count = 0;

InstallFunction(server, 'RetrieveTopics');

InstallFunction(server, 'SubmitContentUrl');


InstallFunction(server, 'SubmitQuizItem');



wrong_answers = [];
answer_in_array = [];




$('.topic_name').preserveDefaultText('topic');
$('.url_name').preserveDefaultText('url');


server.RetrieveTopics("all", AfterRetrieveTopics);


function AfterRetrieveTopics(response){  // Create list of proficiency topics 

var topics = parseJSON(response);




 $.each(topics, function(t, topic){
$('div#topics').append('<input type="checkbox" id="' + t + '" name="proficiency" value="' + topic.name + '" unchecked ><span>' + topic.name + '</span><br/>')

.find('input[@name="proficiency"]').click(function(){
$('input[@name="proficiency"]').setValue($(this).attr("value"));    });

topic_sum = t + 1;
return topic_sum;
});


$('input[@name="proficiency"]').setValue(topics[0].name);  //default


$('#submit_url').click(function () {

        for (j = 0; j < topic_sum; j++) {
if (eval('document.content_url.proficiency[' + j + '].checked') == true) {
    var topic = eval('document.content_url.proficiency[' + j + '].value')
    }}

    server.SubmitContentUrl(document.content_url.url.value, topic, AfterSubmitUrl);
    
    
$('form#content_url').hide();
$('div#loading_items').show();
    
});


}




function AfterSubmitUrl(response){  BuildQuizEditor(response); }


 

});

