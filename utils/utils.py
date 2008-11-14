
import os
import logging
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template


ROOT_PATH = os.path.dirname(__file__) + "/.."

global LOGINSTATUS
LOGINSTATUS = "unknown"




def tpl_path(template_file_name):
    return os.path.join(ROOT_PATH,
                        './templates', template_file_name)

                        
def login_url(uri):
  # Construct Login/Logout URL.
  if users.get_current_user():
    url = users.create_logout_url(uri)
    url_linktext = 'Logout'
  else:
    url = users.create_login_url(uri)
    url_linktext = 'Login'
  return url

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







# 404
class NotFoundPageHandler(webapp.RequestHandler):
    def get(self):
        #x for testing 500 error
        self.error(404)
        path = tpl_path('404.html')
        template_values = {}
        self.response.out.write(template.render(path, template_values))
