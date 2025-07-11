


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
import requests
from geopy.geocoders import Nominatim
from dateutil import parser

# Weather API endpoint for city search (no API key required)
class WeatherAPIView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        city = request.query_params.get('city')
        if not city:
            return Response({'error': 'City parameter is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Geocode city name to lat/lon
        geolocator = Nominatim(user_agent="weather-app")
        location = geolocator.geocode(city)
        if not location:
            return Response({'error': 'City not found.'}, status=status.HTTP_404_NOT_FOUND)
        lat, lon = location.latitude, location.longitude
        # Fetch weather data from open-meteo
        url = (
            f"https://api.open-meteo.com/v1/forecast?"
            f"latitude={lat}&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=relative_humidity_2m&timezone=auto"
        )
        r = requests.get(url)
        if r.status_code != 200:
            return Response({'error': 'Weather API error.'}, status=r.status_code)
        data = r.json()
        if "current_weather" not in data or "hourly" not in data:
            return Response({'error': 'Incomplete weather data.'}, status=status.HTTP_502_BAD_GATEWAY)
        # Find closest humidity value to current time
        try:
            current_time = parser.parse(data["current_weather"]["time"])
            times = [parser.parse(t) for t in data["hourly"]["time"]]
            humidities = data["hourly"]["relative_humidity_2m"]
            closest_index = min(range(len(times)), key=lambda i: abs(times[i] - current_time))
            humidity = humidities[closest_index]
        except Exception:
            humidity = None
        result = {
            'city': city.title(),
            'temperature': data["current_weather"]["temperature"],
            'humidity': humidity,
            'wind_speed': data["current_weather"]["windspeed"],
            'wind_direction': data["current_weather"]["winddirection"],
            'time': data["current_weather"]["time"],
        }
        return Response(result)
