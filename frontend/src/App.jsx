
import { useState } from 'react';
import './App.css';

function App() {
  const [city, setCity] = useState('');
  const [temperature, setTemperature] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    setTemperature(null);
    try {
            const res = await fetch(`/api/weather?city=${encodeURIComponent(city)}`);
      if (!res.ok) {
        throw new Error('City not found or server error');
      }
      const data = await res.json();
      setTemperature(data.temperature);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="weather-app">
      <h1>Weather Dashboard</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter city name"
          value={city}
          onChange={e => setCity(e.target.value)}
          required
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Loading...' : 'Get Temperature'}
        </button>
      </form>
      {temperature !== null && (
        <div className="result">
          <h2>Temperature in {city}:</h2>
          <p>{temperature} °C</p>
        </div>
      )}
      {error && <p className="error">{error}</p>}
    </div>
  );
}

export default App;
