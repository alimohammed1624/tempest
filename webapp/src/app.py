#!/usr/bin/env python3

from flask import Flask, request
import requests

app = Flask(__name__)


@app.route("/")
def main():
    return """
    <h1>Tempest</h1>
    Enter a city to fetch temperature!
    <form action="/fetch" method="GET">
        <input name="city">
        <input type="submit" value="Fetch!">
    </form>
    <form action="/disp" method="GET">
        <input type="submit" value="Display all records!">
    </form>
    """


@app.route("/fetch", methods=["GET"])
def fetch():
    data = requests.get(
        "http://analyzer:8001/fetch", params={"city": request.args.get("city")}
    )
    if data.json().get("error") is not None:
        return f"""
            {data.json()["error"]["message"]}
            <form action="/" method="GET">
                <input type="submit" value="Back to Home!">
            </form>
        """
    return f"""
        Added to database!
        {render_table([data.json()])}
        <form action="/disp" method="GET">
            <input type="submit" value="Display All!">
        </form>
        <form action="/" method="GET">
            <input type="submit" value="Back to Home!">
        </form>
    """


@app.route("/disp", methods=["GET"])
def disp():
    data = (requests.get("http://analyzer:8001/fetchall")).json().get("data")
    return f"""
        {render_table(data)}
        <form action="/" method="GET">
            <input type="submit" value="Back to Home!">
        </form>
    """


def render_table(data):
    table = "<table border = 1>"
    table += "<tr><th>City</th><th>Weather Variation Index</th><th>Time</th></tr>"
    for row in data:
        table += f"<tr><td>{row.get('city')}</td><td>{row.get('index')}%</td><td>{row.get('timestamp')}</td></tr>"
    table += "</table>"
    return table
