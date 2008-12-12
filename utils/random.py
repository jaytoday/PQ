import logging

def sort_by_attr(seq,attr):
    intermed = [ (getattr(seq[i],attr), i, seq[i]) for i in xrange(len(seq)) ]
    intermed.sort()
    intermed.reverse() # ranked from greatest to least
    return [ tup[-1] for tup in intermed ]



def jsonp(callback, html):
    html = html.replace('\r\n','').replace("\n", "").replace("'", "&rsquo;");
    return callback + "('" + html + "');"

    

