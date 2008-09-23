/* Javascript for SnapTalent Publish Popup */

// Helpers //////////////////////////////

$st = function(name){
    return document.getElementById(name);
}

// Image Swap //////////////////////////////

load_image_swap = function() {
    var ims = document.getElementsByName('image_link')
    var f = ims[0];
    if (f){
        image_swap(f);
    }
}

image_swap = function(t){
    var src = t.firstChild.src;
    $st('bphoto').src = image_large_link(src);
}

image_large_link = function(src){
    var ext = src.split('.');
    ext = ext[ext.length-1];
    var nsrc = src.substr(0,src.length-5)+'m.'+ext;
    return nsrc;
}

image_next = function(){
    var ims = document.getElementsByName('image_link');
    var csrc = $st('bphoto').src;
    var j = 0;
    for (var i=0; i<ims.length; i++){
        nsrc = image_large_link(ims[i].firstChild.src);
        if (csrc == nsrc){
            if (i == ims.length-1){ j = 0 }
            else { j = i+1 }
            $st('bphoto').src = image_large_link(ims[j].firstChild.src);
        }
    }
}

// Bookmarking //////////////////////////////

bookmark = function(id, title) {
    var url = "http://snaptalent.com/ads/"+id;
    if (document.all) {
        window.external.AddFavorite(url, title);
    } else if (window.sidebar) {
        window.sidebar.addPanel(title, url, "");
    } else {
        $st('bookmark_response').innerHTML = "Whoops, cannot bookmark. Try checking out this link <a href='http://snaptalent.com/ads/"+id+"/'>http://snaptalent.com/ads/"+id+"/</a>";
    }
    log(5);
}

// tabs //////////////////////////////

boldme = function(t){
    if (typeof t != 'object'){
        t = $st(t);
    }
	var $ts = $(t).parent('body [name=bolder]');
	$ts.siblings().children().css({
		fontWeight: 'normal',
		textDecoration: 'underline',
		paddingLeft: '0px'
	})
	$ts.children().css({
		fontWeight: 'bold',
		textDecoration: 'none',
		paddingLeft:	'0px'
	});
}

// Give me More! //////////////////////////////

see_more = function(more, t){
    var m = document.getElementsByName(more);
    for (var i=0; i<m.length; i++){
        m[i].style.display = 'block';
    }
    if (typeof t != 'undefined') {
        t.style.display = 'none';
    }
}

hide = function(less_of, num){
    var m = document.getElementsByName(less_of);
    for (var i=num; i<m.length; i++){
        m[i].style.display = 'none';
        $st('see_more_'+less_of).style.display = 'block';
    }
}

// youtube ////////////////////////////////

youtube_next = function(ticket){
    YTN = YTN+1;
    if (YTN > 3) { YTN = 1 }
    $st('youtube_thumb').src = "http://img.youtube.com/vi/"+ticket+"/"+YTN+".jpg";
}


// Highlight //////////////////////////////

highlight = function(word){
    var reg = new RegExp(word, "gi");
    var h = document.getElementsByName('highlightable');
    for (var i=0; i<h.length; i++){
        h[i].innerHTML = h[i].innerHTML.replace(reg, '<span class="pink">'+word+'</span>');
    }
}
