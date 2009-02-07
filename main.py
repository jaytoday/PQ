from google.appengine.ext.webapp.util import run_wsgi_app
from utils.webapp.wsgi import WSGIApplication
from utils.utils import redirect_from_appspot, browser_check
from utils.routes.mapper import Mapper
map = Mapper(explicit = True)
from urls import url_routes


def RequestHandler():
    url_routes(map)
    app = WSGIApplication(map, debug = True)
    #app = redirect_from_appspot(app)
    app = browser_check(app) 
    run_wsgi_app(app)
                                

if __name__ == "__main__":
  RequestHandler()







