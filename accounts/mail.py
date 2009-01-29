import logging
from .model.user import Profile
from google.appengine.api import mail



### For support, use self.request.headers['User-Agent']
### For feedback forms, etc. use user info.


def mail_intro_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.warning("%s is not a valid email", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "Welcome to PlopQuiz!" 
	message.to = profile.email
	if len(profile.fullname) < 1: user_name = "PlopQuiz User"
	else: user_name = profile.fullname
	message.body = """

	%s,
	
	Welcome to PlopQuiz!
	
	Your academic profile on PlopQuiz.com will help you demonstrate your knowledge about emerging subjects of public interest.
	
	Each quiz you take is a new chance for you to add awards to your academic profile and compete for sponsorships from our community organizations.
	
	
	
	If there's anything we can help you with, e-mail support@plopquiz.com or call us at (650) 353-2694. 
	
	
	
	Warm Regards,

	James 
	Team PlopQuiz	
	
	
	
	
	%s
	

	

	
	""" % (user_name, mail_footer())


	
	message.send()


	


def mail_sponsor_message(sponsor, award):
	sponsee = award.winner
	logging.debug("sending e-mail to %s", sponsor.email)
	if not mail.is_email_valid(sponsor.email):
		logging.error("%s is not valid", sponsor.email)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "Your PlopQuiz sponsorship has been awarded!" 
	message.to = sponsor.email
	message.body = """

	%s,
	
	Your PlopQuiz sponsorship has been earned by a student!
	
	%s has been awarded a sponsorship from your organization for exceptional performance in the %s quiz subject "
	
	You can visit this student's profile at %s
	
	You can view the sponsorship on your profile at %s
	

	%s
	""" % (sponsor.fullname, sponsee.fullname, upper(award.proficiency), 
	        "http://" + str(os.environ['HTTP_HOST']) + "profile/" + sponsee.profile_path,
	        "http://" + str(os.environ['HTTP_HOST']) + "sponsors/" + sponsor.profile_path,
	      mail_footer())

	message.send()


	
	
	


def mail_sponsee_message(sponsee, sponsor):
	logging.debug("sending e-mail to %s", sponsee.email)
	if not mail.is_email_valid(sponsee.email):
		logging.error("%s is not valid", sponsee.email)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "You've earned a PlopQuiz sponsorship!"
	message.to = sponsee.email
	from model.employer import Employer
	this_business = Employer.get_by_key_name(sponsor.unique_identifier)
	sponsor_message = this_business.sponsorship_message
	if sponsor_message is None:
		sponsor_message = this_business.default_message()
	message.body = """
 
	%s,
	
	You've earned a PlopQuiz sponsorship from %s for the %s quiz subject!
	
	Here is a message from %s: 
	
	-------------------------------------------------------------------
	
	
	
	%s
	
	
	
	-------------------------------------------------------------------
	
	This sponsorship is now on your profile: %s 
	
	This sponsorship is now on the profile of %s: %s
	
	
	%s
	
    
	
	""" % (sponsee.fullname, sponsor.fullname, upper(award.proficiency), sponsor.fullname, sponsor_message, 
	       "http://" + str(os.environ['HTTP_HOST']) + "profile/" + sponsee.profile_path,
	       sponsor.fullname,
	       "http://" + str(os.environ['HTTP_HOST']) + "sponsors/" + sponsor.profile_path,
	       mail_footer())

	message.send()








def new_years_message():
	from model.account import MailingList
	peoples = MailingList.all().fetch(1000)


	from utils.utils import ROOT_PATH
	file = open(ROOT_PATH + "/data/new_years.pdf")
	pdf_str = file.read()
	
	for p in peoples: 
		message = mail.EmailMessage()
		message.sender = get_sender()
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
	












def mail_sponsor_intro(profile):
	import os
	if not mail.is_email_valid(profile.email):
		logging.warning("%s is not a valid email", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "Your PlopQuiz Community Sponsor Application" 
	message.to = profile.email
	if len(profile.fullname) < 1: user_name = "PlopQuiz User"
	else: user_name = profile.fullname
	message.body = """

	%s,
	
	
	Good news! PlopQuiz has accepted your Community Sponsor application.
	
	Your new role as a PlopQuiz Community Sponsor is a chance to connect with motivated learners and show your support for issues of public interest.
	
	Members of your organization can use this private link to sign in to your account:
	
	%s
	
	
	
	Once signed in, you can edit your profile, view your sponsorships, and configure your sponsorship settings.
	
	If there's anything we can help you with, e-mail support@plopquiz.com or call us at (650) 353-2694. 
	
	
	
	Warm Regards,

	James 
	Team PlopQuiz
	
	
	%s

	
	""" % (user_name, 
	"http://" + str(os.environ['HTTP_HOST']) + "/login?reset=" + str(profile.key()),
	 mail_footer())


	
	message.send()









def reset_account_access(user):
	import os
	logging.debug("sending e-mail to %s", user.email)
	if not mail.is_email_valid(user.email):
		logging.error("%s is not valid", user.email)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "Reset Access to Your PlopQuiz Account"
	message.to = user.email
	
	



	message.body = """
 
	%s,
	
	You have requested to reset access to your PlopQuiz account.
	
	Visit this address to link your PlopQuiz account to a listed OpenID provider.

	
	%s
	
	
	
    %s
	
	""" % (user.fullname, 
	"http://" + str(os.environ['HTTP_HOST']) + "/login?reset=" + str(user.key()), 
	mail_footer())

	message.send()
	return True




def mail_footer(): #Todo: unsubscribe
	footer = """
	-------------------------------------------------------------------
	
	Thanks For Using PlopQuiz! /  http://www.plopquiz.com

	
	
	"""
	
	return footer 







def get_sender():
	return "plopquiz@plopquiz.com"
