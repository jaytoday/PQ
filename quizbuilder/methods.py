import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext import db
from .model.quiz import QuizItem, RawQuizItem, ProficiencyTopic, ContentPage, Proficiency
from .utils.utils import tpl_path, ROOT_PATH, raise_error
import simplejson
#import views
import induction
from .quiztaker.methods import DataMethods as quiztaker_methods
from .employer.methods import DataMethods as employer_methods


def dump_data(gql_query):
	try:
		objects = gql_query.fetch(1000)
		return encode(objects)
		#for object in objects:
	except:
		return "unable to encode objects"
		

def load_data(data_type, verbose):
    data = DataMethods()
    return data.load_data(data_type, "")


def refresh_data(data_type, verbose):
    data = DataMethods()
    query = {"proficiencies": Proficiency.all(), 'proficiency_topics': ProficiencyTopic.all(), 'content_pages': ContentPage.all(), 'raw_items' : RawQuizItem.all()}
    data.delete_data(query[data_type])
    return data.load_data(data_type, "")

def restore_backup():
    data = DataMethods()
    data_types =  ["proficiencies", 'proficiency_topics', 'employers', 'content_pages', 'raw_items', 'raw_items', 'quiz_items']
    for data_type in data_types:
    	data.load_data(data_type, "/backup/")
    

class DataMethods():

  def delete_data(self, query):
     print ""
     entities = query.fetch(1000)
     for entity in entities:
     	print "DELETED"
     	print entity.__dict__
     	entity.delete()

    
  def load_data(self, data_type, path):
		print data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		entities = []
		for entity in newdata:
			if data_type == 'proficiencies':
				save_entity = Proficiency.get_or_insert(entity['name'], name = entity['name'])
				try: save_entity.status = entity['status']
				except: pass # no status specified
			if data_type == 'proficiency_topics':
				this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency']['name'])
				print entity['proficiency']
				save_entity = ProficiencyTopic.get_or_insert(entity['name'], name = entity['name'], 
											   proficiency = this_proficiency.get())
			if data_type == 'content_pages':
				 try: this_proficiency = Proficiency.gql("WHERE name = :1", entity['proficiency']['name'])
				 except TypeError: continue # some old content pages dont have proficiencies
				 print entity['url']
				 save_entity = ContentPage(url = entity['url'], proficiency = this_proficiency.get()) 
			if data_type == 'raw_items':
				print entity['page']['url']
				this_url = ContentPage.gql("WHERE url = :1", entity['page']['url'])
				save_entity = RawQuizItem(
										  index = entity['index'],
										  answer_candidates = entity['answer_candidates'],
										  pre_content = entity['pre_content'],
										  content = entity['content'],
										  post_content = entity['post_content'],
										  page = this_url.get(),
										  moderated = False)
			if data_type == 'quiz_items': 
				qtm = quiztaker_methods()
				return qtm.refresh_quiz_items("loud")
			if data_type == 'employers':
				emp = employer_methods()
				return emp.load_data("employers", "")
			entities.append(save_entity)
		try:
			print "saving", str(entities)
			db.put(entities)
		except:
			logging.error('Unable to save new entities')
			print 'Unable to save raw quiz items'
			


  def dump_raw_items(self, list_of_items, *response):
      return encode(list_of_items)
 	




