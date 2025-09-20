import threading
import traceback
import socket
from logging import getLogger
from typing import Callable, Optional, Dict, Any, Type

logger = getLogger("oauth_http_server")
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler  # type: ignore
except ImportError:
    from http.server import HTTPServer, BaseHTTPRequestHandler
try:
    import urlparse  # type: ignore
except ImportError:
    from urllib import parse as urlparse


def find_unused_port() -> int:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    sock.bind(("", 0))
    sock.listen(socket.SOMAXCONN)
    ipaddr, port = sock.getsockname()
    sock.close()
    return port


class OAuthHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        path = [i for i in self.path.split("/") if i]
        logger.debug("Path: %s" % path)
        if path[0] != "oauth":
            raise ValueError("Unable to process non-OAuth request.")
        callback_data = "?".join(path[1].split("?")[1:])
        parsed_data = {k: v[0] for k, v in urlparse.parse_qs(callback_data).items()}
        try:
            self.server.callback(parsed_data)
        except Exception:
            logger.exception("Error calling oAuth login callback.")
            self.send_response(500)
            self.end_headers()
            self.wfile.write(traceback.format_exc().encode())
            return
        self.send_response(200)
        self.end_headers()
        self.wfile.write(self.server.success_msg.encode())
        t = threading.Thread(target=self.server.shutdown)
        t.daemon = True
        t.start()


class OAuthServer(HTTPServer):
    allow_reuse_address = 0

    def __init__(
        self,
        host: str = "localhost",
        port: Optional[int] = None,
        handler_class: Type[BaseHTTPRequestHandler] = OAuthHandler,
        callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> None:
        if not callable(callback):
            raise TypeError("Must provide a callable callback.")
        if port is None:
            port = find_unused_port()
        # Because for some reason super won't work for the HTTPServer
        HTTPServer.__init__(self, (host, port), handler_class)
        self.host, self.port = host, port
        self.callback = callback

    def get_oauth_callback_url(self) -> str:
        return "http://%s:%d/oauth/callback" % (self.host, self.port)

    success_msg = """
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
