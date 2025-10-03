import React, { useState, useEffect } from 'react';
import ThreatChart from './ThreatChart';
import SystemStatus from './SystemStatus';

const API_BASE = 'http://localhost:8001';

const AnalyticsPage = ({ sessions, stats, loading, onBack }) => {
  const [timeRange, setTimeRange] = useState('24h');
  const [chartType, setChartType] = useState('bar');
  const [detailedStats, setDetailedStats] = useState(stats);

  useEffect(() => {
    // Load additional analytics data
    const fetchDetailedStats = async () => {
      try {
        const response = await fetch(`${API_BASE}/analytics`);
        if (response.ok) {
          const data = await response.json();
          setDetailedStats(data);
        }
      } catch (error) {
        console.log('Analytics endpoint not available, using basic stats');
      }
    };

    fetchDetailedStats();
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-blue-950">
      {/* Analytics Header */}
      <div className="bg-gradient-to-r from-slate-900/95 via-slate-800/95 to-purple-900/95 backdrop-blur-xl border-b border-white/10 py-6">
        <div className="max-w-7xl mx-auto px-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={onBack}
                className="flex items-center space-x-2 px-4 py-2 bg-blue-600/20 hover:bg-blue-600/30 text-blue-300 hover:text-blue-200 border border-blue-500/30 rounded-lg transition-all duration-300 hover:scale-105"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
                </svg>
                <span>Back to Dashboard</span>
              </button>
              
              <div className="flex items-center space-x-3">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-xl flex items-center justify-center">
                  <span className="text-white text-xl">📊</span>
                </div>
                <div>
                  <h1 className="text-2xl font-bold text-white">Advanced Analytics</h1>
                  <p className="text-gray-400 text-sm">Comprehensive threat intelligence & trends</p>
                </div>
              </div>
            </div>

            {/* Time Range Selector */}
            <div className="flex items-center space-x-3">
              <span className="text-gray-400 text-sm">Time Range:</span>
              <select 
                value={timeRange} 
                onChange={(e) => setTimeRange(e.target.value)}
                className="bg-gray-800/50 border border-gray-600 rounded-lg px-3 py-2 text-white text-sm focus:border-blue-500 focus:outline-none"
              >
                <option value="1h">Last Hour</option>
                <option value="24h">Last 24 Hours</option>
                <option value="7d">Last 7 Days</option>
                <option value="30d">Last 30 Days</option>
              </select>
            </div>
          </div>
        </div>
      </div>

      {/* Main Analytics Content */}
      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* System Status Summary */}
        <div className="mb-8">
          <SystemStatus stats={detailedStats} />
        </div>

        {/* Analytics Grid */}
        <div className="space-y-8">
          {/* Threat Activity Charts */}
          <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-2xl p-8">
            <div className="flex items-center justify-between mb-6">
              <h2 className="text-xl font-bold text-white flex items-center">
                <span className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center mr-3">
                  📈
                </span>
                Threat Activity Analysis
              </h2>
              
              <div className="flex items-center space-x-3">
                <span className="text-gray-400 text-sm">Chart Type:</span>
                <div className="flex bg-gray-700/50 rounded-lg p-1">
                  <button 
                    onClick={() => setChartType('bar')}
                    className={`px-3 py-1 text-xs rounded transition-all ${
                      chartType === 'bar' ? 'bg-blue-600 text-white' : 'text-gray-400 bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Bar
                  </button>
                  <button 
                    onClick={() => setChartType('line')}
                    className={`px-3 py-1 text-xs rounded transition-all ${
                      chartType === 'line' ? 'bg-blue-600 text-white' : 'text-gray-400 bg-gray-700/50 hover:text-white'
                    }`}
                  >
                    Line
                  </button>
                </div>
              </div>
            </div>

            <ThreatChart sessions={sessions} loading={loading} />
          </div>

          {/* Enhanced Statistics Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Attack Patterns */}
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <span className="w-6 h-6 bg-gradient-to-br from-orange-500 to-red-600 rounded-lg flex items-center justify-center mr-2 text-sm">
                  🎯
                </span>
                Attack Patterns
              </h3>
              
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-gray-400 text-sm">Command Injection</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-red-500 to-pink-500 h-2 rounded-full" style={{ width: '78%' }}></div>
                    </div>
                    <span className="text-white text-sm font-medium">78%</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-400 text-sm">File Access</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-orange-500 to-red-500 h-2 rounded-full" style={{ width: '65%' }}></div>
                    </div>
                    <span className="text-white text-sm font-medium">65%</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-400 text-sm">Network Scans</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-yellow-500 to-orange-500 h-2 rounded-full" style={{ width: '45%' }}></div>
                    </div>
                    <span className="text-white text-sm font-medium">45%</span>
                  </div>
                </div>
                
                <div className="flex items-center justify-between">
                  <span className="text-gray-400 text-sm">System Recon</span>
                  <div className="flex items-center space-x-2">
                    <div className="w-24 bg-gray-700 rounded-full h-2">
                      <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full" style={{ width: '32%' }}></div>
                    </div>
                    <span className="text-white text-sm font-medium">32%</span>
                  </div>
                </div>
              </div>
            </div>

            {/* Geographic Distribution */}
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <span className="w-6 h-6 bg-gradient-to-br from-green-500 to-blue-600 rounded-lg flex items-center justify-center mr-2 text-sm">
                  🌍
                </span>
                Geographic Threat Map
              </h3>
              
              <div className="space-y-3">
                <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white text-sm font-medium">United States</span>
                    <span className="text-red-400 text-sm font-bold">34%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-red-500 to-red-600 h-2 rounded-full" style={{ width: '34%' }}></div>
                  </div>
                </div>
                
                <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white text-sm font-medium">China</span>
                    <span className="text-orange-400 text-sm font-bold">28%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-orange-500 to-orange-600 h-2 rounded-full" style={{ width: '28%' }}></div>
                  </div>
                </div>
                
                <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white text-sm font-medium">Russia</span>
                    <span className="text-yellow-400 text-sm font-bold">19%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-yellow-500 to-yellow-600 h-2 rounded-full" style={{ width: '19%' }}></div>
                  </div>
                </div>
                
                <div className="bg-gray-900/50 rounded-lg p-3 border border-gray-700/30">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-white text-sm font-medium">Others</span>
                    <span className="text-gray-400 text-sm font-bold">19%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-gray-500 to-gray-600 h-2 rounded-full" style={{ width: '19%' }}></div>
                  </div>
                </div>
              </div>
            </div>

            {/* System Health */}
            <div className="bg-slate-800/50 backdrop-blur-sm border border-slate-700/50 rounded-xl p-6">
              <h3 className="text-lg font-semibold text-white mb-4 flex items-center">
                <span className="w-6 h-6 bg-gradient-to-br from-emerald-500 to-teal-600 rounded-lg flex items-center justify-center mr-2 text-sm">
                  ⚡
                </span>
                System Performance
              </h3>
              
              <div className="space-y-4">
                <div className="text-center">
                  <div className="text-3xl font-bold text-green-400 mb-2">98.7%</div>
                  <div className="text-gray-400 text-sm mb-4">Uptime</div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div className="bg-gradient-to-r from-green-500 to-emerald-500 h-2 rounded-full" style={{ width: '98.7%' }}></div>
                  </div>
                </div>
                
                <div className="grid grid-cols-2 gap-4 text-center">
                  <div className="bg-gray-900/50 rounded-lg p-3">
                    <div className="text-lg font-semibold text-blue-400">2.3ms</div>
                    <div className="text-xs text-gray-400">Avg Response</div>
                  </div>
                  <div className="bg-gray-900/50 rounded-lg p-3">
                    <div className="text-lg font-semibold text-purple-400">156</div>
                    <div className="text-xs text-gray-400">Alerts/min</div>
                  </div>
                </div>
                
                <div className="bg-green-900/20 border border-green-500/30 rounded-lg p-3">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-2">
                      <div className="w-2 h-2 bg-green-400 rounded-full animate-pulse"></div>
                      <span className="text-green-400 text-sm font-medium">All Systems Operational</span>
                    </div>
                    <span className="text-green-400 text-xs">🟢</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsPage;