#!/usr/bin/env python3

import json
import requests
import socket
from time import sleep
from unittest.mock import MagicMock

"""
Server listens for request containing two numbers
and then sums those numbers. The server responds with
the summation
"""


class Server:
    def __init__(self, host=socket.gethostbyname("0.0.0.0"), port=8003):
        self.socket = socket.socket()
        self.socket.bind((host, port))

    def close(self):
        self.socket.close()

    def listen(self):
        self.socket.listen(1)
        conn, addr = self.socket.accept()
        while True:
            data = conn.recv(1024).decode()
            resp = requests.get("http://localhost:8000/ping").json()
            if resp.get("data") != "Healthy":
                conn.send(str(resp).encode())
                continue
            resp = requests.get("http://localhost:8001/ping").json()
            if resp.get("data") != "Healthy":
                conn.send(str(resp).encode())
                continue
            resp = requests.get("http://localhost:8002/ping").json()
            if resp.get("data") != "Healthy":
                conn.send(str(resp).encode())
                continue
            resp = requests.get(
                "http://localhost:8001/fetch", params={"city": data}
            ).json()
            conn.send(str(resp).encode())


if __name__ == "__main__":
    server = Server()
    server.listen()
