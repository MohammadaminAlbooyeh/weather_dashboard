


from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import requests
from geopy.geocoders import Nominatim
from dateutil import parser



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



# Weather model (legacy, not used for real-time API)
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)
    humidity = db.Column(db.Integer, nullable=False, default=50)

# Search history model
from datetime import datetime
class SearchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), nullable=False)
    temperature = db.Column(db.Float, nullable=True)
    humidity = db.Column(db.Float, nullable=True)
    description = db.Column(db.String(120), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)


# Create tables and add initial data if not exists
def create_tables():
    db.drop_all()
    db.create_all()
    if not Weather.query.first():
        db.session.add_all([
            Weather(city="Tehran", temperature=30, description="Sunny", humidity=40),
            Weather(city="Shiraz", temperature=28, description="Partly Cloudy", humidity=35),
            Weather(city="Mashhad", temperature=25, description="Rainy", humidity=60),
            Weather(city="Tabriz", temperature=22, description="Windy", humidity=30),
        ])
        db.session.commit()

@app.route('/')
def home():
    return jsonify({"message": "Weather Dashboard Flask API is running."})




# Weather endpoint with real-time data from Open-Meteo
@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Tehran')
    geolocator = Nominatim(user_agent="weather-dashboard-flask")
    location = geolocator.geocode(city)
    if not location:
        return jsonify({
            "city": city,
            "temperature": None,
            "description": "City not found",
            "humidity": None
        }), 404
    lat, lon = location.latitude, location.longitude
    url = (
        f"https://api.open-meteo.com/v1/forecast?"
        f"latitude={lat}&longitude={lon}"
        f"&current_weather=true"
        f"&hourly=relative_humidity_2m,weathercode&timezone=auto"
    )
    response = requests.get(url)
    if response.status_code != 200:
        return jsonify({
            "city": city,
            "temperature": None,
            "description": "Weather API error",
            "humidity": None
        }), 500
    data = response.json()
    current = data.get("current_weather", {})
    # Find closest humidity value to current time
    try:
        current_time = parser.parse(current["time"])
        times = [parser.parse(t) for t in data["hourly"]["time"]]
        humidities = data["hourly"]["relative_humidity_2m"]
        closest_index = min(range(len(times)), key=lambda i: abs(times[i] - current_time))
        humidity = humidities[closest_index]
    except Exception:
        humidity = None
    temperature = current.get("temperature")
    # Weather description mapping (optional, can be improved)
    weathercode = current.get("weathercode")
    code_map = {
        0: "Clear sky",
        1: "Mainly clear",
        2: "Partly cloudy",
        3: "Overcast",
        45: "Fog",
        48: "Depositing rime fog",
        51: "Light drizzle",
        53: "Drizzle",
        55: "Dense drizzle",
        56: "Freezing drizzle",
        57: "Dense freezing drizzle",
        61: "Slight rain",
        63: "Rain",
        65: "Heavy rain",
        66: "Freezing rain",
        67: "Heavy freezing rain",
        71: "Slight snow fall",
        73: "Snow fall",
        75: "Heavy snow fall",
        77: "Snow grains",
        80: "Slight rain showers",
        81: "Rain showers",
        82: "Violent rain showers",
        85: "Slight snow showers",
        86: "Heavy snow showers",
        95: "Thunderstorm",
        96: "Thunderstorm with hail",
        99: "Thunderstorm with heavy hail"
    }
    description = code_map.get(weathercode, "Unknown")
    # Save search to database
    search = SearchHistory(
        city=city.title(),
        temperature=temperature,
        humidity=humidity,
        description=description
    )
    db.session.add(search)
    db.session.commit()
    return jsonify({
        "city": city.title(),
        "temperature": temperature,
        "description": description,
        "humidity": humidity
    })

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True, port=5001)
