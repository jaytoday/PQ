PQ 
================

![PQ Logo](http://plopquiz.com/static/stylesheets/img/homepage/logo.png)


Setup
------------

  Run PQ through dev_appserver. Refer to App Engine docs for details. 
  
  You can restore your datastore at /dev/admin by loading each data type, 
  from top to bottom.
  
  If you are running your SDK server for the first time, you must restore data
  before your server will properly function. 


Tips
------------    

* Codebase Architecture

  URL patterns are defined in /urls.py.
  
  ## Applications 
  
  Each application is stored in an eponymous folder. Typically, each application consists of:
  
  -- views.py - renders the template for a page
  -- rpc.py - XML-RPC methods
  -- methods.py - shared methods, and code chunks too large for a views.py class. 
  
  
  ## Shared Files 
  
  -- Templates are in /templates/, in the folder corresponding to the application.
  -- Models are defined in /models/ 
  -- Libraries and utilities are in /utils/
  -- Javascript is in /static/scripts/ (unless it needs to be dynamic)
  -- Stylesheets are in /static/stylesheets/
  -- Images are in /static/stylesheets/img/
  -- Backup JSON and files that need to be opened during execution are in /data/
  



* Developer Methods

  You must be logged in as an administrator to use developer methods. 
  
  On the development server, this is as easy as clicking the "Sign in as Administrator" checkbox.



* Offline Development

  For convenience while developing offline, you can click "convenience" at the login screen. 

  You can then enter your UID as an argument, like __"http://localhost:8080/dev/admin?shortcut=login&uid=myusername"__ 

    
Utilities
------------    
    
    /dev/admin - datastore operations.
    /console/ - interactive console, datastore and memcache administration, pastebin, logs, etc. 
