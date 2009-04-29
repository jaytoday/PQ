

// do we have jQuery
if(!window.jQuery ) { {% include "../static/scripts/jquery/jquery-1.3.1.min.js" %}   }


$(document).ready(function() {
	
                // TODO: visible error if no <body> in document
                $("script", $("body")).each(function() {
                if(this.src.indexOf('{{ http_host }}/js/quiz') > -1) 
                 $(this).after('<div id="pqwidget"><a href="{{ http_host }}/quiz/{{ quiz_subject }}" class="widget_footer">Take This Quiz at PlopQuiz.Com</a></div>'); } );
                 
                 
			 }
