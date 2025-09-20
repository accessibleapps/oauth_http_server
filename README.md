# oauth_http_server

A simple HTTP server for parsing OAuth callbacks for desktop apps.

## What it does

Desktop applications often need to authenticate with OAuth providers that only support web-based redirects. This package creates a temporary local HTTP server to receive OAuth callback URLs, making it possible for desktop apps to complete OAuth flows.

## Installation

```bash
pip install -e .
```

## Usage

```python
from oauth_http_server import OAuthServer

def handle_oauth_response(data):
    print(f"Received OAuth data: {data}")

server = OAuthServer(callback=handle_oauth_response)
callback_url = server.get_oauth_callback_url()
print(f"Use this callback URL: {callback_url}")

# Start the server and wait for OAuth callback
server.serve_forever()
```

## API

`OAuthServer(host='localhost', port=None, callback=None)`

- `host`: Server hostname (default: 'localhost')
- `port`: Server port (default: automatically finds unused port)
- `callback`: Function to call with parsed OAuth data

`get_oauth_callback_url()`: Returns the full callback URL to use with OAuth providers

The server automatically shuts down after receiving a callback.
