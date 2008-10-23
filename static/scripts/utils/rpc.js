    
function Request(function_name, opt_argv, app_name) {

	if (!opt_argv)
		opt_argv = new Array();

	// Find if the last arg is a callback function; save it
	var callback = null;
	var len = opt_argv.length;

	if (len > 0 && typeof opt_argv[len-1] == 'function') {
		callback = opt_argv[len-1];
		opt_argv.length--;
	}

	var async = (callback != null);

	// Encode the arguments in to a URI
	var query = 'action=' + encodeURIComponent(function_name);

	for (var i = 0; i < opt_argv.length; i++) {
		var key = 'arg' + i;
		var val = JSON.stringify(opt_argv[i]);
		query += '&' + key + '=' + encodeURIComponent(val);
	}
	query += '&time=' + new Date().getTime(); // IE cache workaround

	// Create an XMLHttpRequest 'GET' request w/ an optional callback handler 
	var req = new XMLHttpRequest();
	req.open('GET', '/' + app_name + '/rpc?' + query, async);

	if (async) {
		req.onreadystatechange = function() {
			if(req.readyState == 4 && req.status == 200) {
				var response = null;
				try {
					response = JSON.parse(req.responseText);
				} catch (e) {
					response = req.responseText;
				}
				callback(response);
			}
		}
	}

	// Make the actual request
	req.send(null);
}

// Adds a stub function that will pass the arguments to the AJAX call 
function InstallFunction(obj, functionName, app_name) {
	obj[functionName] = function() { 
		Request(functionName, arguments, app_name);
	}
}




function PostRequest(function_name, opt_argv, app_name) {

  if (!opt_argv)
    opt_argv = new Array();
 
  // Find if the last arg is a callback function; save it
  var callback = null;
  var len = opt_argv.length;
  if (len > 0 && typeof opt_argv[len-1] == 'function') {
    callback = opt_argv[len-1];
    opt_argv.length--;
  }
  var async = (callback != null);
 
  // Build an Array of parameters, w/ function_name being the first parameter
  var params = new Array(function_name);
  for (var i = 0; i < opt_argv.length; i++) {
    params.push(opt_argv[i]);
  }
  var body = JSON.stringify(params);

  // Create an XMLHttpRequest 'POST' request w/ an optional callback handler 
  var req = new XMLHttpRequest();
  req.open('POST','/' + app_name + '/rpc/post', async);
 
  req.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
  req.setRequestHeader("Content-length", body.length);
  req.setRequestHeader("Connection", "close");

  if (async) {
    req.onreadystatechange = function() {
      if(req.readyState == 4 && req.status == 200) {
        var response = null;
        try {
         response = JSON.parse(req.responseText);
        } catch (e) {
         response = req.responseText;
        }
        callback(response);
      }
    }
  }
 
  // Make the actual request
  req.send(body);
}

// Adds a stub function that will pass the arguments to the AJAX call 
function InstallPostFunction(obj, functionName, app_name) {
	obj[functionName] = function() { 
		PostRequest(functionName, arguments, app_name);
	}
}
