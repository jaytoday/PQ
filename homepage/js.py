import logging
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from utils import webapp
from utils.utils import tpl_path, memoize, Debug


FILE_CACHE_CONTROL = 'private, max-age=86400'
FILE_CACHE_TIME = datetime.timedelta(days=20)


class BaseJS(webapp.RequestHandler):
    @memoize('base_js')
    def get(self):
        if not Debug(): set_expire_header()
        template_values = {}
        path = tpl_path('base.js')
        from utils.random import minify 
        self.response.out.write( minify(template.render(path, template_values)) )

    
def set_expire_header():
  expires = datetime.datetime.now() + FILE_CACHE_TIME 
  self.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
  self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
