import logging
import cgi
from .model.user import QuizTaker, ProficiencyLevel, TopicLevel
from .model.quiz import ItemScore
from google.appengine.ext import db
#from decimal import Decimal, ROUND_HALF_UP


# TODO: Much better documentation/logging!!

class TopicLevelData():               
    def get(self, quiz_taker):
    	return quiz_taker.topic_levels
                                                            


    def set(self, quiz_taker, save=False):
		save = []
		topic_scores = {}
		edited_scores = False
		total_scores = 0
		for this_score in quiz_taker.itemscores:
			total_scores += 1
			try: 
				
				current_average = topic_scores[this_score.quiz_item.topic.key()]['average']
				current_count = topic_scores[this_score.quiz_item.topic.key()]['count']
				current_product = current_average * current_count
				new_sum = current_product + this_score.score
				if this_score.score > 99: 
					logging.warning('perfect score warning! score: %d', this_score.score)
					this_score.score = 99
				new_count = current_count + 1
				new_average = new_sum / new_count

			except:# no current average
				try: topic_scores[this_score.quiz_item.topic.key()] = {}
				except: 
				    logging.warning('no topic for quiz item: %s', this_score.quiz_item.key())
				    continue # Reference Property error for old scores. 
				new_count = 1
				new_average = this_score.score
				
			topic_scores[this_score.quiz_item.topic.key()]['count'] = new_count
			topic_scores[this_score.quiz_item.topic.key()]['average'] = new_average
		
		logging.info('processing %d item scores for user %s' % ( total_scores, quiz_taker.unique_identifier )  )
		
		for topic_pair in topic_scores.items():
			tl_keyname = str(quiz_taker.unique_identifier) + "_" + str(topic_pair[0])
			topic_pair[1]['average'] = int(topic_pair[1]['average'])
			topic_level = TopicLevel.get_by_key_name(tl_keyname)
			if not topic_level: 
			    topic_level = TopicLevel(key_name = tl_keyname,
										topic = topic_pair[0],
										quiz_taker = quiz_taker)
										
			topic_level.topic_level = topic_pair[1]['average']
			logging.info('new topic level for user %s is %s' % (topic_level.quiz_taker.unique_identifier, topic_level.topic_level )  )
			save.append(topic_level)
		if save: db.put(save)
		return save
			
			 
			
		
			
		  
					

        	
class ProficiencyLevelData():               
    def get(self, quiz_taker):
    	return quiz_taker.proficiency_levels

                                                            


    def set(self, quiz_taker, save=False):
		logging.info('setting proficiency level data for %s', quiz_taker.unique_identifier)
		save = []
		pro_scores = {}
		for tl in quiz_taker.topic_levels.fetch(1000):
			try: 
				current_average = pro_scores[tl.topic.proficiency.key()]['average']
				current_count = pro_scores[tl.topic.proficiency.key()]['count']
				current_product = current_average * current_count
				new_sum = current_product + tl.topic_level
				new_count = current_count + 1
				new_average = new_sum / new_count				
			except: # no current average
				pro_scores[tl.topic.proficiency.key()] = {}
				new_count = 1
				new_average = tl.topic_level
			pro_scores[tl.topic.proficiency.key()]['count'] = new_count
			pro_scores[tl.topic.proficiency.key()]['average'] = new_average

		for pro_pair in pro_scores.items():
				pl_keyname = str(quiz_taker.unique_identifier) + "_" + str(pro_pair[0])
				pro_pair[1]['average'] = int(pro_pair[1]['average'])
				if ProficiencyLevel.get_by_key_name(pl_keyname):
					proficiency_level = ProficiencyLevel.get_by_key_name(pl_keyname)
					proficiency_level.proficiency_level = pro_pair[1]['average']
				else:
					 proficiency_level = ProficiencyLevel(key_name = pl_keyname,
															proficiency = pro_pair[0],
															quiz_taker = quiz_taker,
															proficiency_level = pro_pair[1]['average'])
				save.append(proficiency_level)
		if save: db.put(save)
		return save
