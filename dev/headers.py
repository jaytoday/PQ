import wsgiref.handlers
import datetime, time
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from utils.utils import memoize
from utils.utils import tpl_path, Debug
from utils.random import compress


FILE_CACHE_CONTROL = 'private, max-age=86500'
FILE_CACHE_TIME = datetime.timedelta(days=5)


class RequestHandler(webapp.RequestHandler):

    def get(self):
        if not Debug(): set_expire_header(self)
        if self.request.get('js'): 
            self.response.headers['Content-Type'] = 'text/javascript'
            #self.response.headers['Content-Encoding'] = 'gzip'
        if self.request.get('css') : self.response.headers['Content-Type'] = 'text/css'
        output = False
        if self.request.get('js') == "base": output = self.base_js()
        if self.request.get('css') == "base": output = self.base_css()
        if self.request.get('css') == "blog": output = self.blog_css()
        #headers["content-md5"] = b64encode(checksum)
        self.response.out.write( output )
        
        
    @memoize('base_js')
    def base_js(self):
        template_values = {}
        path = tpl_path('base.js')
        from utils.random import minify 
        return minify(template.render(path, template_values)) 
        	
	
    @memoize('base_css')
    def base_css(self):
        template_values = {}
        path = tpl_path('css/base.css')
        from utils.cssmin import cssmin
        return cssmin(template.render(path, template_values)) 



    @memoize('blog_css')
    def blog_css(self):
        template_values = {}
        path = tpl_path('css/blog.css')
        from utils.cssmin import cssmin
        return cssmin(template.render(path, template_values)) 
            




    
def set_expire_header(request):
  expires = datetime.datetime.now() + FILE_CACHE_TIME 
  request.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
  if request.request.get('test'): request.response.headers['Expires'] = "EXPIRE_TEST" #expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
  elif request.request.get('now'): request.response.headers['Expires'] = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
  else: request.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')





