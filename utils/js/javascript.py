

from StringIO import StringIO


def jsmin(js):
    ins = StringIO(js)
    outs = StringIO()
    JavascriptMinify().minify(ins, outs)
    str = outs.getvalue()
    if len(str) > 0 and str[0] == '\n':
        str = str[1:]
    return str

def isAlphanum(c):
    """return true if the character is a letter, digit, underscore,
           dollar sign, or non-ASCII character.
    """
    return ((c >= 'a' and c <= 'z') or (c >= '0' and c <= '9') or
            (c >= 'A' and c <= 'Z') or c == '_' or c == '$' or c == '\\' or (c is not None and ord(c) > 126));

class UnterminatedComment(Exception):
    pass

class UnterminatedStringLiteral(Exception):
    pass

class UnterminatedRegularExpression(Exception):
    pass

class JavascriptMinify(object):

    def _outA(self):
        self.outstream.write(self.theA)
    def _outB(self):
        self.outstream.write(self.theB)

    def _get(self):
        """return the next character from stdin. Watch out for lookahead. If
           the character is a control character, translate it to a space or
           linefeed.
        """
        c = self.theLookahead
        self.theLookahead = None
        if c == None:
            c = self.instream.read(1)
        if c >= ' ' or c == '\n':
            return c
        if c == '': # EOF
            return '\000'
        if c == '\r':
            return '\n'
        return ' '

    def _peek(self):
        self.theLookahead = self._get()
        return self.theLookahead

    def _next(self):
        """get the next character, excluding comments. peek() is used to see
           if a '/' is followed by a '/' or '*'.
        """
        c = self._get()
        if c == '/':
            p = self._peek()
            if p == '/':
                c = self._get()
                while c > '\n':
                    c = self._get()
                return c
            if p == '*':
                c = self._get()
                while 1:
                    c = self._get()
                    if c == '*':
                        if self._peek() == '/':
                            self._get()
                            return ' '
                    if c == '\000':
                        raise UnterminatedComment()

        return c

    def _action(self, action):
        """do something! What you do is determined by the argument:
           1   Output A. Copy B to A. Get the next B.
           2   Copy B to A. Get the next B. (Delete A).
           3   Get the next B. (Delete B).
           action treats a string as a single character. Wow!
           action recognizes a regular expression if it is preceded by ( or , or =.
        """
        if action <= 1:
            self._outA()

        if action <= 2:
            self.theA = self.theB
            if self.theA == "'" or self.theA == '"':
                while 1:
                    self._outA()
                    self.theA = self._get()
                    if self.theA == self.theB:
                        break
                    if self.theA <= '\n':
                        raise UnterminatedStringLiteral()
                    if self.theA == '\\':
                        self._outA()
                        self.theA = self._get()


        if action <= 3:
            self.theB = self._next()
            if self.theB == '/' and (self.theA == '(' or self.theA == ',' or
                                     self.theA == '=' or self.theA == ':' or
                                     self.theA == '[' or self.theA == '?' or
                                     self.theA == '!' or self.theA == '&' or
                                     self.theA == '|' or self.theA == ';' or
                                     self.theA == '{' or self.theA == '}' or
                                     self.theA == '\n'):
                self._outA()
                self._outB()
                while 1:
                    self.theA = self._get()
                    if self.theA == '/':
                        break
                    elif self.theA == '\\':
                        self._outA()
                        self.theA = self._get()
                    elif self.theA <= '\n':
                        raise UnterminatedRegularExpression()
                    self._outA()
                self.theB = self._next()


    def _jsmin(self):
        """Copy the input to the output, deleting the characters which are
           insignificant to JavaScript. Comments will be removed. Tabs will be
           replaced with spaces. Carriage returns will be replaced with linefeeds.
           Most spaces and linefeeds will be removed.
        """
        self.theA = '\n'
        self._action(3)

        while self.theA != '\000':
            if self.theA == ' ':
                if isAlphanum(self.theB):
                    self._action(1)
                else:
                    self._action(2)
            elif self.theA == '\n':
                if self.theB in ['{', '[', '(', '+', '-']:
                    self._action(1)
                elif self.theB == ' ':
                    self._action(3)
                else:
                    if isAlphanum(self.theB):
                        self._action(1)
                    else:
                        self._action(2)
            else:
                if self.theB == ' ':
                    if isAlphanum(self.theA):
                        self._action(1)
                    else:
                        self._action(3)
                elif self.theB == '\n':
                    if self.theA in ['}', ']', ')', '+', '-', '"', '\'']:
                        self._action(1)
                    else:
                        if isAlphanum(self.theA):
                            self._action(1)
                        else:
                            self._action(3)
                else:
                    self._action(1)

    def minify(self, instream, outstream):
        self.instream = instream
        self.outstream = outstream
        self.theA = '\n'
        self.theB = None
        self.theLookahead = None

        self._jsmin()
        self.instream.close()


import os
import re

import StringIO

from google.appengine.ext import webapp
from google.appengine.api import memcache

import wsgiref.handlers

jsm = JavascriptMinify()

memCacheExpire = 900

def getFileName(path):
  regex = re.compile('/[a-zA-Z_]+/([a-zA-Z0-9_\-/]+\.(js|css))$')
  return os.path.join(os.path.dirname(__file__) + '/.../static/' + regex.search(path).groups()[0])

def getFileContent(filename):  
  ospath = os.path.join(os.path.dirname(__file__), filename)
  input = open(ospath, 'r')
  return input.read()

def minify(filename):    
  path = os.path.join(os.path.dirname(__file__), filename)        
  input = open(path, 'r')
  output = StringIO.StringIO()

  jsm.minify(input, output)

  return output.getvalue()  

class JsMinify(webapp.RequestHandler):
  def get(self):
        
    data = memcache.get(self.request.path)    

    if data is None:
      filename = getFileName(self.request.path)
      data = minify(filename)   
      memcache.add(self.request.path, data, memCacheExpire)      

    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(data)


class JsMinify_(webapp.RequestHandler):
  def get(self):
    filename = getFileName(self.request.path)
    data = minify(filename)              

    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(data)


class JsNormal(webapp.RequestHandler):
  def get(self):      

    data = memcache.get(self.request.path)    

    if data is None:
      filename = getFileName(self.request.path)
      data = getFileContent(filename)
      memcache.add(self.request.path, data, memCacheExpire)   

    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(data)

class JsNormal_(webapp.RequestHandler):
  def get(self):      
    filename = getFileName(self.request.path)
    data = getFileContent(filename)

    self.response.headers['Content-Type'] = 'text/javascript'
    self.response.out.write(data)

apps_binding = []

# serving normal javascript file from mem cache
apps_binding.append(('/static/scripts/.*', JsNormal))

# serving normal javascript file directly from disk
apps_binding.append(('/static/scripts_/.*', JsNormal_))

# serving minified javascript file from mem cache
apps_binding.append(('/static/scripts_min/.*', JsMinify))

# serving minified javascript file directly from disk
apps_binding.append(('/static/scripts/.*', JsMinify_))


application = webapp.WSGIApplication(apps_binding, debug=True)
wsgiref.handlers.CGIHandler().run(application)
