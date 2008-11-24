from model.quiz import QuizItem, ItemScore
from model.user import QuizTaker
from .model.proficiency import Proficiency, ProficiencyTopic
from .model.employer import Employer 
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils import simplejson
from google.appengine.ext import db
from utils.gql_encoder import GqlEncoder, encode
    

def refresh_data(data_type, verbose):
  data = DataMethods()
  data.delete_data(data_type, verbose) 
  data.load_data(data_type, "") 
     

def load_data(data_type, verbose):
  data = DataMethods()
  data.load_data(data_type, "") 
       
 
def dump_data(gql_query):
  try:
	objects = gql_query.fetch(1000)
	return encode(objects)
  except:
	encode(objects)
	return "unable to encode objects"     
 

     
     
     
class DataMethods():
	
  def delete_data(self, data_type, *verbose):
		query = ""
		if data_type == "employers": query = db.GqlQuery("SELECT * FROM Employer")
		if not query: return False	
		objects = query.fetch(1000)
		for object in objects:
			if verbose[0] == "loud":
				print ""
				print "deleted: " + str(object.__dict__) 
			object.delete()
		return True
			
			
  def load_data(self, data_type, path):
		print data_type
		print ""
		json_file = open(ROOT_PATH + "/data/" + path + str(data_type) + ".json")
		json_str = json_file.read()
		newdata = simplejson.loads(json_str) # Load JSON file as object
		for entity in newdata:
			if data_type == 'employers':
				these_proficiencies = []
				for p in entity['proficiencies']:
				  these_proficiencies.append(Proficiency.get_or_insert(p, name = p).name)
				save_entity = Employer.get_or_insert(entity['name'], 
				                                     name = entity['name'],
				                                     email = entity['email'],
				                                     proficiencies = these_proficiencies) 
			try: save_entity.put()	
			except:
				logging.error('Unable to save new entity')
				print 'Unable to save new entity'
			print "ADDED"
			print save_entity.__dict__ 	
			print save_entity.key()   


