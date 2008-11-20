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
from utils.gchecky import model as gmodel



# Template paths
STORE_PATH = 'store/'
DEFAULT_QUIZ_PRICE = 20



user_id = "30"




def return_url(self):
  return str('http://' + self.request._environ['HTTP_HOST'] + '/store/return?id=')
  
def merchant_info(self):
  if self.request._environ['HTTP_HOST'].endswith('plopquiz.com'): # production
	  return {'id': 214037498108639, 'key': "heGOVhmPg4oFuIr_ruIzOw", 'is_sandbox': False}
  else: # development or staging
	  return {'id': 104857833559093, 'key': "NNTk6Yw-wGioO7rglKai6A", 'is_sandbox': True}      

#Store
def render_quiz_button(self, proficiency_tag, proficiency_name ):
	merchant = merchant_info(self)
	# Create a (static) instance of Controller using your vendor ID and merchant key
	controller = Controller(merchant['id'], merchant['key'], is_sandbox=merchant['is_sandbox'])
	#Create your order:
	order = gmodel.checkout_shopping_cart_t(
		shopping_cart = gmodel.shopping_cart_t(items = [
			gmodel.item_t(merchant_item_id =  proficiency_tag,
						  name             = proficiency_name,
						  description      = proficiency_name,
						  unit_price       = gmodel.price_t(value    = DEFAULT_QUIZ_PRICE,
															currency = 'USD'),
						  quantity = 1),
		]),
		checkout_flow_support          = gmodel.checkout_flow_support_t(
			continue_shopping_url      = return_url(self) + user_id,
			request_buyer_phone_number = False))

	# Encode the order into XML, sign it with your merchant key and form
	# Google Checkout Button html.
	prepared = controller.prepare_order(order)

	# Now prepared.html contains the full google checkout button html
	return prepared.html()


 

