import logging
from utils.gql_encoder import GqlEncoder, encode
from google.appengine.ext import db
from google.appengine.api import memcache
from google.appengine.api import mail
from accounts.mail import mail_footer, get_sender
from model.account import MailingList


class Mail():
		
	def send_message(self, mail_type):
		self.mail_type = mail_type
		save = []
		logging.info('sending message')
		(mail_queue, next_recipient) = self.get_next_recipient()
		if not next_recipient: return "Mailout Is Finished"
		m = Messages()
		if mail_type == "beta": m.beta_message(next_recipient)
		elif mail_type == "pq": m.pq_message(next_recipient)
		else: logging.warning('no message specified!')
		logging.info('sent %s message to %s' % (mail_type, next_recipient.fullname) )
		memcache.set(self.mail_type, mail_queue)
		#print "sent ", mail_type, " message to ", next_recipient.fullname - REDUNDANT?
		return str("sent " + mail_type + " message to " +  next_recipient.fullname)
		



	def get_next_recipient(self):
		mail_queue = memcache.get(self.mail_type)
		if mail_queue is None: # doesn't exist yet
		    logging.info('creating mail queue')
		    mail_queue = MailingList.gql("WHERE type = :1", self.mail_type).fetch(1000)
		    memcache.set(self.mail_type, mail_queue) 
		if len(mail_queue) < 1: 
		    memcache.delete(self.mail_type)
		    print "Mailout Is Finished"
		    return False, False
		return mail_queue, mail_queue.pop()
		
		
		


  	
  	
  	
class Messages():
	  	

  def beta_message(self, recipient):

	from utils.utils import ROOT_PATH
	file = open(ROOT_PATH + "/data/new_years.pdf")
	pdf_str = file.read()

	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "A Holiday Greeting from PlopQuiz!" 
	message.to = recipient.email
	
	message.body = """
	
	Hello? Hello? Testing....
	
	
	%s,
	
	I'm sending this email from a program I wrote in a computer language called Python, and 
	the program is being compiled in a Google server farm located in Iowa. 
	
	Not impressed? Well, you are still reading this, so I'll take that as a good sign.
	
	I may have told you about a website I'm working on called PlopQuiz. 
	
	While it will be a little while until the site is ready for public usage, 
	I wanted to give you a peek at what we've got under construction.
	
	You can take a quiz at http://blog.plopquiz.com. Use Firefox 3 if possible.
	
	This company blog is actually run from a different server than the main PlopQuiz site, and it shows how our new ability to 
	administer quizzes "cross-domain" will open up some new possibilities for how we can distribute quizzes.
	
	If you browse down you should see a little "widget" with a "Misconceptions" header and a button saying "Take Quiz" on it.
	
	The topic of the quiz (popular misconceptions) probably won't be too much like the other 
	subjects we'll be publishing this spring, but at least it will give you an idea of what it's like to take a quiz. 
	
	After taking the quiz, you'll be prompted to login (you can use an account with any of the displayed services). 
	
	You'll then be redirected to your profile.  We lowered our grading standards for now, so it's very likely that you 
	may have won an award or sponsorship.
	
	There's not much else you can do with the site right now, but we'd like to begin getting feedback as early as possible.
	
	Here are some specific questions that we'd be interested in hearing feedback on:
	
	
	*  What do you think the PlopQuiz website does? Who is it for? 
	
	*  Would you ever have use for a site like PlopQuiz? What would be needed for it to be useful for you?
	
	*  What do you predict would be the biggest challenge of this website?
	
	
	
	You can respond to this e-mail, or you can reach me at james@plopquiz.com. 
	

	Be well, and good luck in the new year.
	


   -- James

	
	""" % recipient.fullname
	message.attachments = [("PlopQuiz_News_Years_Resolution.pdf", pdf_str)]
	message.send()




  def pq_message(self, recipient):

	from utils.utils import ROOT_PATH
	file = open(ROOT_PATH + "/data/new_years.pdf")
	pdf_str = file.read()

	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "A Holiday Greeting from PlopQuiz!" 
	message.to = recipient.email
	
	message.body = """
	
	Hello? Hello? Testing....
	
	
	%s,
	
	I'm sending this email from a program I wrote in a computer language called Python, and 
	the program is being compiled in a Google server farm located in Iowa. 
	
	Not impressed? Well, you are still reading this, so I'll take that as a good sign.
	
	I may have told you about a website I'm working on called PlopQuiz. 
	
	While it will be a little while until the site is ready for public usage, 
	I wanted to give you a peek at what we've got under construction.
	
	You can take a quiz at http://blog.plopquiz.com. Use Firefox 3 if possible.
	
	This company blog is actually run from a different server than the main PlopQuiz site, and it shows how our new ability to 
	administer quizzes "cross-domain" will open up some new possibilities for how we can distribute quizzes.
	
	If you browse down you should see a little "widget" with a "Misconceptions" header and a button saying "Take Quiz" on it.
	
	The topic of the quiz (popular misconceptions) probably won't be too much like the other 
	subjects we'll be publishing this spring, but at least it will give you an idea of what it's like to take a quiz. 
	
	After taking the quiz, you'll be prompted to login (you can use an account with any of the displayed services). 
	
	You'll then be redirected to your profile.  We lowered our grading standards for now, so it's very likely that you 
	may have won an award or sponsorship.
	
	There's not much else you can do with the site right now, but we'd like to begin getting feedback as early as possible.
	
	Here are some specific questions that we'd be interested in hearing feedback on:
	
	
	*  What do you think the PlopQuiz website does? Who is it for? 
	
	*  Would you ever have use for a site like PlopQuiz? What would be needed for it to be useful for you?
	
	*  What do you predict would be the biggest challenge of this website?
	
	
	
	You can respond to this e-mail, or you can reach me at james@plopquiz.com. 
	

	Be well, and good luck in the new year.
	


   -- James

	
	""" % recipient.fullname
	message.attachments = [("PlopQuiz_News_Years_Resolution.pdf", pdf_str)]
	message.send()






