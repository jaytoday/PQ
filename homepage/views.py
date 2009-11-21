import logging
import wsgiref.handlers
import os
from utils.webapp import template
from utils import webapp
from .utils.utils import memoize, tpl_path

HOMEPAGE_PATH = 'homepage/'           
DEMO_PATH = 'demo/'



class TeaserHomepage(webapp.RequestHandler):
  def get(self):
    self.response.clear()
    template_values = {}
    path = tpl_path(DEMO_PATH + 'homepage.html')
    self.response.out.write(template.render(path, template_values))
    

              

class ViewHomepage(webapp.RequestHandler):

    
    def get(self):
        template_values = {}
        path = tpl_path('utils/none.html')
        self.response.out.write(template.render(path, template_values))

    def old_get(self):
        from homepage.methods import load_action_feed, get_featured_quiz
        template_values = {'page_title': 'Plopquiz', 'recent_actions': load_action_feed(), 'featured_quiz': get_featured_quiz() }
        template_values['homepage_js'] = homepage_js(template_values)
        path = tpl_path(HOMEPAGE_PATH + 'homepage.html')
        self.response.out.write(template.render(path, template_values))






class ExitPage(webapp.RequestHandler):

    def get(self):
        template_values = {}
        path = tpl_path(HOMEPAGE_PATH + 'exit.html')
        if self.request.get('o'): path = tpl_path(HOMEPAGE_PATH + 'old_exit.html')  #for demo, and old time's sake.
        self.response.out.write(template.render(path, template_values))




@memoize('homepage_js')
def homepage_js(template_values):
        path = tpl_path(HOMEPAGE_PATH  + 'scripts/homepage.js')
        from utils.random import minify 
        return minify( template.render(path, template_values) )




class RecentUpdates(webapp.RequestHandler):
  
  def get(self):
    template_values = {'updates': self.get_recent_updates()}
    path = tpl_path(HOMEPAGE_PATH  + 'recent.html')
    self.response.out.write(template.render(path, template_values))


  @memoize('recent_updates', 20000)
  def get_recent_updates(self):
  	WIKIRAGE_URL = "http://www.wikirage.com/rss/1/"
  	from google.appengine.api import urlfetch
  	fetch_page = urlfetch.fetch(WIKIRAGE_URL, follow_redirects=False)
  	from utils.BeautifulSoup import BeautifulSoup
  	soup = BeautifulSoup(fetch_page.content) 
  	updates = []
  	wiki_topics = [ guid.contents[0].split('/')[-2] for guid in soup.findAll('guid') ]
  	import urllib
  	for topic in wiki_topics:
  		topic = urllib.unquote(topic)
  		topic_name = topic.replace('_', ' ')
  		updates.append( { 'topic_path': topic, 'topic_name': topic_name } )
  	return updates

  	
  	
