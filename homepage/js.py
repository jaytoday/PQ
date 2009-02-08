import wsgiref.handlers
import datetime, time

from utils import webapp
from utils.utils import memoize


FILE_CACHE_CONTROL = 'private, max-age=86500'
FILE_CACHE_TIME = datetime.timedelta(days=20)


class Controller(webapp.RequestHandler):
	
	# Cache this as much as possible! This request gets hit on every page, at least once. 
    def get(self):
    	if self.request.get('js') == "base": return self.base_js()
    	if self.request.get('css') == "base": return self.base_css()
    	if self.request.get('css') == "blog": return self.blog_css()

    	
    		
	
    @memoize('base_js')
    def base_js(self):
        from utils.utils import tpl_path, Debug
        from utils.webapp import template
        if not Debug(): set_expire_header(self)
        template_values = {}
        path = tpl_path('base.js')
        from utils.random import minify 
        self.response.out.write( minify(template.render(path, template_values)) )
        
        
    @memoize('base_css')
    def base_js(self):
        from utils.utils import tpl_path, Debug
        from utils.webapp import template
        if not Debug(): set_expire_header(self)
        template_values = {}
        path = tpl_path('base.css')
        from utils.random import minify 
        self.response.out.write( minify(template.render(path, template_values)) )        
        


    @memoize('blog_css')
    def base_js(self):
        from utils.utils import tpl_path, Debug
        from utils.webapp import template
        if not Debug(): set_expire_header(self)
        template_values = {}
        path = tpl_path('base.js')
        from utils.random import minify 
        self.response.out.write( minify(template.render(path, template_values)) )
                

    
def set_expire_header(request):
  expires = datetime.datetime.now() + FILE_CACHE_TIME 
  request.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
  if request.request.get('test'): request.response.headers['Expires'] = "EXPIRE_TEST" #expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
  elif request.request.get('now'): request.response.headers['Expires'] = datetime.datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT')
  else: request.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
