import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from google.appengine.ext import webapp
from google.appengine.ext import db
import simplejson
import string, re
from google.appengine.api import urlfetch
import urllib
from .lib.BeautifulSoup import BeautifulSoup

from .utils import jsonparser as parser
from utils.utils import ROOT_PATH
from utils.gql_encoder import GqlEncoder, encode
from .model.quiz import QuizItem, RawQuizItem,  ContentPage
from .model.proficiency import ProficiencyTopic, Proficiency
import views
import induction
from methods import DataMethods, refresh_data, dump_data, load_data, restore_backup


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


  def add_topic(self, *args):
  	this_proficiency = Proficiency.get(args[1])
	save_topic = ProficiencyTopic(name = args[0], proficiency = this_proficiency)
	save_topic.put()
  	return self.dump_data(["proficiency_topics"])  
  	
  	
  def refresh_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	return refresh_data(args[0], "loud")

  def load_data(self, *args):
  	if len(args) == 0: return "specify data type"
  	return load_data(args[0], "loud")
   

  def dump_data(self, *args):  # dump data for fixtures
  	if len(args) == 0: return "specify data type"
  	if args[0] == "raw_items" : print dump_data(RawQuizItem.all())
  	if args[0] == "content_pages" : print dump_data(ContentPage.all())
  	if args[0] == "proficiency_topics": print dump_data(ProficiencyTopic.all())
  	if args[0] == "proficiencies" : print dump_data(Proficiency.all())
  	print ""
  	print "---do not copy this line or below---"

  def restore_backup(self, *args):
  	return restore_backup()  	


######## INDUCTION METHODS ##########  
        
  def SubmitContentUrl(self, *args):
      induce_url = induction.RawItemInduction()
      #JSON Serialize save_url
      data = DataMethods()
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
      return encode(topics.fetch(9))

  def RetrieveProficiencies(self, *args):   # todo: should be nested list of proficiencies and topics.
      return_proficiencies = []
      #proficiencies = Proficiency.all()
      proficiencies = Proficiency.gql("WHERE name in :1", ["Oil", "Solar Energy","Energy Finance","Biofuels","Electricity", "Energy Efficiency", "Ruby", "Rails"])  # remove after refactoring quiztaker
      return encode(proficiencies.fetch(1000, offset=0)) # temporary offset


  def GetRawItemsForTopic(self, *args):  
      data = DataMethods()
      raw_quiz_items = []
      this_topic = ProficiencyTopic.gql("WHERE name = :1 ORDER BY date DESC", args[0])
      #these_items = RawQuizItem().gql("WHERE topic = :1", this_topic.get())
      try: return data.dump_raw_items(this_topic.get().pages.get().raw_items.fetch(10))  # get 10 at a time...todo: lazy rpc-loader.
      except: return simplejson.dumps([])

  def GetRawItemsForProficiency(self, *args):  
      data = DataMethods()
      this_proficiency = Proficiency.gql("WHERE name = :1 ORDER BY date DESC", args[0]) # try get_or_insert if Proficiency is key
      prof_pages = this_proficiency.get().pages.fetch(10)
      raw_items = []
      for p in prof_pages:
          these_items = RawQuizItem.gql("WHERE page = :1 AND moderated = False", p ) # only get unmoderated items
          items = these_items.fetch(1000)
          raw_items += items
      try: return data.dump_raw_items(raw_items)  # get 10 at a time...todo: lazy rpc-loader.
      except: return simplejson.dumps([])

  def GetTopicsForProficiency(self, *args):  
      data = DataMethods()
      topics = []
      this_proficiency = Proficiency.gql("WHERE name = :1 ORDER BY date DESC", args[0]) # try get_or_insert if Proficiency is key
      topics = ProficiencyTopic.gql("WHERE proficiency = :1 ORDER BY date DESC", this_proficiency.get().key())
      try: return data.dump_raw_items(topics.fetch(10))  # get 10 at a time...todo: lazy rpc-loader.
      except: return simplejson.dumps([])
      

  def SetItemModStatus(self, *args):   # set moderation status for raw item
      this_item = db.get(args[0])
      if args[1] == "false": this_item.moderated = False
      if args[1] == "true": this_item.moderated = True
      this_item.put()
      return encode(this_item)


  def SubmitQuizItem(self, *args):
		new_quiz_item = QuizItem()
		new_quiz_item.index = string.lower(args[0])
		lc_answers = [string.lower(answer) for answer in args[1]]
		new_quiz_item.answers = lc_answers
		this_proficiency = Proficiency.gql("WHERE name = :1", args[5])
		this_topic = ProficiencyTopic.get_or_insert(args[2], name=args[2], proficiency=this_proficiency.get())
		this_topic.put()
		new_quiz_item.topic = this_topic.key()
		new_quiz_item.proficiency = this_topic.proficiency.key()
		# And args[2] 
		# new_quiz_item.proficiency = str(args[5])  # Should be Proficiency   - needs to be calculated. should be proficiency key. 
		new_quiz_item.content =  args[3].replace('title="Click to edit..."', '')
		new_quiz_item.content =  new_quiz_item.content.replace('^f"', '<div class="focus">')    # add focus div. 
		new_quiz_item.content =  new_quiz_item.content.replace('f$"', '</div>')
		new_quiz_item.content =  new_quiz_item.content.replace(' style="opacity: 1;"', '')
		blank_span = re.compile('<span id="blank">.*</span>')  #delete whatever is in span.blank!
		new_quiz_item.content =  blank_span.sub('<span style="opacity: 1;" id="blank"></span>', new_quiz_item.content)
		new_quiz_item.content =  new_quiz_item.content.replace('</div><div class="content">', '')
		new_quiz_item.content =  new_quiz_item.content.replace('</div><div class="post_content">', '')
		new_quiz_item.content =  new_quiz_item.content.replace('<div class="pre_content">', '')
		new_quiz_item.content =  new_quiz_item.content.replace('<div class="content">', '')
		new_quiz_item.content =  new_quiz_item.content.rstrip('</div>')

		new_quiz_item.difficulty = 0 # Default?
		new_quiz_item.content_url = args[4]
		new_quiz_item.theme = new_quiz_item.get_theme(args[4])
		new_quiz_item.put()
		print encode(new_quiz_item)
		return encode(new_quiz_item)
      
      




  def Jeditable(self, *args):   # set moderation status for raw item
      return args[0]




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
    
    
    
    


class RPCPostHandler(webapp.RequestHandler):
  """ Allows the functions defined in the RPCMethods class to be RPCed."""
  def __init__(self):
    webapp.RequestHandler.__init__(self)
    self.methods = RPCMethods()
 
  def post(self):
    args = simplejson.loads(self.request.body)
    func, args = args[0], args[1:]
   
    if func[0] == '_':
      self.error(403) # access denied
      return
     
    func = getattr(self.methods, func, None)
    if not func:
      self.error(404) # file not found
      return

    result = func(*args)
    self.response.out.write(simplejson.dumps(result))
        
