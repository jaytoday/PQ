import logging
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext import db
from .utils.utils import ROOT_PATH
from utils.BeautifulSoup import BeautifulStoneSoup
import random
from model.dev import Setting
from google.appengine.api import memcache


class Fixture():
		
	# first job
	def load(self):
		save = []
		logging.info('loading fixture')
		self.fixture_offset = Setting.get_by_key_name('fixture_offset')  
		if self.fixture_offset.status == "update_stats": #instead of 'create_account'
			logging.warning('Load Fixtures Cron Job Hit Twice In a Row')
			print "error -- current status: ", self.fixture_offset.status
			return False
		this_account, this_user, this_quiz_taker = self.get_fixture()
		scores = Scores()
		import random
		correct_prob = random.randint(80,95)
		FIXTURE_PROFICIENCY = self.get_fixture_subject()
		from model.proficiency import Proficiency 
		this_proficiency = random.sample( Proficiency.gql("WHERE status = 'public'").fetch(1000), 1 )[0]
		save_scores = scores.make_scores(this_user, this_proficiency, correct_prob, SCORE_NUM = 10) 
		memcache.set('current_fixture', ( this_account, this_user, this_quiz_taker ), 600000)
		self.fixture_offset.status = "update_stats"
		print this_user.nickname
		save.append(self.fixture_offset)
		save.extend(save_scores)
		db.put(save)
		# open fixture.xml, go to offset.
		# load one name, email pair. register. 

		FIXTURE_PROFICIENCY = self.get_fixture_subject()
		

	def get_fixture_subject(self):
		try:
			fixture_subject = Setting.get_by_key_name('fixture_subject').status
			from model.proficiency import Proficiency
			return Proficiency.get_by_key_name(fixture_subject)
		except:
			DEFAULT_SUBJECT = "Smart Grid"
			logging.error('unable to load fixture subject - returning default: %s', DEFAULT_SUBJECT)
			return DEFAULT_SUBJECT
	
	def get_fixture(self):
		fixture_file = open(ROOT_PATH + "/data/fixtures.xml")
		fixtures = BeautifulStoneSoup(fixture_file.read())
		this_name = fixtures.findAll('record')[int(self.fixture_offset.value)].contents[1].contents[0]
		this_email = fixtures.findAll('record')[int(self.fixture_offset.value)].contents[3].contents[0]
		return self.create_user(str(this_name), str(this_email))
		
		
		

		
	def create_user(self, name, email):
		from accounts.methods import register_user, register_qt, register_account
		logging.info('Creating New User With Nickname %s', name)
		this_user = {}
		this_user['nickname'] = name
		this_user['fullname'] = this_user['nickname']
		this_user['email'] = email
		this_user['unique_identifier'] = str(name)
		this_user['account'] = register_account(this_user['unique_identifier'], this_user['nickname'])
		this_user['user'] = register_user(this_user['unique_identifier'], this_user['nickname'], this_user['fullname'], this_user['email'])
		this_user['quiz_taker'] = register_qt(this_user['unique_identifier'], this_user['nickname'])
		print this_user['account'].unique_identifier, this_user['user'].unique_identifier, this_user['quiz_taker'].unique_identifier
		return this_user['account'], this_user['user'], this_user['quiz_taker']




	# second job
	def update_stats(self):
	  save = []
	  self.fixture_offset = Setting.get_by_key_name('fixture_offset') 
	  if self.fixture_offset.status != "update_stats":
		   logging.warning('Update Stats Job Hit Twice In A Row')
		   print "error -- current status: ", self.fixture_offset.status
		   return False
	  (this_account, this_user, this_quiz_taker) = memcache.get('current_fixture')
	  logging.info('Updating User Stats for User %s', this_user.unique_identifier)
	  from quiztaker.methods import ProficiencyLevels
	  pl = ProficiencyLevels()
	  pl.set_for_user(this_quiz_taker)
	  from accounts.methods import Awards
	  awards = Awards()
	  # check for new awards
	  new_awards = awards.check_all(this_quiz_taker)
	  from accounts.methods import Sponsorships
	  sponsorships = Sponsorships()
	  # check for new sponsorships, both personal and business
	  new_sponsorships = sponsorships.check_user(this_user)
	  self.fixture_offset.value += 1
	  self.fixture_offset.status = "create_account"
	  save.append(self.fixture_offset)
	  db.put(self.fixture_offset)
	  return new_awards, new_sponsorships



  	
  	
  	
class Scores():
	  	
  def make_scores(self, this_user, this_proficiency, correct_prob, SCORE_NUM = 10):
  	self.correct_prob = correct_prob
  	self.correct_scores = 0  	
  	from model.quiz import QuizItem
  	items = QuizItem.gql("WHERE proficiency = :1", this_proficiency).fetch(1000)
  	items = random.sample(items, SCORE_NUM)
  	self.save = []
  	for i in items: 
  	    self.make_score(i, this_user) 
  	print "saved ", len(self.save), " scores. ", self.correct_scores, " were correct." 
  	return self.save
  	

  def make_score(self, i, this_user): 
	from model.quiz import QuizTaker
	from model.quiz import ItemScore
	import random
	this_user = QuizTaker.get_by_key_name(this_user.unique_identifier)
	picked_answer = ''
	if random.randint(1,100) > self.correct_prob: #wrong answer -- could also just use normal distribution of correct probability
		while picked_answer == i.index: picked_answer = i.answers.pop()
	else:  picked_answer = i.index
	score = ItemScore(quiz_item = i,
						  quiz_taker = this_user,
						  correct_answer = i.index,
						  picked_answer = picked_answer,
						  type = "stub")	
	if score.picked_answer == score.correct_answer: 
		this_score = int(random.normalvariate(int( self.correct_prob ), 15))
		if this_score > 99: this_score = 99
		score.score = this_score
		self.correct_scores += 1
	else: score.score = 0
	self.save.append(score)
  	

  	
