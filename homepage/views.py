import logging
import cgi
import wsgiref.handlers
import os
import datetime, time
from utils.webapp import template
from utils import webapp
from utils.webapp import util
from .utils.utils import tpl_path, memoize, Debug

HOMEPAGE_PATH = 'homepage/'           
              


class ViewHomepage(webapp.RequestHandler):

    def get(self):
        from homepage.methods import load_action_feed
        template_values = {'page_title': 'Plopquiz', 'recent_actions': load_action_feed(), 'featured_quiz': 'Smart Grid'}
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

"""
class AboutUs(webapp.RequestHandler):

    def get(self):
        template_values = {'no_load': True}
        path = tpl_path(HOMEPAGE_PATH + 'about.html')
        self.response.out.write(template.render(path, template_values))
"""        


FILE_CACHE_CONTROL = 'private, max-age=86400'
FILE_CACHE_TIME = datetime.timedelta(days=20)


class BaseJS(webapp.RequestHandler):
    @memoize('base_js')
    def get(self):
        if not Debug(): self.set_expire_header()
        template_values = {} # this could be used for compiling JS into one file from several apps
        path = tpl_path('base.js')
        self.response.out.write(template.render(path, template_values))

    def set_expire_header(self):
      expires = datetime.datetime.now() + FILE_CACHE_TIME 
      self.response.headers['Cache-Control'] = FILE_CACHE_CONTROL
      self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')
