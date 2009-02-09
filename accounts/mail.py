import logging
from .model.user import Profile
from model.account import MailingList
from google.appengine.api import mail
import os


### For support, use self.request.headers['User-Agent']
### For feedback forms, etc. use user info.


def mail_intro_message(profile):
	if not mail.is_email_valid(profile.email):
		logging.warning("%s is not a valid email", profile.email)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = "Your PlopQuiz Account" 
	message.to = profile.email
	if len(profile.fullname) < 1: user_name = "PlopQuiz User"
	else: user_name = profile.fullname
	message.body = """

	%s,
	
	Welcome to PlopQuiz!
	
	Your academic profile on PlopQuiz.com will help you demonstrate your knowledge about emerging subjects of public interest.
	
	Each quiz you take is a new chance for you to add awards to your academic profile and compete for sponsorships from our community organizations.
	
	
		
	
	
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
	""" % (sponsor.fullname, sponsee.fullname, award.proficiency.name.upper(), 
	        "http://" + str(os.environ['HTTP_HOST']) + "profile/" + sponsee.profile_path,
	        "http://" + str(os.environ['HTTP_HOST']) + "sponsors/" + sponsor.profile_path,
	      mail_footer())

	message.send()


	
	
	


def mail_sponsee_message(award, sponsor):
	sponsee = award.winner
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
	
    
	
	""" % (sponsee.fullname, sponsor.fullname, award.proficiency.name.upper(), sponsor.fullname, sponsor_message, 
	       "http://" + str(os.environ['HTTP_HOST']) + "profile/" + sponsee.profile_path,
	       sponsor.fullname,
	       "http://" + str(os.environ['HTTP_HOST']) + "sponsors/" + sponsor.profile_path,
	       mail_footer())

	message.send()










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
	
	Members of your orvybreaks,
       
       Welcome to PlopQuiz!
       
       Your academic profile on PlopQuiz.com will help you demonstrate your knowledge about emerging subjects of public interest.
       
       Each quiz you take is a new chance for you to add awards to your academic profile and compete for sponsorships from our community organizations.
       
       
               
       ganization can use this private link to sign in to your account:
	
	%s
	
	
	
	Once signed in, you can edit your profile, view your sponsorships, and configure your sponsorship settings.
	

	
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
	-----------------------------------------------------------------------------
	
	Visit PlopQuiz at http://www.plopquiz.com
	
    e-mail PlopQuiz: contact@plopquiz.com
	call PlopQuiz: (650) 353-2694
	
	
	"""
	
	return footer 







def get_sender():
	return "plopquiz@plopquiz.com"
