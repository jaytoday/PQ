


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



function AfterGetRawItemsForTopic(response){


var raw_quiz_items = parseJSON(response);

if (raw_quiz_items.length == 0) { $('div#loading_items').html('no quiz items returned -- <a href="">try again?</a>'); }  // no items returned

 $.each(raw_quiz_items, function(i,item){


$('ul.item_navigation').append('<li><a href="#' + i + '">' + item.index + '</a></li>');
	
 	
// raw item template 	
 	
var html = '<div class="quiz_item"  id="' + i + '" ></div>';

html += '<div class="quiz_item_content" id="quiz_item_content_' + i + '"><div class="item_inner">'; // start quiz item content

html += '<div class="pre_content">' + item.pre_content + '</div>';

html += '<div class="content" >' + item.content + '</div>';

html += '<div class="post_content">' + item.post_content + '</div>';


html += '</div></div>'; //end quiz item content


html += '<div class="index">' + item.index + '</div>';


html += '<div class="quiz_form"><form id="quiz_data_' + i + '" name="quiz_data_' + i + '"><input type="text" name="slug" class="slug_name" value="slug_name" /><br/><input type="text" name="category" class="category_name" value="category" /><br/><input type="submit" onClick="return false;this.disabled = true;" id="submit_item_' + i + '" class="submit_item" value="Submit Quiz Item" /></form></div>';


html += '<div class="answers_container"><div class="answer_candidates" id="answers_' + i + '"></div></div>';  // Expand answer candidates




// load items
$('div#quiz_items').append(html);
$('div#loading_items').hide();
$('ul.item_navigation').show('slow');
$('div#quiz_items').show('slow');



answers =  eval(item.answer_candidates); //item.answer_candidates



 $.each(answers, function(n, answer){
 	
 	
answer_html = '<div class="ac_container"><div id ="' + n + '" class="answer_candidate" >' + answer + '</div></div>';


$('div#answers_' + i).append(answer_html);

});




EditQuizItem(i, item, answers); // Run function after the above code is evaluated.



});




sliderInit();  


}


 

});

