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

    @memoize('homepage', 30000)
    def get(self):
        from homepage.methods import load_action_feed
        template_values = {'page_title': 'Plopquiz', 'recent_actions': load_action_feed(), 'featured_quiz': 'Recovery.Gov'}
        template_values['homepage_js'] = homepage_js(template_values)
        template_values['load'] = 2000 # give 2 seconds to load 
        path = tpl_path(HOMEPAGE_PATH + 'homepage.html')
        self.response.out.write(template.render(path, template_values))


	

	def load_action_feed():
		ACTION_THRESHOLD = 20 # too much? do testing on laptops.
		action_feed = []
		from model.account import Sponsorship, Award
		recent_sponsorships = Sponsorship.all().order('date').fetch(ACTION_THRESHOLD)
		recent_awards = Award.all().order('date').fetch(ACTION_THRESHOLD)
		action_feed.extend(recent_sponsorships)
		action_feed.extend(recent_awards)
		from operator import attrgetter
		action_feed.sort(key = attrgetter('date'), reverse = True)
		return action_feed
		





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
