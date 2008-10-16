
function EditQuizItem(i, item, answers) {
  
  
wrong_answers[i] = [];
answer_in_array[i] = [];    

 $.each(answers, function(n, answer){
 	
 answer_in_array[i][n] = "False"; 
 
});


 
 //$('div#' + i + ' > div#quiz_item_content').jScrollPane();

// $('div#answers_' + i).jScrollPane();
 
// $('#quiz_item_content').markItUp(mySettings);
   
   
      

$('#quiz_data_' + i + ' > input[@name="proficiency"]').click(function(){
$('#quiz_data_' + i + ' > input[@name="proficiency"]').setValue($(this).attr("value"));
});


    
$('div#answers_' + i + '').find('.ac_container').click(function(){
			
//    If answer is selected, remove it if it's already in array. 
//    If not, add it to the array, if the limit hasn't been reached. 

answer_text = $(this).text();

n = $(this).attr("id");


for (var a = -1, loopCnt = wrong_answers[i].length; a < loopCnt; a++) {



if (answer_text == wrong_answers[i][a]){   // if answer text is already there


wrong_answers[i].splice(wrong_answers[i].indexOf(answer_text), 1);

answer_in_array[i][n] = "False"; // answer not in array anymore

$(this).css("color","#555555");
$(this).css("font-weight","normal"); 
$(this).css("font-size","1em"); 

console.log('removed text');
return;


}

}

console.log('array', wrong_answers[i]);

if (answer_in_array[i][n] == "False") {

if (wrong_answers[i].length > 1) { console.log("Only 2 Wrong Answers, Please!"); return false; }  // If there are already two answers

wrong_answers[i].splice(wrong_answers[i].length, 0, answer_text);   // add answer to array

answer_in_array[i][n] == "True";




 $(this).css("color","#000000"); 
  $(this).css("font-weight","bold"); 
  $(this).css("font-size",".9em"); 
  
  console.log('added item', answer_text, wrong_answers[i],wrong_answers[i].length);
  return;
  
}



			    

			});

 
    
function PreviewAnswer(answer) {
	
	// On a hover over an answer, preview its text in the item content.

 	var answer_span = $('div#quiz_item_content_' + i + ' > div.item_inner').find('.answer_span');
	$('#answers_' + i + '').find('.ac_container').hover(function()
	
	{
        //answer_span.fadeTo(1,0.5);
        answer_span.html($(this).text());
	    answer_span.fadeTo("slow", 1);
	
	},
	function()
	{
	    
		answer_span.empty();
		answer_span.html(answer);
        //answer_span.fadeTo(100, 0.5);
	});   
    
  
}


PreviewAnswer(item.index);


            
        
$('#submit_item_' + i).click(function() {
	
	// Edited quiz item is submitted. 
    

console.log(eval('document.quiz_data_' + i + '.slug.value'));

console.log(eval('document.quiz_data_' + i + '.category.value'));

console.log(wrong_answers[i]);

console.log($('div#quiz_item_content_' + i).html())



 server.SubmitQuizItem(item.index, wrong_answers[i].concat(item.index), eval('document.quiz_data_' + i + '.slug.value'),   eval('document.quiz_data_' + i + '.category.value'), $('div#quiz_item_content_' + i).html(),  onItemAddSuccess);
});
 
 
 
 

function onItemAddSuccess(response)
{
    console.log(response);
}


   
    

}

