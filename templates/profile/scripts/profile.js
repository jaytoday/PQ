

$(function()
{
console.log('bleeeah');

$main_tabs = $('.profile ul').tabs();
        
$sidebar_tabs = $('#profile_sidebar').tabs();

console.log('blah');

console.log($('div.subject_img'));
$('div.subject_img').mouseover(function(){ console.log('on'); $(this).find('span').slideUp(1000);});

$('div.subject_img').mouseout(function(){ console.log('off'); $(this).find('span').slideDown(1000);});

});


