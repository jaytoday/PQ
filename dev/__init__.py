

""" 

Import development files 

"""

from algorithm import *





import wsgiref.handlers
from google.appengine.ext import webapp





class controller (object):
    def __init__(self,hnd):
        self.hnd=hnd
    def echo(self,data):
        self.hnd.response.out.write(data)
       
  
        
class URIRouter(webapp.RequestHandler):
    uri=None
    seg=[]
    controller='test'   #default controller name
    method='index'   #default method
    def post(self,uri):
        self.uri=uri
        self.dispatch()
        
    def get(self,uri):
        self.uri=uri
        self.dispatch()
        
    def parseURI(self):
        self.seg=self.uri.split('/')
        if self.seg[0]!='' :
            #set the first segment of uri as the class name of controller
            self.controller=self.seg[0]
        if len(self.seg) >1 :
            #set the second segment of uri as the method name of controller
            if self.seg[1]!='' : 
                self.method=self.seg[1]
    def dispatch(self):
        self.parseURI()
        #create controller object
        c=globals()[self.controller](self)
        #call the method
        getattr(c,self.method)(*self.seg[2:])


class controller (object):
    def __init__(self,hnd):
        self.hnd=hnd
    def echo(self,data):
        self.hnd.response.out.write(data)
#an example of controller        


        


