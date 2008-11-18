
import os
import logging
from google.appengine.ext import db
from google.appengine.api import users
import webapp.template
from webapp import *


ROOT_PATH = os.path.dirname(__file__) + "/.."

global LOGINSTATUS
LOGINSTATUS = "unknown"




def tpl_path(template_file_name):
    return os.path.join(ROOT_PATH,
                        './templates', template_file_name)

                        

def login_text():
  # Construct Login/Logout Text.
  if users.get_current_user():
    LOGINSTATUS = "logged in"
    url_linktext = 'Logout'
  else:
    url_linktext = 'Login'
  return url_linktext




def check_login(LOGINSTATUS):
  # Construct Login/Logout Text.
  if users.get_current_user():
    LOGINSTATUS = "logged in"
  else:
    LOGINSTATUS = "logged out"
  return LOGINSTATUS

def raise_error(error_string):
    # Raise and Log Error
    logging.error(error_string)




def require_login(uri):
  if users.get_current_user():
    LOGINSTATUS = "logged in"
    return LOGINSTATUS
  else:
    redirect(users.create_login_url(uri))




def loginrequired(handler):
    def redirect_to_login(request):
        return redirect(users.create_login_url(handler.request.uri))

    user = users.get_current_user()
    if user:
        return func
    else:
        return redirect_to_login



def redirect_from_appspot(wsgi_app):
    def redirect_if_needed(env, start_response):
        if env["HTTP_HOST"].startswith('plopquiz.appspot.com'):
            import webob, urlparse
            request = webob.Request(env)
            scheme, netloc, path, query, fragment = urlparse.urlsplit(request.url)
            url = urlparse.urlunsplit([scheme, 'www.plopquiz.com', path, query, fragment])
            start_response('301 Moved Permanently', [('Location', url)])
            return ["301 Moved Peramanently",
                  "Click Here" % url]
        else:
            return wsgi_app(env, start_response)
    return redirect_if_needed
    

# 404
class NotFoundPageHandler(webapp.RequestHandler):
    def get(self):
        if self.request.path == "/": return
        self.error(404)
        path = tpl_path('404.html')
        template_values = {}
        self.response.out.write(template.render(path, template_values))




