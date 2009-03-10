from google.appengine.ext import db


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
	from model.proficiency import Proficiency
	#from model.user import SubjectMember
	memberships = this_user.member_subjects.fetch(1000) 
	member_subjects = []
	for m in memberships: member_subjects.append(m.subject.name)
	these_subjects = Proficiency.gql("WHERE name IN  :1 ORDER BY modified DESC", member_subjects).fetch(1000)[offset:offset+5] 
	subject_list = []
	for s in these_subjects:
		is_member = False
		for m in memberships:
			if m.subject.name == s.name:
				if m.is_admin: is_member = "admin"
				else: is_member = "contributor"
		subject_list.append({"subject": s, "is_member": is_member})
	return subject_list 
