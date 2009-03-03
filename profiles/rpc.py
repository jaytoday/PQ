import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
from utils import webapp, simplejson
from google.appengine.ext import db
from .utils.utils import tpl_path, ROOT_PATH, raise_error
from utils.gql_encoder import GqlEncoder, encode
from .model.user import ProfilePicture
from google.appengine.api import images

PROFILE_PATH = 'profile/'

class RPCHandler(webapp.RequestHandler):
  # AJAX Handler
  def __init__(self):
    webapp.RequestHandler.__init__(self)
    self.methods = RPCMethods()

 
  def get(self):
    func = None
   
    action = self.request.get('action')
    if action:
      if action[0] == '_':
        self.error(403) # access denied
        return
      else:
        func = getattr(self.methods, action, None)
   
    if not func:
      self.error(404) # file not found
      return
     
    args = ()
    while True:
      key = 'arg%d' % len(args)
      val = self.request.get(ksey)
      if val:
        args += (simplejson.loads(val),)
      else:
        break
    result = func(*args)
    self.response.out.write(simplejson.dumps(result))
    


class RPCPostHandler(webapp.RequestHandler):
  """ Allows the functions defined in the RPCMethods class to be RPCed."""
  def __init__(self):
    webapp.RequestHandler.__init__(self)
    self.methods = RPCMethods()
 
  def post(self):
    args = simplejson.loads(self.request.body)
    func, args = args[0], args[1:]
   
    if func[0] == '_':
      self.error(403) # access denied
      return
     
    func = getattr(self.methods, func, None)
    if not func:
      self.error(404) # file not found
      return

    result = func(*args)
    self.response.out.write(simplejson.dumps(result))
        


class PictureUpload(webapp.RequestHandler):
  def post(self):
  	try:
  		small_image = images.resize(self.request.get("img"), 45, 45)
  		large_image = images.resize(self.request.get("img"), 95, 95)
  		new_image = ProfilePicture(small_image = small_image,
  		                           large_image = large_image)
  		new_image.put()
  		new_image.key_name = str(new_image.key())
  		new_image.put()
  		self.response.out.write(new_image.key_name)
  	except:
  		self.response.out.write('error') 
    
    




class RPCMethods(webapp.RequestHandler):
  """ Defines AJAX methods.
  NOTE: Do not allow remote callers access to private/protected "_*" methods.
  """




  def SubmitPicture(self, *args): #TODO: This can be added to the class below to reduce url mappings
  	try: 
  	    new_pic = db.Blob(args[0])
  	    return new_pic
  	except:
  		return False
  	
  	

class ProfilePost(webapp.RequestHandler): 
  def post(self):    
  	if len(self.request.path.split('/subject_img/')) > 1: return self.response.out.write(self.subject_img() )
  	if self.request.get('action') == 'subject_blurb': return self.response.out.write(simplejson.dumps(  self.subject_blurb()  )) 
  	if self.request.get('action') == 'change_rights': return self.response.out.write(self.change_rights() ) 


  def subject_blurb(self):
      from model.proficiency import Proficiency
      subject_name = self.request.get('subject_name')
      this_subject = Proficiency.get_by_key_name(subject_name)
      if this_subject is None: 
          logging.error('no subject found when saving blurb for subject_name %s ', subject_name)
          return "no subject found"
      this_subject.blurb = self.request.get('new_blurb')
      this_subject.put()
      return "OK"
      
  def subject_img(self):
      subject_name = self.request.path.split('/subject_img/')[1].replace('%20',' ')
      from model.proficiency import Proficiency
      this_subject = Proficiency.get_by_key_name(subject_name)
      new_image = this_subject.new_image(self.request.get('subject_img'))
      db.put(new_image)
      logging.info('saved new image for subject %s' % (this_subject.name))
      from utils.webapp import template
      path = tpl_path(PROFILE_PATH +'/utils/subject_frame.html')
      template_values = {'p': this_subject}
      return template.render(path, template_values)
           
      

  def change_rights(self):
	from model.proficiency import Proficiency
	from model.user import Profile, SubjectMember
	subject_name = self.request.get('subject')
	this_subject = Proficiency.get_by_key_name(subject_name) 
	user = Profile.get_by_key_name(self.request.get('user'))
	this_change = self.request.get('rights_action')
	this_membership = SubjectMember.gql("WHERE subject = :1 AND user = :2", this_subject, user).get()
	if this_change == "make_admin":
		logging.info('make admin')
		this_membership.is_admin = True
	if this_change == "remove_admin":
		this_membership.is_admin = False
	db.put(this_membership)
	logging.info('user %s has had admin status set to %s for subject %s' % (user.unique_identifier, str(this_membership.is_admin), this_subject.name))
	from utils.webapp import template
	path = tpl_path(PROFILE_PATH +'/subject/admin_rights.html')
	template_values = {'p': this_subject}
	return template.render(path, template_values)	
			
		
		

		   
      
