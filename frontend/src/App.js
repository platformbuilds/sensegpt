
import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Chat from './pages/Chat';
import Dashboard from './pages/Dashboard';
import TraceExplorer from './pages/TraceExplorer';

function App() {
  return (
    <Router>
      <div>
        <nav>
          <ul>
            <li><Link to="/chat">Chat Assistant</Link></li>
            <li><Link to="/dashboard">Anomaly Dashboard</Link></li>
            <li><Link to="/trace">Trace Explorer</Link></li>
          </ul>
        </nav>
        <Routes>
          <Route path="/chat" element={<Chat />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/trace" element={<TraceExplorer />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
