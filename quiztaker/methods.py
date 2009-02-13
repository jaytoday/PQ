import logging
from model.quiz import QuizItem, ItemScore
from model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic
from .model.employer import Employer 
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils import simplejson
from google.appengine.ext import db
from utils.gql_encoder import GqlEncoder, encode
    


 

def new_topic(topic_name, proficiency_name): 
	this_proficiency = Proficiency.gql("WHERE name = :1", proficiency_name)
	new_topic = ProficiencyTopic(name=topic_name, proficiency=this_proficiency.get().key())
	new_topic.put()
	return new_topic.key()


     
     
     
class DataMethods():
	




  def refresh_scores(self, verbose):
		scores = []		
		json_file = open(ROOT_PATH + "/data/item_scores.json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		# Retrieve Proficiency. If new, then save it.
		for item in newdata:
			# Store Item in Datastore
			if item['type'] == 'trash': continue
			if item['type'] == 'temp': continue
			this_taker = QuizTaker.get(item['quiz_taker']['key'])
			this_vendor = Employer.get(item['vendor']['key'])
			this_item = QuizItem.get(item['quiz_item']['key'])
			score = ItemScore(
								 quiz_taker = this_taker,
								 picked_answer = item['picked_answer'],
								 correct_answer = item['correct_answer'],
								 score = item['score'],
								 quiz_item = this_item,
								 vendor = this_vendor,
								 type = item['type'])
								  #Add List of Answers
			scores.append(score)
			if verbose[0] == "loud":
			  print encode(score)
		db.put(scores) # save scores 	   
							




  
			
  def load_data(self, data_type, *verbose):
		# Load External JSON fixture
		if data_type == "quiz_items": return self.refresh_quiz_items(verbose)
		if data_type == "item_scores": return self.refresh_scores(verbose)
		
		# refresh all?






class ProficiencyLevels():


	def set_all(self): # Set levels for all users -- this can't *actually*  be used. 
		return # Deprecated
		from ranking.methods import TopicLevelData, ProficiencyLevelData
		quiz_takers = QuizTaker.all().fetch(1000)        # this can only do a thousand at a time
		ptl = TopicLevelData()
		for qt in quiz_takers:
		  ptl.set(qt)
		pl = ProficiencyLevelData()
		for qt in quiz_takers:
		  pl.set(qt)      
	  
		  
	def set_for_user(self, qt):
		save = []
		from ranking.methods import TopicLevelData, ProficiencyLevelData
		ptl = TopicLevelData()
		save.extend( ptl.set(qt) )
		pl = ProficiencyLevelData()
		save.extend( pl.set(qt) ) 
		db.put(save)
		return save 
		# TODO: return value so it is known whether award check should be done. 
  
      
