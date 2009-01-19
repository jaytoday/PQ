  $(function() {
    $('.error').hide();  
    console.log($("button#sponsor_submit"));
    
    $("button#sponsor_submit").click(function() {

      // validate and process form here
      
      $('.error').hide();
      
      
  	  var name = $("input#name").val();
  		if (name == "") {
        $("label#name_error").show();
        $("input#name").focus();
        return false;
      }
  		var email = $("input#email").val();
  		if (email == "" ) {
        $("label#email_error").show();
        $("input#email").focus();
        return false;
      }
  		/*
  		 var phone = $("input#phone").val();
  		if (phone == "") {
        $("label#phone_error").show();
        $("input#phone").focus();
        return false;
      }
      */
      
      return false;
    });
    
    
FeedScroll();
    
  });
  

  
  
//scroll through action feed items
function FeedScroll(){	
	
	//if ($("#action_feed > div").length < 6) ExtendFeed();
	
var scroll_feed = setTimeout(function()
		{
		$("#action_feed > div:first").animate({opacity: 0, height: 0 }, {duration:800, complete:function(){ 
			$(this).remove(); $("#action_feed").append($(this).animate({opacity: 1, height: 100 }));    
			}});
		
		FeedScroll();
		}, 6000);
}
