$(function(){

$('#submit_business').click(function(){
	
//	console.log('click');
	$.ajax(
                                {
                                        url:  "/dev/rpc",
                                        data:
                                        {
                                                action: "add_business",
                                                arg0: '"' + $('input#business_name').val() + '"'
                                        },
                                        success: function(response)
                                        {
//	console.log(response)               

}
});
});



$('a.delete').click(function(){

var this_link = $(this);

	$.ajax(
                                {
                                        url:  "/dev/rpc",
                                        data:
                                        {
                                                action: "delete_data",
                                                arg0: '"' + $(this).attr('id') + '"'
                                        },
                                        success: function(response)
                                        {
	// console.log(response.split('Status')[0]);
	this_link.parent().find('div.response').append(response.split('Status')[0]);                   
	
	}
});
});



$('a.load').click(function(){
	

LoadData($(this));


});


$('a#restore_all_data').click(function(){
	
var check = confirm("do you want to restore backup data? Existing data may be deleted!");

if (check) {
	$.getScript("/static/scripts/dev/restore.js");
}
else window.location="/dev/admin";


});




}); // end of onLoad



function LoadData(this_link){

	$.ajax(
                                {
                                        url:  "/dev/rpc",
                                        data:
                                        {
                                                action: "load_data",
                                                arg0: '"' + this_link.attr('id') + '"'
                                        },
                                        success: function(response)
                                        {
	
	
	
	this_link.parent().find('div.response').append(response.split('Status')[0]);    
	
//	console.log(response.substr(0, 8));
	if (response.indexOf("Data Load Is Finished") != -1)  { 
	//	console.log("finished!");
		return;
	
	}
	  //   console.log(response.split('Status')[0]);   
	      LoadData(this_link);    // Cycle is not completed yet     
	
	}
});

}
