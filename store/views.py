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








class Store(webapp.RequestHandler):
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
			gmodel.item_t(merchant_item_id = 'fruit_1',
						  name             = 'apple',
						  description      = 'An apple a day keeps doctors away',
						  unit_price       = gmodel.price_t(value    = .55,
															currency = 'USD'),
						  quantity = 3),
			gmodel.item_t(merchant_item_id = 'fruit_2',
						  name             = 'Orange',
						  description      = 'Why every orange is orange?',
						  unit_price       = gmodel.price_t(value    = .35,
															currency = 'USD'),
						  quantity = 7),
		]),
		checkout_flow_support          = gmodel.checkout_flow_support_t(
			continue_shopping_url      = 'http://wikipedia.org/fruits/',
			request_buyer_phone_number = False))

	# Encode the order into XML, sign it with your merchant key and form
	# Google Checkout Button html.
	prepared = controller.prepare_order(order)

	# Now prepared.html contains the full google checkout button html
	print prepared.html()
	return




	login_response = str('http://' + self.request._environ['HTTP_HOST'] + '/login/response')
	template_values = {'token_url': login_response }
	if self.request.get('error') == "true":
		template_values['error'] = "True"
	path = tpl_path(STORE_PATH +'store.html')
	self.response.out.write(template.render(path, template_values))

	 


class LoginResponse(webapp.RequestHandler):
		#RPX Response Handler
	def get(self):
		token = self.request.get('token')
		url = 'https://rpxnow.com/api/v2/auth_info'
		args = {
		  'format': 'json',
		  'apiKey': 'a36dbaa685c9356086c69b9923a637ecf33369bc',
		  'token': token
		  }
		r = urlfetch.fetch(url=url,
						   payload=urllib.urlencode(args),
						   method=urlfetch.POST,
						   headers={'Content-Type':'application/x-www-form-urlencoded'}
						   )
		json = simplejson.loads(r.content)
		print "a"
		print json
		return
		if json['stat'] == 'ok':    
		  unique_identifier = json['profile']['identifier']
		  nickname = json['profile']['preferredUsername']
		  email = json['profile']['email']
		  # log the user in using the unique_identifier
		  # this should your cookies or session you already have implemented
		  
		  #self.log_user_in(unique_identifier)    
		  self.redirect('/preview/homepage')
		else:
		  self.redirect('/login?error=true')
		  

    
class Logout(webapp.RequestHandler):
  #Login
  def get(self):
    template_values = {'token_url': self.request.env}
    path = tpl_path(STORE_PATH +'login.html')
    self.response.out.write(template.render(path, template_values))
    

