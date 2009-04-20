from google.appengine.ext import db
from model.proficiency import Proficiency
import logging

MIN_SUBJECT_LENGTH = 10

def get_membership(user, subject):
			from model.user import SubjectMember
			subject_membership = SubjectMember.gql("WHERE user = :1 AND subject = :2", user, subject).get()
			assert subject_membership is not None
			return subject_membership


def get_user_items(user, subject):
	    user_items = []
	    for item in user.authored_items.fetch(1000):
			try: 
				assert item.proficiency.name == subject.name
				user_items.append(item)
				continue
			except: pass
			try: 
				assert item.pending_proficiency.name == subject.name
				user_items.append(item)
				continue
			except: pass	    	
	    return user_items
	    			    		



def get_subjects_for_user(this_user, offset=0): # Can this be refactored?
	"""
	
	This current method places member subjects first, and then loads non-member subjects.
	
	This is just a prototype and a later implementation may be different.
	
	"""	
	memberships = this_user.member_subjects.fetch(100) 
	member_subjects = []
	for m in memberships: member_subjects.append(m.subject.name)
	these_subjects = Proficiency.gql("WHERE name IN  :1 AND status = 'public' ORDER BY status, modified DESC", member_subjects).fetch(1000)
	# In case there aren't enough member subjects, add more
	if len(these_subjects) - offset < MIN_SUBJECT_LENGTH: these_subjects = extra_subjects(member_subjects, these_subjects, offset=offset)
	subject_list = []
	if len(these_subjects[offset:offset+5]) > 0: these_subjects = these_subjects[offset:offset+5]
	for s in these_subjects[:5]:
		is_member = False
		for m in memberships:
			if m.subject.name == s.name:
				if m.is_admin: is_member = "admin"
				else: is_member = "contributor"
		subject_list.append({"subject": s, "is_member": is_member})
	return subject_list



def extra_subjects(member_subjects, these_subjects, offset=0): 
	extra_subjects = Proficiency.gql("WHERE status = 'public' ORDER BY status, modified DESC").fetch(100)
	current_count = 0
	for s in extra_subjects:
		if current_count >= MIN_SUBJECT_LENGTH: break
		elif s.name not in member_subjects:
			these_subjects.append(s)
			current_count += 1
		else: continue # subject already in these_subjects
		
	return these_subjects
	


def send_invite(sender, subject_name, email_address):
	import os
	from google.appengine.api import mail
	from accounts.mail import mail_footer, get_sender
	if not mail.is_email_valid(email_address):
		logging.warning("%s is not a valid email", email_address)
		return False
	message = mail.EmailMessage()
	message.sender = get_sender()
	message.subject = sender.fullname + "has invited you to contribute quiz material" 
	message.to = email_address
	message.body = """


	%s has invited you to contribute to the %s quiz subject at PlopQuiz.com.	
	
	
	
	You can respond to this invitation at the following link:
	
	%s


	Warm Regards,

	James 
	Team PlopQuiz	




	%s





	""" % (sender.fullname, subject_name, "http://" + str(os.environ['HTTP_HOST']) + "/subject/" + subject_name, mail_footer())



	message.send()


