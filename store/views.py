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
from utils.utils import ROOT_PATH, tpl_path, memoize
# Import the main gchecky controller class
from utils.gchecky.controller import Controller
# import Google Checkout API model
import checkout
from utils.gchecky import model as gmodel
from model.proficiency import  Proficiency, ProficiencyTopic
from utils.gql_encoder import GqlEncoder, encode
from model.account import Account
from utils.webapp.util import login_required

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
  @memoize # only use for static functions
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
	template_values = {'checkout_button': prepared.html(), 'page_title': 'Take a Quiz' }
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






class TakeTest(webapp.RequestHandler):

  @login_required
  def get(self):
	# Now prepared.html contains the full google checkout button html
	account = Account.get_by_key_name(self.session['user'])
	account.pass_count = 1
	account.put()
	try: pass_count = account.pass_count
	except: # no pass count yet
	    try: 
	        account.pass_count = 1      # this is just to upgrade model.
	        pass_count = account.pass_count
	    except: 
	        from accounts.methods import register_account
	        register_account(self.session['user'])
	        account = Account.get_by_key_name(self.session['user'])
	        account.pass_count = 1
	        pass_count = account.pass_count
	        # take previous block out
	        
	         
	    account.put()
	test = self.get_test()
	template_values = {'no_load': True, 'pass_count': pass_count}
	path = tpl_path(STORE_PATH +'take_test.html')
	self.response.out.write(template.render(path, template_values))

  def get_test(self):
    if len(self.request.path.split('/sponsor/')[1]) > 0:
		employer = Employer.gql('WHERE name = :1', self.request.path.split('/quiz/')[1].lower())
		try: these_proficiencies = employer.get().proficiencies
		except: return None
		proficiencies = []
		for p in these_proficiencies:
		   this_p = Proficiency.get_by_key_name(p)
		   proficiencies.append(this_p.name)
		return [proficiencies, employer.get()]        
		#except: return [proficiency.name for proficiency in all_proficiencies.fetch(4)]
    if self.request.get('proficiencies'):
        proficiencies = self.request.get('proficiencies')
        return [eval(proficiencies,{"__builtins__":None},{}), self.get_default_vendor()]  
	return None




class Sponsorship(webapp.RequestHandler):

	def get(self):
		profile = self.get_profile()
		template_values = {'page_title': 'Sponsorship', 'no_load': True, 'profile': profile}
		path = tpl_path(STORE_PATH + 'sponsorship.html')
		self.response.out.write(template.render(path, template_values))


	def get_profile(self):
		if not len(self.request.path.split('/sponsor/')[1]) > 0: return False
		from model.user import Profile
		return Profile.gql('WHERE profile_path = :1', self.request.path.split('/sponsor/')[1].lower()).get()
