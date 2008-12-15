
import os
import logging
from google.appengine.ext import db
from google.appengine.api import users
import webapp.template
from webapp import *
from model.dev import Admin 


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




def redirect_to_login(*args, **kwargs):
    return args[0].redirect(users.create_login_url(args[0].request.uri))

def admin_only(handler):
    def wrapped_handler(*args, **kwargs):    
        user = users.get_current_user()
        logging.debug(user)
        if user:
            if users.is_current_user_admin():
                return handler(args[0])
            else:
                logging.warning('An unauthorized user has attempted '
                                'to enter an authorized page')
                return args[0].redirect(users.create_logout_url('/')) #(users.create_logout_url(args[0].request.uri))
        else:
            return redirect_to_login(*args, **kwargs)

    return wrapped_handler
        
        
        
def authorized(user):
	"""Return True if user is authorized."""
	auth_user = users.is_current_user_admin()
	if auth_user: return True
	else: return False 
	"""
    else
	    new_user = Admin(key_name = str(user), user = user)
	    new_user.put()
	    return True
	"""
	    
			        



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
        self.error(404)
        path = tpl_path('utils/404.html')
        template_values = {'no_load': True}
        self.response.out.write(template.render(path, template_values))



def GetPathElements():
    '''split PATH_INFO out to a list, filtering blank/empty values'''
    return [ x for x in os.environ['PATH_INFO'].split('/') if x ]

def GetUserAgent():
    '''return the user agent string'''
    return os.environ['HTTP_USER_AGENT']

def Debug():
    '''return True if script is running in the development envionment'''
    return  'Development' in os.environ['SERVER_SOFTWARE']


def hash_pipe(private_object):
    import md5
    from google.appengine.api import memcache
    new_hash = md5.md5()
    new_hash.update(str(private_object))
    public_token = new_hash.hexdigest()
    memcache.add(public_token, private_object, 6000)
    return public_token



#### MEMCACHE

def memoize(key, time=10000):
    """Decorator to memoize functions using memcache."""
    
    def decorator(fxn):
        def wrapper(*args, **kwargs):
            from google.appengine.api import memcache
            data = memcache.get(key)
            if data is not None:
                return data
            data = fxn(*args, **kwargs)
            memcache.set(key, data, time)
            return data
        return wrapper
    return decorator  

    

### SESSIONS


def set_flash(msg):
	from appengine_utilities.sessions import Session
	session = Session()
	session['flash_msg'] = msg
	return msg


def get_flash(keep=False):
    from appengine_utilities.sessions import Session
    session = Session()
    msg = session['flash_msg']
    if not keep: session['flash_msg'] = False
    return msg
    
