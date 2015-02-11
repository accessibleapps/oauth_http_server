from logging import getLogger
logger = getLogger('oauth_http_server')

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import socket
import traceback
import threading
import urlparse

def find_unused_port ():
 sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
 sock.bind(('', 0))
 sock.listen(socket.SOMAXCONN)
 ipaddr, port = sock.getsockname()
 sock.close()
 return port


class OAuthHandler(BaseHTTPRequestHandler):

 def do_GET(self):
  path = [i for i in self.path.split('/') if i]
  logger.debug("Path: %s" % path)
  if path[0] != 'oauth':
   raise ValueError("Unable to process non-OAuth request.")
  callback_data = "?".join(path[1].split('?')[1:])
  parsed_data = {k: v[0] for k, v in urlparse.parse_qs(callback_data).iteritems()}
  try:
   self.server.callback(parsed_data)
  except Exception as e:
   logger.exception("Error calling oAuth login callback.")
   self.send_response(500)
   self.end_headers()
   self.wfile.writelines(    traceback.format_exc(e))
   return
  self.send_response(200)
  self.end_headers()
  self.wfile.write(self.server.success_msg)
  t = threading.Thread(target=self.server.shutdown)
  t.daemon = True
  t.start()

class OAuthServer(HTTPServer):
 allow_reuse_address = 0

 def __init__(self, host='localhost', port=None, handler_class=OAuthHandler, callback=None):
  if not callable(callback):
   raise TypeError("Must provide a callable callback.")
  if port is None:
   port = find_unused_port()
  HTTPServer.__init__(self, (host, port), handler_class) #Because for some reason super won't work for the HTTPServer
  self.host, self.port = host, port
  self.callback = callback

 def get_oauth_callback_url(self):
  return 'http://%s:%d/oauth/callback' % (self.host, self.port)

 success_msg = \
"""
<html>
<head>
<title>Successful login!</title>
</head>
<body>
<h1>Login successful!</h1>
<p>
You have been logged in!
You can now close this window and enjoy the app.
</p>
</body>
</html>
"""
