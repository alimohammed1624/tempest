#!/usr/bin/env python3
import requests
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from os import environ

app = Flask(__name__)

"""
Define the database model
that is used to store 
the temperature.
"""

key = "e4418a5d189b4f9399e11616232809"


@app.route("/fetch", methods=["GET"])
def fetch():
    city = request.args.get("city", "")
    temperature = get_temperature(city)
    return temperature


"""
using API
"""


def get_temperature(city):
    response = requests.get(
        f"http://api.weatherapi.com/v1/forecast.json?key={key}&q={city}&days=3"
    )
    return response.json()


"""
In main we first get the current temperature and then 
create a new object that we can add to the database. 
"""
