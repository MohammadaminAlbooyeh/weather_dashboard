

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///weather.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Weather model
class Weather(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(80), unique=True, nullable=False)
    temperature = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120), nullable=False)


# Create tables and add initial data if not exists
def create_tables():
    db.create_all()
    if not Weather.query.first():
        db.session.add_all([
            Weather(city="Tehran", temperature=30, description="Sunny"),
            Weather(city="Shiraz", temperature=28, description="Partly Cloudy"),
            Weather(city="Mashhad", temperature=25, description="Rainy"),
            Weather(city="Tabriz", temperature=22, description="Windy"),
        ])
        db.session.commit()

@app.route('/')
def home():
    return jsonify({"message": "Weather Dashboard Flask API is running."})



# Weather endpoint with SQLite data
@app.route('/api/weather', methods=['GET'])
def get_weather():
    city = request.args.get('city', 'Tehran')
    weather = Weather.query.filter_by(city=city).first()
    if weather:
        return jsonify({
            "city": weather.city,
            "temperature": weather.temperature,
            "description": weather.description
        })
    else:
        return jsonify({
            "city": city,
            "temperature": 20,
            "description": "Unknown"
        }), 404

if __name__ == '__main__':
    with app.app_context():
        create_tables()
    app.run(debug=True)
