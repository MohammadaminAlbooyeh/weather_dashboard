

import { useState } from 'react';
import './App.css';


function App() {
  const [city, setCity] = useState('');
  const [weather, setWeather] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setWeather(null);
    try {
      const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
      if (!res.ok) {
        throw new Error('City not found or server error');
      }
      const data = await res.json();
      setWeather(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-app">
      <h1>Weather Dashboard</h1>
      <form onSubmit={handleSubmit} className="weather-form">
        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={e => setCity(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Get Weather'}
        </button>
      </form>
      {weather && (
        <div className="weather-card">
          <h2>{weather.city}</h2>
          <p><span role="img" aria-label="thermometer">🌡️</span> Temperature: <b>{weather.temperature} °C</b></p>
          <p><span role="img" aria-label="humidity">💧</span> Humidity: <b>{weather.humidity} %</b></p>
          <p><span role="img" aria-label="desc">☀️</span> {weather.description}</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
