import logging
logging.info('Loading %s', __name__)
from .model.user import Profile
from google.appengine.api import mail

# We need to verify that email works with Facebook and Myspace users.

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
	
	
	Try to use the latest version of Firefox. 
	

	%s
	""" % profile.fullname

	message.send()
	print "sent message: ", message.body


	
