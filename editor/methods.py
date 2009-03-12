from google.appengine.ext import db
from model.proficiency import Proficiency
import logging

MIN_SUBJECT_LENGTH = 5

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
	
	memberships = this_user.member_subjects.fetch(1000) 
	member_subjects = []
	for m in memberships: member_subjects.append(m.subject.name)
	these_subjects = Proficiency.gql("WHERE name IN  :1 AND status = 'public' ORDER BY status, modified DESC", member_subjects).fetch(1000)[offset:offset+5] 
	# In case there aren't enough member subjects, add more
	if len(these_subjects) < MIN_SUBJECT_LENGTH: these_subjects = extra_subjects(member_subjects, these_subjects)
	subject_list = []
	for s in these_subjects:
		is_member = False
		for m in memberships:
			if m.subject.name == s.name:
				if m.is_admin: is_member = "admin"
				else: is_member = "contributor"
		subject_list.append({"subject": s, "is_member": is_member})
	return subject_list 



def extra_subjects(member_subjects, these_subjects, offset=0): 
	extra_count = MIN_SUBJECT_LENGTH - len(these_subjects)
	extra_subjects = Proficiency.gql("ORDER BY modified DESC").fetch(1000)[offset:offset+5] 
	current_count = 0
	for s in extra_subjects:
		if current_count >= extra_count: break
		elif s.name not in member_subjects:
			these_subjects.append(s)
			logging.info('adding %s to subjects', s.name)
			current_count += 1
		else: continue # subject already in these_subjects
		
	return these_subjects
	
