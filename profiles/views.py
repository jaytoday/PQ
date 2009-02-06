import logging
# Log a message each time this module get loaded.
logging.info('Loading %s', __name__)
import cgi
import wsgiref.handlers
import datetime, time
from utils.webapp import template
from utils.webapp.util import login_required
from google.appengine.ext import db
from utils import webapp
from utils.utils import ROOT_PATH, tpl_path, memoize, get_flash, set_flash
from utils.random import sort_by_attr
from model.user import Profile, QuizTaker, ProfilePicture



# Template paths
PROFILE_PATH = 'profile/'
REPORT_CARD_LIMIT = 5
CLOUD_LIMIT = 9
TOPIC_LEVEL_MIN = 10

class ViewProfile(webapp.RequestHandler):
  #View a profile
  def get(self):
    template_values = self.get_profile()
    if not template_values: return
    template_values['load'] = 2000 # give 2 seconds to load 
    template_values['profile_js'] = profile_js(template_values)
    path = tpl_path(PROFILE_PATH +'profile_template.html')
    self.response.out.write(template.render(path, template_values))
    

  def get_profile(self):
		profile_stub = self.request.path.split('/profile/')[1].lower()
		profile_path = profile_stub.replace(' ','_')
		import urllib
		user = Profile.gql('WHERE profile_path = :1', urllib.unquote(profile_stub))
		try:
			user = user.get()
			if user.is_sponsor == True: self.redirect('/sponsors/' + user.profile_path) # go to sponsor profile
			logging.info('loading profile of %s for user %s' % (user.profile_path, getattr(self.session['user'], 'profile_path', "?")))
			this_user = user.unique_identifier
		except:
		    logging.info('no profile of %s found for user %s' % (profile_path, getattr(self.session['user'], 'profile_path', "?")))
		    self.redirect('/profile_not_found/') # if no user is found
		    return
		is_profile_owner = False
		if self.session['user']:
		    if user.unique_identifier == self.session['user'].unique_identifier: is_profile_owner = True
		# get report card scores
		qt = QuizTaker.get_by_key_name(user.unique_identifier)
		topic_levels = self.get_topic_levels(qt)
		level_cloud = self.make_cloud(topic_levels[0:CLOUD_LIMIT])
		range = 50
		depth = 50
		# get awards and sponsorships
		from model.account import Award, Sponsorship
		"""
		for s in user.sponsorships.fetch(100): #just temporarily, to test for referenceproperty errors.
			try: s.sponsor.photo.key()
			except: 
			    s.delete()
		"""
		return { 'user': user, 'profile_owner': is_profile_owner,  'top_levels': topic_levels[0:REPORT_CARD_LIMIT],
		        'level_cloud': level_cloud, 'flash_msg': get_flash(),
		        'range': range, 'depth': depth, 'level_msg': self.level_msg, 'scroll': self.set_scroll(user) }


      
  def get_topic_levels(self, qt):
      try: all_topic_levels = qt.topic_levels.fetch(100)
      except: # no topic levels set
          all_topic_levels = None
      public_topic_levels = []
      if all_topic_levels: public_topic_levels = [t for t in all_topic_levels if t.topic_level > TOPIC_LEVEL_MIN]
      self.level_msg = False
      if len(public_topic_levels) < 4: 
          self.level_msg = True
      return sort_by_attr(public_topic_levels, 'topic_level') # sort from greatest to least

      
  def make_cloud(self, topic_levels):
	level_cloud = []
	num = len(topic_levels)
	for tl in topic_levels:
		for n in range(num):
		   level_cloud.append(tl)
		num -= 1
	return level_cloud            


  def set_scroll(self, user):
    # TODO: Could these extra fetches be avoided? A count would have to be created seperately, in QT. 
	SCROLL_THRESHOLD = 2
	scroll = {}
	if len(user.awards.fetch(1000)) > SCROLL_THRESHOLD: scroll['awards'] = True
	if len(user.sponsorships.fetch(1000)) > SCROLL_THRESHOLD: scroll['sponsors'] = True
	if len(scroll) == 0: scroll = False
	return scroll




class EditProfile(webapp.RequestHandler):
  @login_required
  def get(self):
    public_photos = self.public_photos()
    if self.session['create_profile'] == True:
        edit_type = "Create"
        self.session['create_profile'] = False
    else: edit_type = 'Edit'
    template_values = {'user': self.session['user'], 'edit_type': edit_type, 
                       'photo_keys': public_photos}
                       
    template_values['edit_profile_js'] = edit_profile_js(template_values)
    path = tpl_path(PROFILE_PATH +'edit.html')
    self.response.out.write(template.render(path, template_values))

  def public_photos(self):
      public_photos = []
      photos = ProfilePicture.gql("WHERE type = :1", "pq").fetch(10)
      for p in photos:
          public_photos.append(str(p.key()))
      return public_photos


  

class EditSponsorSettings(webapp.RequestHandler):
  @login_required
  def get(self):
    if self.session['create_profile'] == True:
        edit_type = "Create"
        self.session['create_profile'] = False
    else: edit_type = 'Edit'
    from model.employer import Employer
    this_employer = Employer.get_by_key_name(self.session['user'].unique_identifier)
    from model.proficiency import Proficiency
    subjects = Proficiency.gql("WHERE status = :1", "public").fetch(1000)
    template_values = {'user': self.session['user'], 'edit_type': edit_type, 'this_employer': this_employer,
                        'subjects': subjects }
    path = tpl_path(PROFILE_PATH +'sponsor_settings.html')
    self.response.out.write(template.render(path, template_values))

      






class ViewSponsorProfile(webapp.RequestHandler):

  def get(self):
    from model.account import Sponsorship, Award
    template_values = self.get_sponsor_profile()
    if not template_values: return
    template_values['load'] = 2000 # give 2 seconds to load 
    template_values['profile_js'] = profile_js(template_values)
    path = tpl_path(PROFILE_PATH +'sponsor_template.html')
    self.response.out.write(template.render(path, template_values))
    

  def get_sponsor_profile(self):
		profile_stub = self.request.path.split('/sponsors/')[1].lower()
		profile_path = profile_stub.replace(' ','_')
		import urllib
		user = Profile.gql('WHERE profile_path = :1', urllib.unquote(profile_stub))
		try:
			user = user.get()
			if user.is_sponsor == False: self.redirect('/profile/' + user.profile_path) # go to sponsor profile
			logging.info('loading profile of %s for user %s' % (user.profile_path, getattr(self.session['user'], 'profile_path', "?")))
			this_user = user.unique_identifier
		except:
		    logging.debug('no sponsors profile of %s found for user %s' % (profile_path, getattr(self.session['user'], 'profile_path', "?")))
		    self.redirect('/sponsor_not_found/') # if no user is found
		    return False
		is_profile_owner = False
		if self.session['user']:
		    if user.unique_identifier == self.session['user'].unique_identifier: is_profile_owner = True
		else: set_flash('anon_viewer')
		from model.proficiency import Proficiency
		if len(user.sponsored_subjects) > 0: sponsored_subjects = [ Proficiency.get(user.sponsored_subjects[0]) ]
		else: sponsored_subjects = []
		return { 'user': user, 'sponsored_subjects': sponsored_subjects, 'profile_owner': is_profile_owner, 'is_sponsor': True}



 # TODO: Images don't load sometimes.


class Image (webapp.RequestHandler):  # TODO: Move this to somewhere more appropriate?
  # File caching controls
  FILE_CACHE_CONTROL = 'private, max-age=86400'
  FILE_CACHE_TIME = datetime.timedelta(days=20)
  @memoize('image_object')
  def get(self):
    self.set_expire_header()
    image_type = self.request.path.split('/image/')[1].lower().replace('/','')
    if image_type == 'profile': return self.profile_image()
    if image_type == 'subject': return self.subject_image()

  def profile_image(self):      
    if not self.request.get("img_id"): 
        self.redirect('/picture_not_found')
        return
    try: 
        pic = ProfilePicture.get(self.request.get("img_id"))
        self.response.headers['Content-Type'] = "image/png"
        if self.request.get("size") == "large": self.response.out.write(pic.large_image)
        else: self.response.out.write(pic.small_image)
    except: 
        self.redirect('/picture_not_found')
        return
    
          
  def subject_image(self):      
    from model.proficiency import SubjectImage
    if not self.request.get("img_id"): 
        self.redirect('/picture_not_found')
        return
    if self.request.get("img_id") == "default": return self.default_subject_image()
    self.response.headers['Content-Type'] = "image/png"
    pic = SubjectImage.get(self.request.get("img_id"))
    try: 
        if self.request.get("size") == "large": self.response.out.write(pic.large_image)
        else: self.response.out.write(pic.small_image)
    except: 
        self.redirect('/picture_not_found')
        logging.warning( 'picture not found: %s', self.request.get("img_id") )
        return
    

  def default_subject_image(self):
      from model.proficiency import DefaultSubjectImage
      pic = DefaultSubjectImage.all().get()
      self.response.headers['Content-Type'] = "image/png"
      if self.request.get("size") == "large": self.response.out.write(pic.large_image) 
      else: self.response.out.write(pic.small_image)     


  def set_expire_header(self):
      expires = datetime.datetime.now() + self.FILE_CACHE_TIME 
      self.response.headers['Cache-Control'] = self.FILE_CACHE_CONTROL
      self.response.headers['Expires'] = expires.strftime('%a, %d %b %Y %H:%M:%S GMT')













class ViewEmployerProfile(webapp.RequestHandler):  # deprecated
  def get(self):
    template_values = {}
    path = tpl_path(PROFILE_PATH +'employer_prototype.html')
    self.response.out.write(template.render(path, template_values))
    


class BrowseProfiles(webapp.RequestHandler):  # deprecated -- use this for sponsors
  def get(self):
    template_values = {}
    path = tpl_path(PROFILE_PATH +'browse_profiles.html')
    self.response.out.write(template.render(path, template_values))
    


class LoadUserProfile(webapp.RequestHandler):  # deprecated! 
  def get(self):
    if not self.request.get('user'): return False
    template_values = {}
    path = tpl_path(PROFILE_PATH + self.request.get('user') + '.html')
    self.response.out.write(template.render(path, template_values))
    



class PreviewViewProfile(webapp.RequestHandler): #deprecated 
  def get(self):

    template_values = {}
    path = tpl_path(PROFILE_PATH +'prototype.html')
    self.response.out.write(template.render(path, template_values))






@memoize('profile_js')
def profile_js(template_values):
        path = tpl_path(PROFILE_PATH + 'scripts/profile_template.js')
        from utils.random import minify 
        return minify( template.render(path, template_values) )

         

@memoize('edit_profile_js')
def edit_profile_js(template_values):
        path = tpl_path(PROFILE_PATH + 'scripts/edit_profile.js')
        from utils.random import minify 
        return minify( template.render(path, template_values) )        
        
