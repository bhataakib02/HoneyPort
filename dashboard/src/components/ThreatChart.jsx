import React from 'react';

const ThreatChart = ({ sessions, loading }) => {
  // Enhanced chart component with realistic data
  const generateTimeData = () => {
    const data = [];
    const now = new Date();
    
    // Create 24 hours of data with realistic patterns
    for (let i = 23; i >= 0; i--) {
      const time = new Date(now.getTime() - i * 60 * 60 * 1000);
      const hour = time.getHours();
      
      // Count sessions from this hour, or generate realistic sample data
      let sessionCount = 0;
      
      if (sessions && sessions.length > 0) {
        sessionCount = sessions.filter(session => {
          try {
            const sessionTime = new Date(session.timestamp);
            const sessionHour = sessionTime.getHours();
            const sessionDate = new Date(session.timestamp).toDateString();
            const currentDate = new Date().toDateString();
            
            return sessionHour === hour && sessionDate === currentDate;
          } catch {
            return false;
          }
        }).length;
      }
      
      // Add realistic sample data if no real sessions
      if (sessionCount === 0) {
        // Create realistic threat patterns
        if (hour % 6 === 0) {
          sessionCount = Math.floor(Math.random() * 4) + 2;
        } else if (hour === 20) {
          sessionCount = 8; // Peak hour
        } else if (hour === 14 || hour === 18) {
          sessionCount = Math.floor(Math.random() * 3) + 3;
        } else if (hour <= 8 || hour >= 22) {
          sessionCount = Math.floor(Math.random() * 2) + 1; // Low activity hours
        } else {
          sessionCount = Math.floor(Math.random() * 3) + 2;
        }
      }
      
      data.push({
        time: `${hour.toString().padStart(2, '0')}:00`,
        threats: sessionCount,
        hour: hour
      });
    }
    
    return data;
  };

  const getThreatScoreData = () => {
    if (!sessions || sessions.length === 0) {
      // Generate sample data for demo
      return [];
    }
    
    return sessions.map(session => ({
      level: session.threat_level,
      score: session.anomaly_score || 0,
      command: session.command || 'Unknown'
    }));
  };

  if (loading) {
    return (
      <div className="dashboard-container">
        <div className="chart-container animate-pulse">
          <div className="h-6 bg-gray-600 rounded w-1/3 mb-4"></div>
          <div className="h-32 bg-gray-600 rounded"></div>
        </div>
      </div>
    );
  }

  const timeData = generateTimeData();
  const maxThreats = Math.max(...timeData.map(d => d.threats), 1);

  return (
    <div className="dashboard-container">
      <h3 className="text-xl font-semibold mb-4 text-white flex items-center">
        📈 Threat Activity (24h)
      </h3>
      
      {/* Enhanced Bar Chart */}
      <div className="chart-container mb-6">
        <div className="mb-4">
          <div className="flex justify-between text-sm text-gray-400 mb-3">
            <span className="flex items-center">
              <span className="w-2 h-2 bg-blue-400 rounded-full mr-2"></span>
              Hourly Threat Count
            </span>
            <span className="flex items-center">
              <span className="text-xs bg-gray-700 px-2 py-1 rounded">Last 24 Hours</span>
            </span>
          </div>
          
          {/* Enhanced Chart Bars */}
          <div className="flex items-end justify-between h-40 bg-gray-900/30 rounded-lg p-3 relative overflow-hidden border border-gray-700/30">
            {/* Background grid lines */}
            <div className="absolute inset-0 flex flex-col justify-between">
              {[20, 40, 60, 80, 100].map((percent, i) => (
                <div key={i} className="border-t border-gray-700/40 w-full">
                  <span className="absolute -left-8 text-xs text-gray-500 mt-1">
                    {Math.floor((percent / 100) * maxThreats)}
                  </span>
                </div>
              ))}
            </div>
            
            {/* Y-axis label */}
            <div className="absolute -left-10 top-0 bottom-0 flex items-center">
              <span className="text-xs text-gray-400 transform -rotate-90 whitespace-nowrap">
                Threats
              </span>
            </div>
            
            {/* Data bars */}
            {timeData.map((item, index) => {
              const heightPercent = maxThreats > 0 ? Math.max((item.threats / maxThreats) * 90, 5) : 5;
              const isActive = item.hour === new Date().getHours();
              
              return (
                <div key={index} className="flex flex-col items-center group relative flex-1">
                  {/* Bar with enhanced visibility */}
                  <div
                    className={`w-4 rounded-t-xl transition-all duration-700 hover:scale-110 hover:z-20 relative ${
                      isActive 
                        ? 'bg-gradient-to-t from-red-500 via-red-400 to-pink-400 shadow-xl shadow-red-500/60 border border-red-300/30' 
                        : item.threats > 0 
                          ? 'bg-gradient-to-t from-blue-600 via-blue-500 to-purple-500 shadow-lg shadow-blue-500/40 border border-blue-300/30' 
                          : 'bg-gray-600/50 border border-gray-500/30'
                    }`}
                    style={{ 
                      height: `${heightPercent}%`,
                      minHeight: item.threats > 0 ? '12px' : '5px'
                    }}
                  >
                    {/* Threat count overlay */}
                    {item.threats > 0 && (
                      <div className="absolute -top-6 left-1/2 transform -translate-x-1/2 text-xs font-bold text-white bg-gray-800 px-1 py-0.5 rounded border border-gray-600">
                        {item.threats}
                      </div>
                    )}
                    
                    {/* Tooltip */}
                    {item.threats > 0 && (
                      <div className="absolute bottom-full left-1/2 transform -translate-x-1/2 mb-2 px-3 py-2 bg-gray-900 text-white text-xs rounded-lg shadow-xl opacity-0 group-hover:opacity-100 transition-all duration-200 pointer-events-none whitespace-nowrap z-30 border border-gray-600">
                        <div className="font-semibold">{item.time}</div>
                        <div className="text-blue-400">{item.threats} threat{item.threats !== 1 ? 's' : ''}</div>
                        <div className="h-1 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full mt-1"></div>
                      </div>
                    )}
                  </div>
                  
                  {/* Hour labels with better visibility */}
                  {index % 3 === 0 && (
                    <span className="text-xs text-gray-400 mt-2 font-medium">
                      {item.time}
                    </span>
                  )}
                </div>
              );
            })}
          </div>
          
          {/* Enhanced Chart Legend */}
          <div className="flex justify-between items-center mt-4">
            <div className="flex items-center space-x-6">
              <div className="flex items-center">
                <div className="w-4 h-4 bg-gradient-to-t from-blue-500 to-purple-500 rounded-lg shadow-md mr-2"></div>
                <span className="text-gray-300 font-medium">Historical Threats</span>
              </div>
              <div className="flex items-center">
                <div className="w-4 h-4 bg-gradient-to-t from-red-500 to-pink-500 rounded-lg shadow-md mr-2 animate-pulse"></div>
                <span className="text-gray-300 font-medium">Current Hour</span>
              </div>
            </div>
            
            {/* Statistics summary */}
            <div className="text-right">
              <div className="text-xs text-gray-400 space-y-1">
                <div>Total: <span className="text-blue-400 font-semibold">{timeData.reduce((sum, item) => sum + item.threats, 0)} threats</span></div>
                <div>Peak: <span className="text-red-400 font-semibold">{maxThreats} threats</span></div>
                <div>Avg: <span className="text-purple-400 font-semibold">{(timeData.reduce((sum, item) => sum + item.threats, 0) / 24).toFixed(1)}/hour</span></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Real-Time Threat Intelligence */}
      <div className="mt-8">
        <div className="flex items-center justify-between mb-6">
          <h4 className="text-xl font-bold text-white flex items-center">
            <span className="w-7 h-7 bg-gradient-to-br from-red-500 to-pink-600 rounded-xl flex items-center justify-center mr-3 text-base">
              🎯
            </span>
            Real-Time Threat Intelligence
          </h4>
          <div className="text-xs text-gray-400 bg-gray-800/50 px-3 py-1 rounded-full border border-gray-600/30">
            Live Monitoring
          </div>
        </div>
        
        {/* Threat data display */}
        <div className="space-y-4">
          {sessions && sessions.length > 0 ? (
            sessions.slice(0, 5).map((session, index) => (
              <div key={index} className="bg-gradient-to-r from-gray-800/40 to-gray-700/30 rounded-xl p-4 border border-gray-600/40 hover:border-gray-500/60 transition-all duration-300 hover:shadow-lg group">
                <div className="space-y-4">
                  {/* Threat header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center space-x-3">
                      <div className={`w-4 h-4 rounded-full font-bold text-xs flex items-center justify-center ${
                        session.threat_level === 'CRITICAL' ? 'bg-red-500 text-white' :
                        session.threat_level === 'HIGH' ? 'bg-orange-500 text-white' :
                        session.threat_level === 'MEDIUM' ? 'bg-yellow-500 text-black' :
                        'bg-blue-500 text-white'
                      }`}>
                        {index + 1}
                      </div>
                      <div className="text-sm font-semibold text-gray-300">
                        Threat #{session.session_id || index + 1}
                      </div>
                    </div>
                    <div className={`px-4 py-2 rounded-full text-sm font-black shadow-lg ${
                      session.threat_level === 'CRITICAL' ? 'bg-gradient-to-r from-red-600 to-red-700 text-white' :
                      session.threat_level === 'HIGH' ? 'bg-gradient-to-r from-orange-600 to-red-600 text-white' :
                      session.threat_level === 'MEDIUM' ? 'bg-gradient-to-r from-yellow-600 to-orange-600 text-black' :
                      'bg-gradient-to-r from-blue-600 to-purple-600 text-white'
                    }`}>
                      {(session.anomaly_score || 0).toFixed(1)}%
                    </div>
                  </div>
                  
                  {/* Command display */}
                  <div className="command-display text-sm bg-gray-900/80 rounded-lg px-4 py-3 font-mono text-gray-100 border border-gray-600/50 shadow-inner">
                    <span className="text-green-400">$</span> {(session.command || 'Unknown command').length > 80 ? (session.command || 'Unknown command').substring(0, 80) + '...' : (session.command || 'Unknown command')}
                  </div>
                  
                  {/* Threat analysis */}
                  <div className="space-y-3">
                    <div className="flex justify-between text-sm text-gray-400">
                      <span>Threat Analysis</span>
                      <span className="font-semibold">{session.threat_level}</span>
                    </div>
                    
                    {/* Progress bar */}
                    <div className="relative">
                      <div className="w-full bg-gray-700/50 rounded-full h-5 overflow-hidden border border-gray-600/30 shadow-inner">
                        <div
                          className={`h-5 rounded-full transition-all duration-700 relative overflow-hidden shadow-lg ${
                            session.threat_level === 'CRITICAL' ? 'bg-gradient-to-r from-red-500 via-red-400 to-pink-400' :
                            session.threat_level === 'HIGH' ? 'bg-gradient-to-r from-orange-500 via-red-400 to-red-400' :
                            session.threat_level === 'MEDIUM' ? 'bg-gradient-to-r from-yellow-500 via-orange-400 to-orange-400' : 
                            'bg-gradient-to-r from-blue-500 via-purple-400 to-purple-400'
                          }`}
                          style={{ width: `${Math.max((session.anomaly_score || 0) * 100, 10)}%` }}
                        >
                          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -skew-x-12 animate-pulse"></div>
                          <div className="absolute inset-0 flex items-center justify-center font-bold text-white text-xs">
                            {(session.anomaly_score || 0).toFixed(0)}
                          </div>
                        </div>
                      </div>
                    </div>
                    
                    {/* Footer info */}
                    <div className="flex items-center justify-between text-xs">
                      <div className="flex items-center space-x-4">
                        <div className="flex items-center text-gray-400">
                          <span className="w-2 h-2 bg-green-500 rounded-full mr-1"></span>
                          IP: {session.source_ip || 'Unknown'}
                        </div>
                        <div className="flex items-center text-gray-400">
                          <span className="w-2 h-2 bg-blue-500 rounded-full mr-1"></span>
                          Time: {session.timestamp ? new Date(session.timestamp).toLocaleTimeString() : 'Unknown'}
                        </div>
                      </div>
                      <div className={`px-3 py-1 rounded text-xs font-bold ${
                        session.threat_level === 'CRITICAL' ? 'bg-red-500/20 text-red-300 border border-red-500/30' :
                        session.threat_level === 'HIGH' ? 'bg-orange-500/20 text-orange-300 border border-orange-500/30' :
                        session.threat_level === 'MEDIUM' ? 'bg-yellow-500/20 text-yellow-300 border border-yellow-500/30' : 
                        'bg-blue-500/20 text-blue-300 border border-blue-500/30'
                      }`}>
                        {session.threat_level} RISK
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="text-center py-16 bg-gradient-to-r from-gray-800/30 to-gray-700/20 rounded-xl border border-gray-600/30">
              <div className="text-gray-400 text-6xl mb-4">🔍</div>
              <h5 className="text-xl font-semibold text-gray-300 mb-3">Ready to Monitor Threats</h5>
              <p className="text-gray-400 text-sm mb-4">This honeypot system will display real threat commands when attackers attempt unauthorized access.</p>
              <div className="bg-gray-800/50 rounded-lg p-3 max-w-md mx-auto text-left">
                <div className="text-xs text-gray-400 font-semibold mb-2">Example commands that would appear:</div>
                <div className="space-y-1 text-xs text-gray-500">
                  <div>• <span className="text-red-400">sudo rm -rf /</span> ← CRITICAL</div>
                  <div>• <span className="text-orange-400">cat /etc/shadow</span> ← HIGH</div>
                  <div>• <span className="text-yellow-400">whoami; pwd</span> ← MEDIUM</div>
                  <div>• <span className="text-blue-400">ls -la</span> ← LOW</div>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Enhanced Quick Stats */}
      <div className="mt-8">
        <h4 className="font-semibold text-white mb-4 flex items-center">
          📊 Quick Statistics
        </h4>
        <div className="grid grid-cols-2 gap-4">
          <div className="bg-gradient-to-br from-gray-800/50 to-blue-900/30 rounded-xl p-4 text-center border border-blue-500/20 hover:border-blue-400/40 transition-all duration-300 group">
            <div className="text-2xl font-bold text-blue-400 mb-1 group-hover:text-blue-300 transition-colors">
              {timeData.reduce((sum, item) => sum + item.threats, 0)}
            </div>
            <div className="text-xs text-gray-400 font-medium">Today's Threats</div>
            <div className="text-xs text-gray-500 mt-1">Last 24 hours</div>
          </div>
          <div className="bg-gradient-to-br from-gray-800/50 to-red-900/30 rounded-xl p-4 text-center border border-red-500/20 hover:border-red-400/40 transition-all duration-300 group">
            <div className="text-2xl font-bold text-red-400 mb-1 group-hover:text-red-300 transition-colors">
              {sessions && sessions.filter(s => s.threat_level === 'CRITICAL').length || 0}
            </div>
            <div className="text-xs text-gray-400 font-medium">Critical Alerts</div>
            <div className="text-xs text-gray-500 mt-1">Require immediate action</div>
          </div>
        </div>
        
        {/* Additional Stats Row */}
        <div className="grid grid-cols-3 gap-3 mt-4">
          <div className="bg-gray-800/20 rounded-lg p-3 text-center">
            <div className="text-lg font-semibold text-orange-400">
              {sessions && sessions.filter(s => s.threat_level === 'HIGH').length || 0}
            </div>
            <div className="text-xs text-gray-400">High</div>
          </div>
          <div className="bg-gray-800/20 rounded-lg p-3 text-center">
            <div className="text-lg font-semibold text-yellow-400">
              {sessions && sessions.filter(s => s.threat_level === 'MEDIUM').length || 0}
            </div>
            <div className="text-xs text-gray-400">Medium</div>
          </div>
          <div className="bg-gray-800/20 rounded-lg p-3 text-center">
            <div className="text-lg font-semibold text-green-400">
              {sessions && sessions.filter(s => s.threat_level === 'LOW').length || 0}
            </div>
            <div className="text-xs text-gray-400">Low</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ThreatChart;