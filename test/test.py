#!/usr/bin/env python3

"""
This file is called test.py
"""
from subprocess import Popen
from client import Client


def test_server_client():
    """
    We start the server and let it run in the background. Then we ask
    the client to make a call to the server and we compare the expected value.
    """
    server = Popen("./server.py")
    client = Client()
    resp = client.test("Boulder")
    assert resp.get("city") == "Boulder", f"Response is {resp}"
