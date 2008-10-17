import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplejson

from google.appengine.api import urlfetch
import string
import urllib
from .lib.BeautifulSoup import BeautifulSoup

from .utils import jsonparser as parser
from utils.utils import ROOT_PATH
from utils.gql_encoder import GqlEncoder, encode
from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
import views
import induction
from methods import DataMethods

class RPCHandler(webapp.RequestHandler):
  # AJAX Handler
  def __init__(self):
    webapp.RequestHandler.__init__(self)
    self.methods = RPCMethods()

  def get(self):
    func = None
   
    action = self.request.get('action')
    if action:
      if action[0] == '_':
        self.error(403) # access denied
        return
      else:
        func = getattr(self.methods, action, None)
   
    if not func:
      self.error(404) # file not found
      return
     
    args = ()
    while True:
      key = 'arg%d' % len(args)
      val = self.request.get(key)
      if val:
        args += (simplejson.loads(val),)
      else:
        break
    result = func(*args)
    self.response.out.write(simplejson.dumps(result))
    


class RPCMethods(webapp.RequestHandler):
  """ Defines AJAX methods.
  NOTE: Do not allow reload(sys); sys.setdefaultencoding('utf-8')
remote callers access to private/protected "_*" methods.
  """


######## MODEL METHODS ##########  


  def add_proficiency(self, *args):
	save_p = Proficiency(name = args[0])
	save_p.put()
  	return self.dump_data(["proficiencies"]) 


  def add_proficiency_topic(self, *args):
  	this_proficiency = Proficiency.get(args[1])
	save_topic = ProficiencyTopic(name = args[0], proficiency = this_proficiency)
	save_topic.put()
  	return self.dump_data(["proficiency_topics"])  
  	

    
    
  def refresh_data(self):
  	data = DataMethods()
  	data.delete_data(RawQuizItem.all())
  	data.delete_data(ContentPage.all())
  	data.delete_data(ProficiencyTopic.all())
  	data.delete_data(Proficiency.all())
  	data.load_data('proficiencies')
  	data.load_data('proficiency_topics')
  	data.load_data('content_pages')
  	data.load_data('raw_items')


  def dump_data(self, *args):  # dump data for fixtures
  	data = DataMethods()
  	if len(args) == 0: return "specify data type"
  	if args[0] == "raw_items" : print data.dump_data(RawQuizItem.all())
  	if args[0] == "content_pages" : print data.dump_data(ContentPage.all())
  	if args[0] == "proficiency_topics": print data.dump_data(ProficiencyTopic.all())
  	if args[0] == "proficiencies" : print data.dump_data(Proficiency.all())
  	print ""
  	print "---do not copy this line or below---"

  	


######## INDUCTION METHODS ##########  
        
  def SubmitContentUrl(self, *args):
      induce_url = induction.RawItemInduction()
      #JSON Serialize save_url
      data = DataMethods()
      # Save page,and topic, if necessary.
      # Induction:
      # 1. Perform semantic analysis
      # 2. Retrieve answer candidates
      # 3. Attempt to create raw quiz items.
      json_response = data.dump_raw_items(induce_url.get(args))
      return json_response



######## QUIZBUILDER METHODS ##########  

  def RetrieveTopics(self, *args):   # todo: should be nested list of proficiencies and topics.
      return_topics = []
      topics = ProficiencyTopic.all()
      return encode(topics.fetch(1000))



  def GetRawItemsForTopic(self, *args):  
      data = DataMethods()
      raw_quiz_items = []
      this_topic = ProficiencyTopic.gql("WHERE name = :1 ORDER BY date", args[0])
      #these_items = RawQuizItem().gql("WHERE topic = :1", this_topic.get())
      try: return data.dump_raw_items(this_topic.get().pages.get().raw_items.fetch(10))  # get 10 at a time...todo: lazy rpc-loader.
      except: return simplejson.dumps([])




  def SubmitQuizItem(self, *args):
      new_quiz_item = QuizItem()
      new_quiz_item.index = args[0]
      new_quiz_item.answers = args[1]
      new_quiz_item.slug = args[2]
       # And args[2] 
      new_quiz_item.category = str(args[4])       # different datastore? Not currently in model 
      new_quiz_item.proficiency = str(args[5])  # Should be Proficiency
      new_quiz_item.content = str(args[6])
      new_quiz_item.difficulty = 0 # Default?
      #new_quiz_item.put()
      print new_quiz_item
      return "saved quiz item" 








######## OPENCALAIS HELPER METHOD ##########

  def hund(self, *args):  # Workaround for 100,000 character limit for SemanticProxy.
		#page = 'http://' + str(args[0].replace('http%3A//',''))
		webpage = urlfetch.fetch(args[0])
		soup = BeautifulSoup(webpage.content)
		the_text = soup.findAll(text=True)[0:1000]
		all_text = []
		print ""
		for t in the_text:
			all_text.append(t.encode('utf-8'))
		print(string.join(all_text)[0:99999])
		#print soup.contents[1].findAll(text=True)
		#print str(page.contents)	

        
       





      	
