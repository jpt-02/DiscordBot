import { useState, useEffect } from 'react';
import './App.css'; 

const API_BASE_URL = 'http://localhost:5000'; 

function App() {
  // Only need state for fetching stats
  const [botStats, setBotStats] = useState(null);
  const [loadingStats, setLoadingStats] = useState(true);
  const [errorStats, setErrorStats] = useState(null);

  // --- Stats Fetching (GET Request to /api/stats) ---

  const fetchBotStats = () => {
    fetch(`${API_BASE_URL}/api/stats`)
      .then(response => {
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setBotStats(data);
        setErrorStats(null);
      })
      .catch(err => {
        console.error("Fetch stats error:", err);
        setErrorStats("Could not connect to the API server. Check Flask terminal.");
        setBotStats(null);
      })
      .finally(() => {
        setLoadingStats(false);
      });
  };

  useEffect(() => {
    fetchBotStats();
  }, []); // Run only once on component load

  // --- Rendering ---

  return (
    <div className="App-container">
      <h1>Discord Bot Status Panel</h1>
      <p className="note">Data fetched from SQLIte DB via Flask API on port 5000</p>

      {/* Bot Stats Display */}
      <section className="stats-section">
        <h2>Live Bot Statistics (GET)</h2>
        {loadingStats && <p>Loading stats from API...</p>}
        {errorStats && <p className="error-message">Error: {errorStats}</p>}
        
        {botStats && (
          <div className="status-card">
            <p>Status: <strong style={{color: botStats.status === 'Online' ? 'green' : 'red'}}>{botStats.status}</strong></p>
            <p>Guilds: <strong>{botStats.guild_count}</strong></p>
            <p>Total Members: <strong>{botStats.total_members}</strong></p>
            <p>Last Updated: {new Date(botStats.last_updated).toLocaleTimeString()}</p>
          </div>
        )}
      </section>
    </div>
  );
}

export default App;