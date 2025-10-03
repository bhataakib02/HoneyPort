import React, { useState, useEffect } from 'react';
import SessionList from './components/SessionList';
import SessionViewer from './components/SessionViewer';
import StatsCards from './components/StatsCards';
import ThreatChart from './components/ThreatChart';
import ProfessionalHeader from './components/ProfessionalHeader';
import SystemStatus from './components/SystemStatus';
import AnalyticsPage from './components/AnalyticsPage';
import './index.css';

const API_BASE = 'http://localhost:8001';

function App() {
  const [sessions, setSessions] = useState([]);
  const [stats, setStats] = useState({
    total_sessions: 0,
    total_threats: 0,
    threat_levels: { LOW: 0, MEDIUM: 0, HIGH: 0, CRITICAL: 0 },
    avg_score: 0,
    last_activity: null,
    system_health: {},
    attack_vectors: {},
    geographic_distribution: {},
    active_connections: 0
  });
  const [selectedSession, setSelectedSession] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());
  const [autoRefresh, setAutoRefresh] = useState(false);
  const [activeTab, setActiveTab] = useState('dashboard');
  const [currentPage, setCurrentPage] = useState('dashboard'); // 'dashboard' or 'analytics'

  // Professional data fetching
  const fetchProfessionalSessions = async () => {
    try {
      const response = await fetch(`${API_BASE}/sessions`);
      if (!response.ok) throw new Error('Failed to fetch session data');
      const data = await response.json();
      setSessions(data.sessions || []);
    } catch (err) {
      console.error('Session fetch error:', err);
      setError(err.message);
    }
  };

  const fetchProfessionalStats = async () => {
    try {
      const response = await fetch(`${API_BASE}/stats`);
      if (!response.ok) throw new Error('Failed to fetch statistics');
      const data = await response.json();
      setStats(data);
    } catch (err) {
      console.error('Stats fetch error:', err);
    }
  };

  // Enhanced data loading
  const loadProfessionalData = async () => {
    setLoading(true);
    setError(null);
    
    try {
      await Promise.all([fetchProfessionalSessions(), fetchProfessionalStats()]);
      setLastUpdate(new Date());
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // Initial professional load
  useEffect(() => {
    loadProfessionalData();
  }, []);

  // Professional auto-refresh
  useEffect(() => {
    if (!autoRefresh) return;

    const interval = setInterval(() => {
      loadProfessionalData();
    }, 30000); // Reduced refresh rate - manual refresh preferred

    return () => clearInterval(interval);
  }, [autoRefresh]);

  // Professional WebSocket connection
  useEffect(() => {
    let websocket;
    
    const connectProfessionalWebSocket = () => {
      try {
        websocket = new WebSocket(`ws://localhost:8001/ws/threats`);
        
        websocket.onopen = () => {
          console.log('🌐 Professional WebSocket connection established');
        };
        
        websocket.onmessage = (event) => {
          const message = JSON.parse(event.data);
          if (message.type === 'system_welcome') {
            console.log('🤖 Connected to AetherionBot Professional System');
          } else if (message.type === 'new_session' || message.type === 'threat_alert') {
            loadProfessionalData();
          }
        };
        
        websocket.onclose = () => {
          console.log('WebSocket disconnected, reconnecting shortly...');
          setTimeout(connectProfessionalWebSocket, 5000);
        };
        
        websocket.onerror = (error) => {
          console.error('Professional WebSocket error:', error);
        };
      } catch (err) {
        console.error('WebSocket connection initialization failed:', err);
      }
    };

    connectProfessionalWebSocket();

    return () => {
      if (websocket) {
        websocket.close();
      }
    };
  }, []);

  const handleSessionSelect = (session) => {
    setSelectedSession(session);
  };

  const handleProfessionalScan = async () => {
    const professionalScanPayloads = [
      { command: 'ls -la /etc', ip: '10.0.0.100', expected: 'MEDIUM' },
      { command: 'cat /etc/passwd | grep root', ip: '203.0.113.15', expected: 'HIGH' },
      { command: 'rm -rf /tmp/security_cache/*', ip: '198.51.100.50', expected: 'CRITICAL' },
      { command: 'python -c "import os; os.system(\'whoami\')"', ip: '172.16.1.200', expected: 'HIGH' },
      { command: 'nc -l 4444', ip: '203.0.113.25', expected: 'HIGH' }
    ];

    for (const payload of professionalScanPayloads) {
      try {
        const response = await fetch(`${API_BASE}/analyze`, {
          method: 'POST',
          headers: { 
            'Content-Type': 'application/json',
            'X-AetherionBot-Source': 'Professional-Dashboard'
          },
          body: JSON.stringify(payload)
        });
        
        if (response.ok) {
          const result = await response.json();
          console.log(`🎯 Professional scan "${payload.command}" -> ${result.threat_level} (Confidence: ${result.confidence})`);
          
          // Create professional session record
          await fetch(`${API_BASE}/sessions`, {
            method: 'POST',
            headers: { 
              'Content-Type': 'application/json',
              'X-AetherionBot-Source': 'Professional-Dashboard'
            },
            body: JSON.stringify({
              session_id: `professional_scan_${Date.now()}`,
              timestamp: new Date().toISOString(),
              ip: payload.ip,
              command: payload.command,
              threat_level: result.threat_level,
              anomaly_profile: 'test_case'
            })
          });
          
          // Professional timing
          await new Promise(resolve => setTimeout(resolve, 1500));
        }
      } catch (err) {
        console.error(`Professional scan failed for "${payload.command}":`, err);
      }
    }
    
    // Refresh professional data
    setTimeout(loadProfessionalData, 3000);
  };

  // Render Analytics Page
  if (currentPage === 'analytics') {
    return (
      <AnalyticsPage 
        sessions={sessions}
        stats={stats}
        loading={loading}
        onBack={() => setCurrentPage('dashboard')}
      />
    );
  }

  // Render Main Dashboard
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950 relative overflow-hidden">
      {/* Enhanced Background Pattern */}
      <div className="absolute inset-0 opacity-20">
        <div className="absolute inset-0" style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg width='60' height='60' viewBox='0 0 60 60' xmlns="http://www.w3.org/2000/svg"%3E%3Cg fill="none" fill-rule="evenodd"%3E%3Cg fill="%23ffffff" fill-opacity="0.02"%3E%3Ccircle cx="30" cy="30" r="1"/%3E%3C/g%3E%3C/g%3E%3C/svg%3E")`
        }}></div>
        {/* Floating Particles */}
        <div className="absolute top-1/4 left-1/4 w-2 h-2 bg-blue-400/30 rounded-full animate-pulse floating-particle" style={{animationDelay: '0s'}}></div>
        <div className="absolute top-1/3 right-1/3 w-1 h-1 bg-purple-400/40 rounded-full animate-bounce floating-particle" style={{animationDelay: '0.5s'}}></div>
        <div className="absolute bottom-1/4 left-1/2 w-3 h-3 bg-pink-400/20 rounded-full animate-pulse floating-particle" style={{animationDelay: '1s'}}></div>
        <div className="absolute top-3/4 right-1/4 w-1.5 h-1.5 bg-cyan-400/30 rounded-full animate-bounce floating-particle" style={{animationDelay: '1.5s'}}></div>
        <div className="absolute bottom-1/3 left-1/4 w-2 h-2 bg-yellow-400/20 rounded-full animate-pulse floating-particle" style={{animationDelay: '2s'}}></div>
        <div className="absolute top-1/2 right-1/6 w-1 h-1 bg-emerald-400/25 rounded-full animate-pulse floating-particle" style={{animationDelay: '2.5s'}}></div>
        <div className="absolute bottom-1/2 left-1/6 w-2.5 h-2.5 bg-indigo-400/15 rounded-full animate-bounce floating-particle" style={{animationDelay: '3s'}}></div>
      </div>

      {/* Professional Header */}
      <ProfessionalHeader 
        lastUpdate={lastUpdate}
        autoRefresh={autoRefresh}
        setAutoRefresh={setAutoRefresh}
        onRefresh={loadProfessionalData}
        onScan={handleProfessionalScan}
        loading={loading}
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        currentPage={currentPage}
        setCurrentPage={setCurrentPage}
      />


      {/* Main Content Area */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Error Banner */}
        {error && (
          <div className="bg-red-500/10 border border-red-500/30 rounded-lg p-4 mb-6">
            <div className="flex items-center space-x-3">
              <span className="text-red-400 text-xl">⚠️</span>
              <div>
                <h3 className="text-red-300 font-semibold">Connection Error</h3>
                <p className="text-red-200 text-sm">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Dashboard Content */}
        {activeTab === 'dashboard' && (
          <div className="space-y-6">
            {/* Stats Cards */}
            <div className="mb-8">
              <StatsCards 
                stats={stats} 
                loading={loading}
              />
            </div>

            {/* System Status Monitor - Horizontal Above */}
            <div className="mb-6">
              <SystemStatus stats={stats} />
            </div>

            {/* Main Grid - 2 Sections (60/40) */}
            <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
              {/* Section 1: Threat Sessions (60%) */}
              <div className="lg:col-span-3 bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-bold text-white">Threat Sessions</h2>
                  <span className="px-3 py-1 bg-blue-500/20 text-blue-300 text-sm rounded-full">
                    {sessions.length} Active
                  </span>
                </div>
                
                {loading ? (
                  <div className="text-center py-12">
                    <div className="animate-spin text-4xl mb-4">🔄</div>
                    <p className="text-gray-400">Loading session data...</p>
                  </div>
                ) : (
                  <SessionList 
                    sessions={sessions}
                    onSessionSelect={handleSessionSelect}
                    selectedSession={selectedSession}
                  />
                )}
              </div>

              {/* Section 2: Right Panel - Session Details & Quick Analytics (40%) */}
              <div className="lg:col-span-2 space-y-6">
                {/* Session Details */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6" data-section="session-details">
                  <h3 className="text-lg font-semibold text-white mb-4">Session Details</h3>
                  {selectedSession ? (
                    <SessionViewer 
                      session={selectedSession}
                      onClose={() => setSelectedSession(null)}
                    />
                  ) : (
                    <div className="text-center py-8">
                      <div className="text-gray-400 text-4xl mb-3">🔍</div>
                      <p className="text-gray-500 text-sm">Select a session to view details</p>
                    </div>
                  )}
                </div>

                {/* Quick Analytics Summary */}
                <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-semibold text-white flex items-center">
                      📊 Quick Analytics
                    </h3>
                    <button 
                      onClick={() => setCurrentPage('analytics')}
                      className="px-4 py-2 bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700 text-white text-sm font-semibold rounded-lg transition-all duration-300 transform hover:scale-105"
                    >
                      View Full Analytics →
                    </button>
                  </div>
                  
                  {/* Mini Stats */}
                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div className="bg-gray-900/30 rounded-lg p-3 text-center">
                      <div className="text-xl font-bold text-blue-400">
                        {sessions.reduce((sum, session) => {
                          const sessionTime = new Date(session.timestamp);
                          const now = new Date();
                          const hoursDiff = (now - sessionTime) / (1000 * 60 * 60);
                          return hoursDiff <= 24 ? sum + 1 : sum;
                        }, 0)}
                      </div>
                      <div className="text-xs text-gray-400">24h Threats</div>
                    </div>
                    <div className="bg-gray-900/30 rounded-lg p-3 text-center">
                      <div className="text-xl font-bold text-red-400">
                        {sessions.filter(s => s.threat_level === 'CRITICAL').length}
                      </div>
                      <div className="text-xs text-gray-400">Critical</div>
                    </div>
                  </div>
                  
                  {/* Simple Progress Bar */}
                  <div className="space-y-2">
                    <div className="flex justify-between text-xs text-gray-400">
                      <span>CRITICAL</span>
                      <span>{sessions.filter(s => s.threat_level === 'CRITICAL').length}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-red-500 to-red-600 h-2 rounded-full" 
                           style={{ width: `${Math.max((sessions.filter(s => s.threat_level === 'CRITICAL').length / Math.max(sessions.length, 1)) * 100, 10)}%` }}>
                      </div>
                    </div>
                    
                    <div className="flex justify-between text-xs text-gray-400">
                      <span>HIGH</span>
                      <span>{sessions.filter(s => s.threat_level === 'HIGH').length}</span>
                    </div>
                    <div className="w-full bg-gray-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full" 
                           style={{ width: `${Math.max((sessions.filter(s => s.threat_level === 'HIGH').length / Math.max(sessions.length, 1)) * 100, 10)}%` }}>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Professional Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="professional-card p-8">
            <h2 className="text-3xl font-bold text-white mb-8 flex items-center">
              📊 Professional Analytics Dashboard
              <span className="ml-4 px-4 py-2 bg-gradient-to-r from-emerald-600 to-blue-600 rounded-full text-sm font-medium">
                Enterprise Intelligence
              </span>
            </h2>
            
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
              {/* Attack Vector Distribution */}
              <div className="bg-gray-800 bg-opacity-40 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4">🎯 Attack Vector Analysis</h3>
                <div className="space-y-3">
                  {Object.entries(stats.attack_vectors || {}).map(([vector, count]) => (
                    <div key={vector} className="flex items-center justify-between">
                      <span className="text-gray-300 text-sm">{vector}</span>
                      <div className="flex items-center space-x-3">
                        <div className="w-24 bg-gray-700 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full"
                            style={{ width: `${(count / Math.max(...Object.values(stats.attack_vectors || {}))) * 100}%` }}
                          />
                        </div>
                        <span className="text-white font-medium text-sm">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Geographic Distribution */}
              <div className="bg-gray-800 bg-opacity-40 rounded-xl p-6">
                <h3 className="text-lg font-semibold text-white mb-4">🌍 Geographic Threat Distribution</h3>
                <div className="space-y-3">
                  {Object.entries(stats.geographic_distribution || {}).slice(0, 5).map(([location, count]) => (
                    <div key={location} className="flex items-center justify-between">
                      <span className="text-gray-300 text-sm">{location}</span>
                      <div className="flex items-center space-x-3">
                        <div className="w-24 bg-gray-700 rounded-full h-2">
                          <div 
                            className="bg-gradient-to-r from-emerald-500 to-teal-500 h-2 rounded-full"
                            style={{ width: `${(count / Math.max(...Object.values(stats.geographic_distribution || {}))) * 100}%` }}
                          />
                        </div>
                        <span className="text-white font-medium text-sm">{count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            <div className="mt-8 text-center">
              <button 
                onClick={() => setActiveTab('dashboard')}
                className="px-6 py-3 bg-gradient-to-r from-purple-600 to-blue-600 hover:from-purple-700 hover:to-blue-700 rounded-xl font-medium transition-all duration-200"
              >
                🏠 Return to Dashboard
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Professional Footer */}
      <footer className="mt-24 bg-gradient-to-r from-slate-950/80 to-blue-950/80 backdrop-blur-xl border-t border-white/5">
        <div className="container mx-auto px-8 py-8">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="space-y-4">
              <div className="flex items-center space-x-3">
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                  <span className="text-white text-lg">🛡️</span>
                </div>
                <h3 className="text-white font-black text-xl">AetherionBot</h3>
              </div>
              <p className="text-gray-400 text-sm leading-relaxed">
                Enterprise-grade threat detection and analysis platform powered by advanced AI/ML algorithms.
              </p>
              <div className="flex items-center space-x-4 text-xs text-gray-500">
                <span className="px-3 py-1 bg-gradient-to-r from-green-500/20 to-emerald-500/20 border border-green-400/30 rounded-full">
                  v1.0.0 Enterprise
                </span>
              </div>
            </div>
            
            <div className="space-y-4">
              <h4 className="text-gray-300 font-bold text-sm uppercase tracking-wider">Quick Access</h4>
              <div className="space-y-2">
                <a href="http://localhost:8001/docs" target="_blank" rel="noopener noreferrer" className="block text-gray-400 hover:text-white transition-colors text-sm">
                  📚 API Documentation
                </a>
                <a href={`${API_BASE}/health`} target="_blank" rel="noopener noreferrer" className="block text-gray-400 hover:text-white transition-colors text-sm">
                  🔍 System Health Monitor
                </a>
                <span className="block text-gray-400 text-sm">
                  📊 Real-time Analytics Dashboard
                </span>
              </div>
            </div>
            
            <div className="space-y-4">
              <h4 className="text-gray-300 font-bold text-sm uppercase tracking-wider">System Status</h4>
              <div className="space-y-2 text-xs">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">API Endpoints:</span>
                  <span className="px-2 py-1 bg-green-500/20 text-green-400 rounded text-xs">8 Active</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">Honeypot:</span>
                  <span className="px-2 py-1 bg-blue-500/20 text-blue-400 rounded text-xs">Port 2222</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-400">WebSocket:</span>
                  <span className="px-2 py-1 bg-purple-500/20 text-purple-400 rounded text-xs">Connected</span>
                </div>
              </div>
            </div>
          </div>
          
          <div className="border-t border-white/5 mt-8 pt-6 text-center">
            <p className="text-gray-500 text-sm">
              © 2025 AetherionBot Enterprise | Professional Threat Detection System | All Rights Reserved
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
}

export default App;