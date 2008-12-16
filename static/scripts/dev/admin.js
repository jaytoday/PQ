$(function(){

$('#submit_business').click(function(){
	
	console.log('click');
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
	console.log(response)               }
});
});

});
