PQ 
================

![PQ Logo](http://plopquiz.com/static/stylesheets/img/homepage/logo.png)


Setup
------------

  Run PQ through dev_appserver. 
  
  To load a datastore snapshot, navigate to /dev/admin
  and select the Restore Backup Datastore option, or manually load each data type.


Tips
------------    

* Developer Methods


  You must be logged in as an administrator to use developer methods. 
  
  On the development server, this is as easy as clicking the "Sign in as Administrator" checkbox.


* Offline Development

  To make it convenient to develop while offline, you can click "convenience" at the login screen.

  You can then enter your UID as an argument, like __"http://localhost:8080/dev/admin?shortcut=login&uid=myusername"__ 

    
Utilities
------------    
    
    /dev/admin - datastore operations.
    /console/ - interactive console, datastore and memcache administration, pastebin, logs, etc. 
