import requests
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///tempest.db"

db = SQLAlchemy(app)


class Raw(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    city = db.Column(db.String(100), nullable=False)
    data = db.Column(db.JSON, nullable=False)


class Processed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    city = db.Column(db.String(100), nullable=False)
    index = db.Column(db.Float, nullable=False)


@app.route("/fetchall", methods=["GET"])
def fetchall():
    return jsonify(
        {
            "data": [
                {"city": item.city, "index": item.index, "timestamp": item.timestamp}
                for item in Processed.query.all()
            ]
        }
    )


@app.route("/fetch", methods=["GET"])
def fetch():
    city = request.args.get("city", "")
    temperature = requests.get(
        "http://127.0.0.1:8002/fetch", params={"city": city}
    ).json()
    if temperature.get("error") is not None:
        return jsonify({"error": temperature.get("error")})
    data = Raw(timestamp=datetime.utcnow(), data=temperature, city=city)
    db.session.add(data)
    db.session.commit()
    return process_data(temperature, data)


def process_data(temperature, raw: Raw):
    temps = [
        item["day"]["avgtemp_c"] for item in temperature["forecast"]["forecastday"]
    ]
    standard_deviation = 0
    average = sum(temps) / len(temps)
    for item in temps:
        standard_deviation += item**2 / len(temps)
    standard_deviation = standard_deviation**0.5
    index = standard_deviation / average
    data = Processed(id=raw.id, timestamp=raw.timestamp, city=raw.city, index=index)
    db.session.add(data)
    db.session.commit()
    return jsonify({"index": index, "city": raw.city, "timestamp": raw.timestamp})


with app.app_context():
    db.create_all()
