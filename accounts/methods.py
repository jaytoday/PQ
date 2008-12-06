import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
from .model.user import Profile, QuizTaker, ProfilePicture
from model.account import Account, Award
import random
from google.appengine.ext import db




def registered(user_key):
    this_user = Profile.get_by_key_name(user_key)
    if this_user: return this_user
    else: return False
    
    



def register_user(user_key, nickname, fullname, email):
    profile_path = nickname.lower()
    profile_path = profile_path.replace(' ','_')
    photo = default_photo()
    new_user = Profile.get_or_insert(key_name = user_key,
                          unique_identifier = user_key, # redundancy
                          nickname = nickname,
                          fullname = fullname,
                          profile_path = profile_path,
                          photo = photo,
                          )
                          
    if email: new_user.email = email
    new_user.put()
    return new_user 



def register_qt(user_key, nickname):
    new_qt = QuizTaker.get_or_insert(key_name = user_key,
                                     unique_identifier = user_key, # redundancy
                                     nickname = nickname,
                                     )
    new_qt.put()
    return new_qt                                   
    

def register_account(user_key, nickname):
    new_account = Account.get_or_insert(key_name = user_key,
                                     unique_identifier = user_key, # redundancy
                                     nickname = nickname # redundancy 
                                     )
    new_account.put()
    return new_account                                   
    
        

def default_photo():
	photos = ProfilePicture.gql("WHERE type = :1", "pq").fetch(10)
	photo = random.sample(photos, 1) 
	return photo[0]






class Awards():
	
	# Analyze proficiency levels and topiclevels, give awards to quiztakers. 

     # Eventually, a quiztaker attribute will have to mark whether its been processed.
    
	EXCELLENCE_PROFICIENCY_THRESHOLD = 0.1
	FLUENCY_PROFICIENCY_THRESHOLD = .55	
	EXCELLENCE_TOPIC_THRESHOLD = 90
	FLUENCY_TOPIC_THRESHOLD = 55
	
	def check_all(self):
		self.save_awards = [] # for batch datastore trip
		quiz_takers = QuizTaker.all().fetch(1000)
		for qt in quiz_takers:
			self.check_taker(qt)
		db.put(self.save_awards)
		return
			
	def check_taker(self, qt):			
			# Re-Initialize Values 
			from collections import defaultdict 
			self.fluency = defaultdict(list)   
			self.excellence = defaultdict(list)
			self.awarded_proficiencies = {}
			self.topics_in_proficiency = defaultdict(list)    
			for level in qt.topic_levels:
				self.topics_in_proficiency[level.topic.proficiency.key()].append(level.topic.key()) 
				self.add_topic_fluency(level)
				self.add_topic_excellence(level)
			self.check_proficiency_excellence()
			self.check_proficiency_fluency()
			self.upgrade_awards(qt)
			return
			
			
	def add_topic_fluency(self, level):
		# topic_level should be replaced by percentile	
	  if level.topic_level > self.FLUENCY_TOPIC_THRESHOLD: 
	      self.fluency[level.topic.proficiency.key()].append({level.topic.key() : level.topic_level}) 
	      return True
	  else: return False	


	def add_topic_excellence(self, level):	
	  if level.topic_level > self.EXCELLENCE_TOPIC_THRESHOLD: 
	      self.excellence[level.topic.proficiency.key()].append({level.topic.key() : level.topic_level}) 
	      return True
	  else: return False

	def check_proficiency_excellence(self):
		for proficiency, topics in self.topics_in_proficiency.items():
			print float(float(len(self.excellence[proficiency])) / float(len(topics)))
			if float(float(len(self.excellence[proficiency])) / float(len(topics))) > self.EXCELLENCE_PROFICIENCY_THRESHOLD: self.awarded_proficiencies[proficiency] = "Excellence"

	def check_proficiency_fluency(self):
		for proficiency, topics in self.topics_in_proficiency.items():
			if float(float(len(self.fluency[proficiency])) / float(len(topics))) > self.FLUENCY_PROFICIENCY_THRESHOLD: self.awarded_proficiencies[proficiency] = "Fluency"
	  	  

	def upgrade_awards(self, qt):
		for proficiency, type in self.awarded_proficiencies.items():
			print "upgrading award"
			print proficiency, type
			#topic_list = self.topics_in_proficiency[proficiency]   - Only Needed if we need all the topics in the proficiency
			if type == "Fluency": rankings = self.fluency[proficiency]
			if type == "Excellence": rankings = self.excellence[proficiency]
			this_account = Account.get_by_key_name(qt.unique_identifier)
			this_profile = Profile.get_by_key_name(qt.unique_identifier)
			if not this_account: 
			    this_account = register_account(qt.unique_identifier)
			print this_account
			award_topics = [] 
			award_levels = []
			print rankings.__class__
			for rank_dict in rankings:
				for topic, level in rank_dict.items():
					award_topics.append(topic)
					award_levels.append(level)
			new_award = Award(type = type,
			                   topics = award_topics,
			                   levels = award_levels,
			                   proficiency = proficiency,
			                   winner = this_profile )
			self.save_awards.append(new_award)

	





class Sponsorships():


	def check_all(self):
		self.save_sponsorships = [] # for batch datastore trip
		awards = Award.all().fetch(1000)
		for award in awards:
			self.check_award(award)
			continue
			self.check_taker(qt)
		#db.put(self.save_sponsorships)
		return
			
	def check_award(self,award):
		matching_sponsorships = award.sponsorships
		matching_pledges = pledge_query
		
		# confirm that no sponsorship exists for matching pledges
					



	def notify_sponsor(self,sponsor):
		print "I will email", sponsor, "after checking my RSS feeds"
			
	# Based on awards that have been given, activate scholarships. 
