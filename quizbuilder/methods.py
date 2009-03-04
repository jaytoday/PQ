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
	    			    		
