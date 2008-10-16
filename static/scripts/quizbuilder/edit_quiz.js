
function EditQuizItem(i, item, answers) {
  
  //Disambiguate(i);
  
wrong_answers[i] = [];
answer_in_array[i] = [];    

 $.each(answers, function(n, answer){
 	
 answer_in_array[i][n] = "False"; 
 
});



 
 
 //// Style ////
 
 //$('div#' + i + ' > div#quiz_item_content').jScrollPane();
 
 
// $('div#answers_' + i).jScrollPane();
 
// $('#quiz_item_content').markItUp(mySettings);
   
   
      

$('#quiz_data_' + i + ' > input[@name="proficiency"]').click(function(){
$('#quiz_data_' + i + ' > input[@name="proficiency"]').setValue($(this).attr("value"));
});






	
    
		$('div#answers_' + i + '').find('.answer_candidate').click(function(){
			


answer_text = $(this).text();

n = $(this).attr("id");

console.log(n);


// TODO: ranking - splice() method can order answers 

//answer_in_array[i][n] = False;


console.log("true?", answer_in_array[i][n]);

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

wrong_answers[i].splice(wrong_answers[i].length, 0, answer_text);

answer_in_array[i][n] == "True";




 $(this).css("color","#000000"); 
  $(this).css("font-weight","bold"); 
  $(this).css("font-size",".9em"); 
  
  console.log('added item', answer_text, wrong_answers[i],wrong_answers[i].length);
  return;
  
}



			    

			});

 

function onItemAddSuccess(response)
{
    console.log(response);
}


    
function PreviewAnswer(answer) {

 	var answer_span = $('div#quiz_item_content_' + i + ' > div.content').find('.answer_span');
	$('#answers_' + i + '').find('.ac_container').hover(function()
	
	{
	      
        answer_span.fadeTo(1,0.5);
        answer_span.html($(this).text());
	    answer_span.fadeTo("slow", 1);
	
	},
	function()
	{
	    
		answer_span.empty();
		answer_span.html(answer);
        answer_span.fadeTo(100, 0.5);
	});   
    
    
}


PreviewAnswer(item.index);


            
        
$('#submit_item_' + i).click(function() {
    

console.log(eval('document.quiz_data_' + i + '.slug.value'));

console.log(eval('document.quiz_data_' + i + '.category.value'));

console.log(wrong_answers[i]);

console.log($('div#quiz_item_content_' + i).html())



 server.SubmitQuizItem(item.index, wrong_answers[i].concat(item.index), eval('document.quiz_data_' + i + '.slug.value'),   eval('document.quiz_data_' + i + '.category.value'), $('div#quiz_item_content_' + i).html(),  onItemAddSuccess);
});
    
    

}



 function Disambiguate(i){
	
$('.answer_span').one("click", function(){

	var this_word = $(this).text()
	
	console.log(this_word);
			 
		$(this).html('<input type="text" id="example"/>');
		
		
//$(this).find('#example').val(this_word);
console.log('what');
console.log(this_word);

   $(this).find('#example')
      
      .freebaseSuggest( {ac_param:{type:'/people/person'}, suggest_new: 'Create New Topic', } )
      .bind("fb-select", function(e, data) { 
         $('#miniTopic').show().freebaseMiniTopic(data.id);
    })
   .val('')
   .val(this_word)
    .focus()
    .blur()
    ;
    


});


$('div#test').one("click", function(){
	console.log('ra');
$('div#' + i).find("#example").keydown()
.keypress()
.keyup();
});




}
