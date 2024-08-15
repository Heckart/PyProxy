# PyProxy
## Overview
This is a simple proof of concept implementation of an HTTP Proxy using TCP sockets, written in Python.The proxy listens on `localhost:6789`. Upon receiving a client, it accepts the TCP connection, receives any HTTP request it may have, and forwards it to the desired host in the "Host" field. Then, it forwards the response back to the client.

The HTTP requests and responses are unmodified by the proxy.

The proxy stores incoming data, until the remote server is done sending, and then sends it to the client all at once.

## Code
`proxy.py` is the main file. Running it runs the proxy server, which will continue until the process is killed.

It has the following functions:
- `main`
  - Creates the proxy server socket and calls `serve_client` whenever a client connects.
- `serve_client`
  -  Serves a single request from a client. Sends the message to the remove host, gets the response with `receive_response`, and sends it to the client. It closes both sockets afterwards.
- `receive_response`
  - Receives from the remote host, returns it.
- `extract_hostname`
  - Returns the host name and the port for the HTTP header.

## Browser Configuration
Configuring your browser to use the proxy:
- Firefox
  - Go to Settings->General->Network Settings; select "Manual Proxy" and set it to `localhost` on `6789` for HTTP.
- Qutebrowser
  - Execute `:set content.proxy http://localhost:6789/`
  - or, use the GUI in qute://settings
Make sure your browser is not caching the page. In qutebrowser, Shift + r will reload the page, discarding the cache.

## Real-world application
You could easily run this code on a remote machine, and use it a proxy for your browser traffic! This one is not encrypted, but you get the idea.
