import logging

def sort_by_attr(seq,attr):
    intermed = [ (getattr(seq[i],attr), i, seq[i]) for i in xrange(len(seq)) ]
    intermed.sort()
    intermed.reverse() # ranked from greatest to least
    return [ tup[-1] for tup in intermed ]



def jsonp(callback, html):
    html = html.replace('\r\n','').replace("\n", "").replace("'", "&rsquo;");
    return callback + "('" + html + "');"

def compress(data):
    import gzip 
    import cStringIO
    zbuf = cStringIO.StringIO()
    zfile = gzip.GzipFile(mode='wb', compresslevel=2, fileobj=zbuf)
    zfile.write(data)
    zfile.close()
    return zbuf.getvalue()



def minify(js):
		from StringIO import StringIO
		from js.jsmin import JavascriptMinify
		ins = StringIO(js)
		outs = StringIO()
		JavascriptMinify().minify(ins, outs)   
		str = outs.getvalue()
		if len(str) > 0 and str[0] == '\n':
			str = str[1:]
		return str #compress(str)




def css_minify(css):
		return css.replace("\n", "")
		


