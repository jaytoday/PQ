import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
from utils.webapp import template
from utils import webapp
from .utils.utils import tpl_path, ROOT_PATH, raise_error
import ranking_algorithm as filter

# Template paths
RANKING_PATH = 'ranking/'



class Graph(webapp.RequestHandler):
  def get(self):
    template_values = {}
    path = tpl_path(RANKING_PATH + 'graph.html')
    self.response.out.write(template.render(path, template_values))
    


class Filter(webapp.RequestHandler):
  def get(self):
    filter.run()
    return 
    template_values = {}
    path = tpl_path(RANKING_PATH + 'graph.html')
    self.response.out.write(template.render(path, template_values))
    


