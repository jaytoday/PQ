import logging
logging.info('Loading %s', __name__)
from .model.user import Profile
from google.appengine.api import mail

# We need to verify that email works with Facebook and Myspace users.


# This should be used when a user logs in for the first time. 


### For support, use self.request.headers['User-Agent']
### For feedback forms, etc. use user info.


def mail_intro_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.error("%s is not valid", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = "notify@plopquiz.com"
	message.subject = "Welcome to Plopquiz!" 
	message.to = profile.email
	
	message.body = """

	Your name is below!
	
	Here's what you can do with PlopQuiz
	
	
	Try to use the latest version of Firefox. 
	
	Remember how to login
	
	Contact us. Have fun. 
	

	%s
	""" % profile.fullname

	message.send()


	


def mail_sponsor_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.error("%s is not valid", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = "notify@plopquiz.com"
	message.subject = "Your sponsorship has been awarded!" 
	message.to = profile.email
	
	message.body = """

	Your sponsorship has been awarded!
	
	

	%s
	""" % profile.fullname

	message.send()


	
	
	


def mail_sponsee_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.error("%s is not valid", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = "notify@plopquiz.com"
	message.subject = "You've earned a sponsorship!" 
	message.to = profile.email
	
	message.body = """

	You've earned a sponsorship!
	
	

	%s
	""" % profile.fullname

	message.send()

