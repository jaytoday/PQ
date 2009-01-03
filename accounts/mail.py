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
		logging.warning("%s is not a valid email", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = "notify@plopquiz.com"
	message.subject = "Welcome to PlopQuiz!" 
	message.to = profile.email
	if len(profile.fullname) < 1: user_name = "PlopQuiz User"
	else: user_name = profile.fullname
	message.body = """

	%s,
	
	Welcome to PlopQuiz!
	
	If you're getting this e-mail, that means you're testing our pre-beta release.
	
	Either that, or we've goofed. 
	
	If that's the case, reply to this e-mail and we'll make sure to not accidently spam you.
	

	

	
	""" % user_name


	
	message.send()


	


def mail_sponsor_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.error("%s is not valid", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = "notify@plopquiz.com"
	message.subject = "Your PlopQuiz sponsorship has been awarded!" 
	message.to = profile.email
	
	message.body = """

	Your sponsorship has been awarded!
	
	

	%s
	""" % profile.fullname

	#message.send()


	
	
	


def mail_sponsee_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.error("%s is not valid", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = "notify@plopquiz.com"
	message.subject = "You've earned a PlopQuiz sponsorship!" 
	message.to = profile.email
	
	message.body = """

	You've earned a sponsorship!
	
	If this wasn't just a test sponsorship, you would be getting a friendly message from your personal or business sponsor.
	
	You had to have at least a decent score to earn the sponsorship, so congratulations! 
	
	

	%s
	""" % profile.fullname

	message.send()





def new_years_message():
	from model.account import MailingList
	peoples = MailingList.all().fetch(1000)


	from utils.utils import ROOT_PATH
	file = open(ROOT_PATH + "/data/new_years.pdf")
	pdf_str = file.read()
	
	for p in peoples: 
		message = mail.EmailMessage()
		message.sender = "notify@plopquiz.com"
		message.subject = "A Holiday Greeting from PlopQuiz!" 
		message.to = p.email
		
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

		
		""" % p.fullname
		message.attachments = [("PlopQuiz_News_Years_Resolution.pdf", pdf_str)]
		message.send()
		print "sent message to ", p.email
	
