import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from google.appengine.ext import db
from google.appengine.api import users
from utils import webapp
from utils.utils import ROOT_PATH, tpl_path
# Import the main gchecky controller class
from utils.gchecky.controller import Controller
# import Google Checkout API model
import checkout
from utils.gchecky import model as gmodel
from model.proficiency import  Proficiency, ProficiencyTopic
from utils.gql_encoder import GqlEncoder, encode


# Template paths
STORE_PATH = 'store/'
DEFAULT_QUIZ_PRICE = 20



user_id = "30"





class Store(webapp.RequestHandler):

  def return_url(self):
      return str('http://' + self.request._environ['HTTP_HOST'] + '/store/return?id=')
      
  def merchant_info(self):
      if self.request._environ['HTTP_HOST'].endswith('plopquiz.com'): # production
          return {'id': 214037498108639, 'key': "heGOVhmPg4oFuIr_ruIzOw", 'is_sandbox': False}
      else: # development or staging
          return {'id': 104857833559093, 'key': "NNTk6Yw-wGioO7rglKai6A", 'is_sandbox': True}      

  #Store
  def get(self):
	merchant = self.merchant_info()
	# Create a (static) instance of Controller using your vendor ID and merchant key
	controller = Controller(merchant['id'], merchant['key'], is_sandbox=merchant['is_sandbox'])
	#Create your order:
	order = gmodel.checkout_shopping_cart_t(
		shopping_cart = gmodel.shopping_cart_t(items = [
			gmodel.item_t(merchant_item_id = 'oil_quiz',
						  name             = 'Oil Quiz',
						  description      = 'Oil quiz!',
						  unit_price       = gmodel.price_t(value    = DEFAULT_QUIZ_PRICE,
															currency = 'USD'),
						  quantity = 1),
			gmodel.item_t(merchant_item_id = 'energy_quiz',
						  name             = 'Energy Quiz',
						  description      = 'Energy quiz.',
						  unit_price       = gmodel.price_t(value    = DEFAULT_QUIZ_PRICE,
															currency = 'USD'),
						  quantity = 1),
		]),
		checkout_flow_support          = gmodel.checkout_flow_support_t(
			continue_shopping_url      = self.return_url() + user_id,
			request_buyer_phone_number = False))

	# Encode the order into XML, sign it with your merchant key and form
	# Google Checkout Button html.
	prepared = controller.prepare_order(order)

	# Now prepared.html contains the full google checkout button html
	template_values = {'checkout_button': prepared.html() }
	path = tpl_path(STORE_PATH +'store.html')
	self.response.out.write(template.render(path, template_values))

	 





class ChooseProficiency(webapp.RequestHandler):

    def get(self):
    	proficiencies = Proficiency.gql("WHERE status = :1", "public");
    	proficiencies = proficiencies.fetch(1000)
    	buy_buttons = []
    	for p in proficiencies: 
    	    p.checkout_button = checkout.render_quiz_button(self, p.tag(), p.name)
    	    buy_buttons.append( { 'tag': p.tag().lower(), 'html' : p.checkout_button})
    	    
    	prof_json = encode(proficiencies)
        template_values = {'proficiencies' : proficiencies, 'prof_json': prof_json, 'buy_buttons': encode(buy_buttons)}
        path = tpl_path(STORE_PATH + 'proficiency.html')
        self.response.out.write(template.render(path, template_values))

