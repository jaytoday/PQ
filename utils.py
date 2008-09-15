#rom BeautifulSoup import BeautifulSoup
from google.appengine.api import urlfetch



import cgi
import wsgiref.handlers
import random
import os
import logging
import datetime, time



from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp

#RPC
from google.appengine.ext.webapp import util
import simplejson

ROOT_PATH = os.path.dirname(__file__)

global LOGINSTATUS
LOGINSTATUS = "unknown"

def tpl_path(template_file_name):
    return os.path.join(os.path.dirname(__file__),
                        'templates', template_file_name)

def item_path(template_file_name):
    return os.path.join(os.path.dirname(__file__),
                        'templates/items/', template_file_name)
                        
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




class GqlEncoder(simplejson.JSONEncoder):
  
  """Extends JSONEncoder to add support for GQL results and properties.
  
  Adds support to simplejson JSONEncoders for GQL results and properties by
  overriding JSONEncoder's default method.
  """
  
  # TODO Improve coverage for all of App Engine's Property types.

  def default(self, obj):
    
    """Tests the input object, obj, to encode as JSON."""

    if hasattr(obj, '__json__'):
      return getattr(obj, '__json__')()

    if isinstance(obj, db.GqlQuery):
      return list(obj)

    elif isinstance(obj, db.Model):
      properties = obj.properties().items()
      output = {}
      for field, value in properties:
        output[field] = getattr(obj, field)
      return output

    elif isinstance(obj, datetime.datetime):
      output = {}
      fields = ['day', 'hour', 'microsecond', 'minute', 'month', 'second',
          'year']
      methods = ['ctime', 'isocalendar', 'isoformat', 'isoweekday',
          'timetuple']
      for field in fields:
        output[field] = getattr(obj, field)
      for method in methods:
        output[method] = getattr(obj, method)()
      output['epoch'] = time.mktime(obj.timetuple())
      return output

    elif isinstance(obj, time.struct_time):
      return list(obj)

    elif isinstance(obj, users.User):
      output = {}
      methods = ['nickname', 'email', 'auth_domain']
      for method in methods:
        output[method] = getattr(obj, method)()
      return output

    return simplejson.JSONEncoder.default(self, obj)


def encode(input):
  """Encode an input GQL object as JSON

    Args:
      input: A GQL object or DB property.

    Returns:
      A JSON string based on the input object. 
      
    Raises:
      TypeError: Typically occurs when an input object contains an unsupported
        type.
    """
  return GqlEncoder().encode(input)  
