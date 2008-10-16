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

#from .utils import jsonparser as parser
from utils.utils import ROOT_PATH

from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
import views
import induction

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
  	return self.view_proficiencies()

  def view_proficiencies(self, *args):
  	proficiencies = []
  	get_proficiencies = Proficiency.all()
  	for this_proficiency in get_proficiencies.fetch(1000):
  		proficiency = {}
  		proficiency['name'] = this_proficiency.name
  		proficiency['key'] = str(this_proficiency.key())
  		proficiencies.append(proficiency)
  	return proficiencies		

  def add_proficiency_topic(self, *args):
  	this_proficiency = Proficiency.get(args[1])
	save_topic = ProficiencyTopic(name = args[0], proficiency = this_proficiency)
	save_topic.put()
  	return self.view_proficiency_topics()  
  	
  def view_proficiency_topics(self, *args):
  	topics = []
  	get_proficiency_topics = ProficiencyTopic.all()
  	for this_topic in get_proficiency_topics.fetch(1000):
  		topic = {}
  		topic['name'] = this_topic.name
  		topic['proficiency'] = this_topic.proficiency.name
  		topics.append(topic)
  	return topics	
    
    
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
      for this_topic in topics.fetch(1000):
      	topic = {}
      	topic['name'] = this_topic.name
      	topic['proficiency'] = this_topic.proficiency.name
      	return_topics.append(topic)
      json_response = simplejson.dumps(return_topics, indent=4)
      return json_response


  def GetRawItemsForTopic(self, *args):  
      data = DataMethods()
      raw_quiz_items = []
      this_topic = ProficiencyTopic.gql("WHERE name = :1", args[0])
      #these_items = RawQuizItem().gql("WHERE topic = :1", this_topic.get())
      # get 10 at a time...todo: lazy rpc-loader.
      try: return data.dump_raw_items(this_topic.get().pages.get().raw_items.fetch(10))
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

        
       



class DataMethods(webapp.RequestHandler):

  def delete_data(self, query):
     print ""
     entities = query.fetch(1000)
     for entity in entities:
     	print "DELETED"
     	print entity.__dict__
     	entity.delete()

    
  def load_data(self, data_type):
     print ""
     json_file = open(ROOT_PATH + "/data/" + str(data_type) + ".json")
     json_str = json_file.read()
     newdata = simplejson.loads(json_str) # Load JSON file as object
     for entity in newdata:
        if data_type == 'proficiencies':
	        save_entity = Proficiency(name = entity['name']) 
        if data_type == 'proficiency_topics':
			this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency'])
			print entity['proficiency']
			save_entity = ProficiencyTopic(name = entity['name'], 
			                               proficiency = this_proficiency.get())
        if data_type == 'content_pages':
			 this_topic = ProficiencyTopic.gql("WHERE name = :1", entity['topic'])
			 save_entity = ContentPage(url = entity['url'], topic = this_topic.get()) 
     	if data_type == 'raw_items':
            this_url = ContentPage.gql("WHERE url = :1", entity['url'])
            save_entity = RawQuizItem(
									  index = entity['index'],
									  answer_candidates = entity['answer_candidates'],
									  pre_content = entity['pre_content'],
									  content = entity['content'],
									  post_content = entity['post_content'],
									  page = this_url.get(),
									  moderated = False)

        try: save_entity.put()	
     	except:
     		logging.error('Unable to save new entity')
     		print 'Unable to save raw quiz item'
        print "ADDED"
        print save_entity.__dict__ 	
     	print save_entity.key()   





  def dump_raw_items(self, list_of_items, *response):
      raw_items = []
      for this_raw_item in list_of_items:
          raw_item = {}
          raw_item['pre_content'] = unicode(this_raw_item.pre_content)
          raw_item['content'] = unicode(this_raw_item.content)
          raw_item['post_content'] = unicode(this_raw_item.post_content)
          raw_item['answer_candidates'] = this_raw_item.answer_candidates
          raw_item['index'] = unicode(this_raw_item.index)
          raw_item['url'] = unicode(this_raw_item.page.url)
          raw_item['topic'] = unicode(this_raw_item.page.topic.name)
          raw_items.append(raw_item)
      # this parser needs to do character escaping 
      json_response = simplejson.dumps(raw_items, indent=4)
      if response == "print":
          print json_response 
      else:
      	return json_response  	
