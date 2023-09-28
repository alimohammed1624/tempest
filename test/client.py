#!/usr/bin/env python3

from time import sleep
import socket


class Client:
    def __init__(self, host=socket.gethostbyname("0.0.0.0"), port=8003):
        self.socket = socket.socket()
        sleep(1)
        self.socket.connect((host, port))

    def close(self):
        self.socket.close()

    """
    Send two numbers to be added to Server
    Numbers are sent as strings and response 
    is the summation.
    """

    def test(self, data):
        message = str(data)
        self.socket.send(message.encode())
        response = self.socket.recv(1024).decode()
        response = eval(response)
        return response
