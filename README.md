# oauth_http_server Python Package
*A simple http server for parsing oauth callbacks for desktop apps pretending to be webapps*

## Overview
This package provides an `OAuthServer` class that simulates server operations for OAuth authentication. It's primarily intended for use with desktop applications that need to pretend to be web applications for the sake of OAuth.

The server uses a simple HTTP server to listen for and process OAuth callbacks. When a client connects to the server and sends a GET request, the server will validate the request, parse the callback data, and then call the registered callback function with the parsed data.

## Usage 

A basic usage of the `oauth_http_server` package might look something like this:

```python
from oauth_http_server import OAuthServer

def callback(data):
    print('OAuth data received:', data)

server = OAuthServer(callback=callback)
print('OAuth callback URL:', server.get_oauth_callback_url())
server.serve_forever()
```

## Contributing
Contributions to improve the `oauth_http_server` are welcomed. Please feel free to open issues through GitHub or submit a pull request if you have a feature or bugfix.

## License
This project is licensed under the MIT License. See `LICENSE` for more details.
