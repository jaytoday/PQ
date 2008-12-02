import logging
import random
from google.appengine.ext import db
from utils import *
from model.quiz import QuizItem, ItemScore, QuizItemFilter, QuizTakerFilter, ItemScoreFilter
from model.user import QuizTaker 
import string

# This program calculate the degrees of difficulty and degree of proficiency as well as the consistencies of the quiz items and the quiz takers.
# Note: Difficulty, Proficiency are normalized to range from 0 to RANGE_MAX = 10,000
# Fuzzy logic is used ranging from 0 to RANGE_MAX. 0 = false RANGE_MAX = true. intermediate values are allowed.


# DEFINE GLOBAL CONSTANTS

CONVERGENCE_RATIO = 100	# Used to determine termination criterion. At first count, converge_min = converge / CONVERGENCE_RATIO
COUNT_MAX = 200			# Maximum number of times the whole score set is scanned
DAMPING = 1             # value 1 is fastest convergence assuming no nonlinearities. Larger values slow convergence but deal with non-linearities.
RANGE_MAX = 100 		# maximum range for difficulty and proficiency
RANGE_HALF = RANGE_MAX / 2 # half of RANGE_MAX. Used in initialization
NOISE_AMP = 0           # noise amplitude for simulated annealing


class Run_Filter():
	
	# Any of these variables that never change should be global constants
	
	def __init__(self):                 # initialize variables
		self.converge = 0			# Measure of convergence, accumulation of residuals during a cycle.
		self.converge_min = 0		# minimum convergence value at termination of algorithm. Is automatically set in program converge_min = converge / CONVERGENCE_RATIO
		self.count = 0				# Number of of times the whole score set is scanned
		self.residual = 0            # Difference between measured score and expected score
		self.gain = 0                # gain to be applied to residual
		self.annealing = 0           # noise to be applied to residual to achieve simulated annealing, finding global optimum
		self.nudge_difficulty = 0    # amount of nudge allocated to difficulty
		self.nudge_proficiency = 0   # amount of nudge allocated to proficiency
		self.temp = 0                # temporary buffer
		self.last_cycle = False      # last cycle flag is used to terminate optimization and to store the last residuals in takers and items
		self.item_variance = 0       # temporary holds intermediate variance calculations
		self.taker_variance = 0      # temporary holds intermediate variance calculations
		self.expected_score = 0      # expected score by quiz taker given the item difficulty and the taker's proficiency
		self.count = 0				# holds the numbe oftimes the whole score set is passed through the Falman filter.

	def create_filter(self, entity, filter_type, reference):
		print "creating filter"
		new_filter = filter_type(reference = entity)
		new_filter.put()
		return  
	
			
	def get_scores(self):    
			# DATABASE REQUIREMENTS
			# INPUT AND INITIALIZE SCORE DATA    
			# If this data could be used across batches, it would be better to do it only once, so we can reduce datastore lookups.
			# Filters need to be initiated.  
		
			scores = ItemScore.all().fetch(1)
			quiz_items = []
			quiz_takers = []
			for s in scores:
			  if not s.quiz_taker or not s.quiz_item:
				scores.remove(s)
				#s.delete() 
				logging.error('score missing reference data')
				logging.error(s)
				continue
				
			# Is it necessary to generate three seperate lists, or can we just create a list of scores?				
				
			  if not s.quiz_taker.filter.get(): self.create_filter(s.quiz_taker, QuizTakerFilter, 'quiz_taker')# reset filter for quiz taker (training=False, etc.)
			  if not s.quiz_item.filter.get(): self.create_filter(s.quiz_item, QuizItemFilter, 'quiz_item')
			  if not s.filter.get(): self.create_filter(s, QuizItemFilter, 'score')
			  # reset filter for quiz_item
			  quiz_takers.append(s.quiz_taker)
			  quiz_items.append(s.quiz_item)
			quiz_takers = set(quiz_takers)    # only unique entries
			quiz_items = set(quiz_items)
			for score in scores:
				score.residual = 0
				score.trained = 0	# REMOVE THIS INITIALIZATION AFTER TRAINING FIRST BATCH
				continue
			
			return scores
				

	def Initalize_Kalman_Batch(self, items, takers):
			# SHUFFLE??
			# Need to shuffle score list (or index list pointing to score list) every cycle to achieve unbiased convergence.
			# Use the function shuffle( seq[, random])
			# If computing cost of shuffle is too high apply shuffle every 10 times i.e., if ((count % 10) = 0): shuffle( seq[, random]) # modulus operator: %

			# Reset all nudge counts for the next cycle  - this can be done from datastore model. 
			
			for item in items:
				item.filter.nudges_count = 0         			# set first nudge count to 0.

			for taker in takers:
				taker.filter.nudges_count = 0            		# set first nudge count to 0.
			return        	
				
				
	def Compute_Residuals(self, score):
				# expected score = (proficiency level - difficulty + Range Max) / 2
				print score.topic_level()
				expected_score = score.topic_level().topic_level
				residual = score.score - expected_score 	# Residual or Innovation; +ive Residual means performance better than expected
				return expected_score, residual


	def Apply_Nudge_Difficulty(self, item, one_more_nudge):
						item.filter.nudges_count += 1                				# accumulate number of nudges.
						# Allocate nudge to difficulty and proficiency
						# Note: nudge_count + 1 insures that on the first cycle the nudge is distributed equally 50/50 to diff and prof.
						# Note: quiz_item.nudges_count is a measure of the variance of quiz_item during the optimization process and allows weighing of new information. 
						# Note: quiz_taker.nudges_count is a measure of the variance of quiz_taker during the optimization process  and allows weighing of new information.
						nudge_difficulty = self.gain * ( self.residual  + self.annealing ) / (item.filter.nudges_count + one_more_nudge) # Compute nudge allocation equally between diff and prof.

						# Update Difficulty
						temp = item.difficulty - self.nudge_difficulty          # Apply correction to difficuly.
						item.filter.difficulty = max(RANGE_MAX, min(0, self.temp))     # Restrict range (0,10000)


	def Apply_Nudge_Proficiency(self, taker, one_more_nudge):			
						taker.filter.nudges_count += 1                           # accumulate number of nudges. 
						# Allocate nudge to difficulty and proficiency
						# Note: nudge_count + 1 insures that on the first cycle the nudge is distributed equally 50/50 to diff and prof.
						# Note: quiz_item.nudges_count is a measure of the variance of quiz_item during the optimization process and allows weighing of new information. 
						# Note: quiz_taker.nudges_count is a measure of the variance of quiz_taker during the optimization process  and allows weighing of new information.
						nudge_proficiency = self.gain * ( self.residual  + self.annealing ) / (taker.filter.nudges_count + one_more_nudge) # ompute nudge allocation equally between diff and prof.

						# Update Proficiency
						temp = taker.proficiency + nudge_proficiency      # Apply correction to difficuly.
						taker.proficiency = max(RANGE_MAX, min(0, temp))	# <-- ERROR!!!! taker.proficiency doesn't resolve to anything. See the e-mail I sent you. Restrict range (0,10000)

											
	def Collect_Residual_Stats(self, item, taker):
					score.residual = self.residual               # for monitoring, accumulate in residual of quiz item all relevent residuals

					# compute means for residuals associated with quiz items and quiz takers.
					item.filter.mean += (self.residual - item.filter.mean) / item.filter.nudges_count
					taker.filter.mean += (self.residual - taker.filter.mean) / taker.filter.nudges_count

					#compute manhattan
					item.filter.manhattan += abs(self.residual)      # accumulate absolute value of residuals
					taker.filter.manhattan += abs(self.residual)     # accumulate absolute value of residuals					
						
							
									
	def Kalman_Single_Score(self, score):

				self.Compute_Residuals(score)
															# Residual ranges +10000, -10000
				self.converge = max(1073741824, self.converge + abs(self.residual)) 	# Convergence monitor. Saturates at 2**30. Max at 2**32
				self.gain = DAMPING/(DAMPING + self.count)			# Gain decrease on each successive pass through the scores to iron out the discrepancies. 
				self.annealing = NOISE_AMP * random.uniform(0, ((COUNT_MAX - self.count)/COUNT_MAX) * RANGE_MAX/10) 	# annealing is a random number ramping down from RANGE_MAX/10

				print score.quiz_item.filter.get()
				return 
				if (score.quiz_item.filter.trained == False ):
					if ( score.quiz_taker.filter.trained == False ):
						self.Apply_Nudge_Difficulty(1)
						self.Apply_Nudge_Proficiency(1)	
					else:																	# quiz_taker[taker_index].trained == True 
						self.Apply_Nudge_Difficulty(0) 
						nudge_proficiency = 0
				else:
					if (score.quiz_taker.filter.trained == False ):     
						nudge_difficuly = 0                
						self.Apply_Nudge_Proficiency(0)	                                    
					else:
						nudge_difficulty =  0
						nudge_proficiency = 0                           # Both item and taker are trained. No update necessay


				# Collect Info for monitoring purposes
				if self.last_cycle: 
					self.Collect_Residuals_Stats()
					score.quiz_taker.filter.trained = True
					score.quiz_item.filter.trained = True
					score.filter.trained = True     			# increment score usage. Used in sorting scores before processing. Use youngest scores first


	def Collect_Variance_Stats(self):
			#compute variances. Variances have already been initialized to zero.                                           
			for score in scores:
				score.quiz_item.filter.variance += (score.filter.residual - score.quiz_item.filter.mean)**2
				score.quiz_taker.filter.variance += (score.filter.residual - score.quiz_taker.filter.mean)**2
				
				# George, the indentation on these last two had them outside the for-loop, but that would result in an error.
				score.quiz_item.filter.variance = score.quiz_item.filter.variance /( score.quiz_item.filter.nudges_count -1)
				score.quiz_taker.filter.variance = score.quiz_taker.filter.variance /( score.quiz_taker.filter.nudges_count -1)  


def run():
	filter = Run_Filter()
	scores = filter.get_scores()
	filter.converge = filter.converge_min + 1
        # Optimization Main Iterative Loop            
	while ( filter.last_cycle == False ):	
		filter.last_cycle =  ( filter.converge < filter.converge_min ) or ( filter.count >= COUNT_MAX ) # Set last cycle flag on last cycle
		filter.converge = 0	        # Initialize convergence for quiz items
		# is this necessary? filter.Initalize_Kalman_Batch(quiz_items, quiz_takers)
		for score in scores:
			filter.Kalman_Single_Score(score) # Scan all measured scores
			continue
 
                      
        # On the first cycle compute converge_min as a ratio of initial converge value                        
		if filter.count == 0:
			filter.converge_min = max( 1, (filter.converge / CONVERGENCE_RATIO) ) # set converge_min to a fraction of first converge value.
		filter.count += 1 	# increment loop count. Used in terminating the optimization porcess
                                            
	if filter.last_cycle: filter.Collect_Variance_Stats()
	
		# Put back in the database the following

		# score.quiz_item.difficulty = 0          # Difficulty of a Quiz item for a given score
		# score.quiz_item.trained = False         # True if item has gone through an optimization. Used to freeze difficulty when new data is presented
		# score.quiz_item.consistency = 0            # to be put back into the DB. This is a measure of consistency. Low value is most consistent

		# score.quiz_taker.proficiency            # Proficiency of a Quiz Taker of a given score
		# score.quiz_taker.trained                # True if item has gone through an optimization. Used to freeze proficiency when new data is presented 
		# score.quiz_taker.consistency            # to be put back into the DB. This is a measure of consistency. Low value is most consistent
 
        #
# end of algorithm






# Following program is needed to monitor the performance of the optimization program
def monitor():
	pass
# Requirements:
# As algorithm runs:
# display "converge"

# At the end of the algorithm (using last_cycle flag):
# Display means, variances and manhattans, for each quiz item and for each quiz taker.
# Display should be in sorted fashion, in columns of pairs, for example, (quiz_taker, mean) or (quiz_item, manhattan)
# with highest values on top of the sort
#
                                            
#


                                           
