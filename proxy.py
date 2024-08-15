#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
import threading
from typing import Optional


def serve_client(client_socket: socket.socket) -> None:
    """
    1. receives from the client,
    2. extracts the hostname and port from its request,
    3. forwards the message unchanged to the remote,
    4. receives a response from the remote by calling receive_response,
    5. sends that message back to the client
    6. Close the out_socket at the end of the request
    """

    # Receive the HTTP request from the client
    header = receive_header(client_socket)

    result = extract_hostname(header)
    if result is None:
        print("Got a problem here")
        client_socket.close()
        return

    hostname, port = result

    if not hostname:
        client_socket.close()
        return

    # Create socket to remote server
    out_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    out_socket.settimeout(2000)
    out_socket.connect((hostname.decode(), port))

    # Forward request to remote server
    out_socket.sendall(header)

    # receive response from remote server
    response = receive_response(out_socket)

    # Send the response back
    client_socket.sendall(response)

    client_socket.close()
    out_socket.close()


def receive_header(sock: socket.socket) -> bytes:
    """
    receives from the socket until either:
    a HTTP header is received,
    or the socket is closed.
    """
    data = b""
    while True:
        part = sock.recv(4096)
        data += part
        if b"\r\n\r\n" in data:
            break
    return data


def extract_hostname(message: bytes) -> Optional[tuple[bytes, int]]:
    """
    Extracts the hostname and port from the HTTP header's Host field,
    and returns them as a tuple (hostname, port).
    Does not decode the hostname (leaves it as bytes)
    If no port is specified, it assumes the port is 80
    If no hostname is present, it returns None
    """
    lines = message.split(b"\r\n")
    for line in lines:
        if line.startswith(b"Host:"):
            host_data = line.split(b"Host:")[1].strip().split(b":")
            hostname = host_data[0]
            port = int(host_data[1]) if len(host_data) > 1 else 80
            return hostname, port
    return None


def receive_response(out_socket: socket.socket) -> bytes:
    """
    Receives the messages from the out_socket,
    and sends them to the client_socket.
    Receives HTTP message from the out_socket
    (HTTP request must already be sent by caller)
    Receive until the content is fully transmitted
    Return the message in full
    """
    data = b""
    while True:
        part = out_socket.recv(4096)
        if not part:
            break
        data += part
    return data


def main() -> None:
    """
    Creates the proxy server's main socket and binds to it.
    With each new client that connects,
    serves their requests.
    This one is done for you.
    """
    # create the server socket, a TCP socket on localhost:6789
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind(("", 6789))

    # listen for connections
    server_sock.listen(20)

    # forever accept connections
    # thread list is never cleaned (this is a vulnerability)
    threads = []
    while True:
        client_sock, addr = server_sock.accept()
        threads.append(threading.Thread(target=serve_client, args=(client_sock,)))
        threads[-1].start()


if __name__ == "__main__":
    main()
