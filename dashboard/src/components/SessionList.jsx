import React from 'react';

const SessionList = ({ sessions, onSessionSelect, selectedSession }) => {
  const handleSessionClick = (session, e) => {
    onSessionSelect(session);
    
    // Add visual feedback
    if (e?.target) {
      const sessionElement = e.target.closest('.session-item');
      if (sessionElement) {
        sessionElement.classList.add('session-selecting');
        setTimeout(() => {
          sessionElement.classList.remove('session-selecting');
        }, 500);
      }
    }
    
    // Auto-scroll to Session Details section
    setTimeout(() => {
      const sessionDetailsSection = document.querySelector('[data-section="session-details"]');
      if (sessionDetailsSection) {
        // Add highlighting effect
        sessionDetailsSection.classList.add('session-details-highlight');
        setTimeout(() => {
          sessionDetailsSection.classList.remove('session-details-highlight');
        }, 1000);

        sessionDetailsSection.scrollIntoView({ 
          behavior: 'smooth', 
          block: 'start',
          inline: 'nearest'
        });
      }
    }, 100);
  };

  const handleButtonClick = (session, e) => {
    e.stopPropagation();
    
    // Add button press animation
    const button = e.target;
    button.classList.add('button-press');
    setTimeout(() => {
      button.classList.remove('button-press');
    }, 200);
    
    // Handle session selection
    handleSessionClick(session, e);
  };
  const getThreatBadgeClass = (level) => {
    return `px-2 py-1 rounded-full text-xs font-semibold threat-${level.toLowerCase()}`;
  };

  const formatTimestamp = (timestamp) => {
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diffMs = now - date;
      const diffMins = Math.floor(diffMs / (1000 * 60));
      const diffHours = Math.floor(diffMs / (1000 * 60 * 60));
      const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));

      if (diffMins < 1) return 'Just now';
      if (diffMins < 60) return `${diffMins}m ago`;
      if (diffHours < 24) return `${diffHours}h ago`;
      if (diffDays < 7) return `${diffDays}d ago`;
      
      return date.toLocaleDateString();
    } catch (error) {
      return 'Unknown';
    }
  };

  const formatIP = (ip) => {
    // Check if it's an internal IP
    const internalIPs = ['192.168.', '10.', '172.16.', '127.', '::1'];
    const isInternal = internalIPs.some(prefix => ip.startsWith(prefix));
    
    return (
      <span className={`ip-badge ${isInternal ? 'bg-yellow-600 bg-opacity-20 text-yellow-300 border-yellow-500' : 'bg-blue-600 bg-opacity-20 text-blue-300 border-blue-500'}`}>
        {ip} {isInternal ? '(Internal)' : '(External)'}
      </span>
    );
  };

  const truncateCommand = (command, maxLength = 50) => {
    if (command.length <= maxLength) return command;
    return command.substring(0, maxLength) + '...';
  };

  const getSeverityIcon = (level) => {
    switch (level) {
      case 'CRITICAL': return '🚨';
      case 'HIGH': return '⚠️';
      case 'MEDIUM': return '⚡';
      case 'LOW': return 'ℹ️';
      default: return '❓';
    }
  };

  const sortedSessions = [...sessions].sort((a, b) => {
    // Sort by threat level priority (CRITICAL > HIGH > MEDIUM > LOW)
    const threatOrder = { 'CRITICAL': 4, 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
    const aLevel = threatOrder[a.threat_level] || 0;
    const bLevel = threatOrder[b.threat_level] || 0;
    
    if (aLevel !== bLevel) return bLevel - aLevel;
    
    // Then by timestamp (newest first)
    return new Date(b.timestamp || 0) - new Date(a.timestamp || 0);
  });

  if (sessions.length === 0) {
    return (
      <div className="text-center py-16">
        <div className="text-gray-400 text-8xl mb-6 animate-pulse">🛡️</div>
        <h3 className="text-3xl font-bold text-gray-200 mb-4">AetherionBot Ready</h3>
        <p className="text-gray-400 mb-8 text-lg">
          Professional Threat Detection System Active • Awaiting Security Events
        </p>
        
        <div className="bg-gradient-to-r from-slate-800 to-purple-800 rounded-2xl p-8 max-w-2xl mx-auto border border-gray-600">
          <h4 className="font-bold text-white mb-6 text-xl">🚀 Quick Professional Test Commands:</h4>
          <div className="space-y-3 text-sm font-mono bg-black bg-opacity-30 rounded-xl p-6">
            <div className="command-code bg-blue-900 bg-opacity-30 px-4 py-2 rounded-lg">
              <span className="text-green-400">$</span> nc localhost 2222  
              <span className="text-gray-400 ml-2"># Connect to honeypot</span>
            </div>
            <div className="command-code bg-orange-900 bg-opacity-30 px-4 py-2 rounded-lg">
              <span className="text-green-400">$</span> cat /etc/passwd    
              <span className="text-gray-400 ml-2"># Suspicious reconnaissance</span>
            </div>
            <div className="command-code bg-red-900 bg-opacity-30 px-4 py-2 rounded-lg">
              <span className="text-green-400">$</span> rm -rf /tmp/*      
              <span className="text-gray-400 ml-2"># Critical threat test</span>
            </div>
          </div>
          
          <div className="mt-6 p-4 bg-green-900 bg-opacity-20 rounded-lg border border-green-600">
            <p className="text-green-400 font-medium">
              ✅ Threat Detection Engine | ✅ AI Analysis Module | ✅ WebSocket Service | ✅ Data Pipeline
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {/* Enhanced Summary Bar */}
      <div className="bg-gradient-to-r from-gray-800 via-purple-900 to-gray-800 rounded-xl p-6 mb-8 border border-gray-600 shadow-lg">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-8">
            <div className="flex items-center space-x-3">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-gray-300 font-medium">
                📊 {sessions.length} Active Session{sessions.length !== 1 ? 's' : ''} Captured
              </span>
            </div>
            <div className="text-gray-400">
              🎯 Sorting: Threat Priority (Critical → High → Medium → Low)
            </div>
          </div>
          
          <div className="flex items-center space-x-4">
            <div className="px-3 py-1 bg-gradient-to-r from-red-600 to-red-700 rounded-full text-xs font-bold">
              🚨 Critical Priority
            </div>
          </div>
        </div>
        <div className="flex items-center space-x-4">
          {Object.entries({ CRITICAL: 0, HIGH: 0, MEDIUM: 0, LOW: 0 }).map(([level, count]) => {
            const actualCount = sessions.filter(s => s.threat_level === level).length;
            if (actualCount === 0) return null;
            return (
              <span key={level} className="flex items-center space-x-2">
                <span>{getSeverityIcon(level)}</span>
                <span className="text-sm">
                  {actualCount} {level}
                </span>
              </span>
            );
          })}
        </div>
      </div>

      {/* Enhanced Sessions Grid */}
      <div className="space-y-4">
        {sortedSessions.map((session, index) => (
          <div
            key={session.session_id || sessions.indexOf(session)}
            onClick={(e) => handleSessionClick(session, e)}
            className={`relative session-item cursor-pointer transition-all duration-300 transform hover:scale-[1.02] ${
              selectedSession?.session_id === session.session_id
                ? 'bg-gradient-to-r from-blue-600 to-purple-600 bg-opacity-20 border-blue-400 border-opacity-60 shadow-lg shadow-blue-500/20'
                : 'hover:bg-gradient-to-r hover:from-gray-800 hover:to-purple-800 hover:bg-opacity-20 hover:shadow-lg hover:shadow-purple-500/10'
            }`}
          >
            <div className="flex items-start justify-between">
              <div className="flex items-start space-x-4 flex-1">
                {/* Threat Level Icon */}
                <div className="text-2xl mt-1">
                  {getSeverityIcon(session.threat_level)}
                </div>

                <div className="flex-1 min-w-0">
                  {/* IP and Threat Badge */}
                  <div className="flex items-center space-x-3 mb-2">
                    {formatIP(session.ip)}
                    <span className={getThreatBadgeClass(session.threat_level)}>
                      {session.threat_level} • Score: {(session.anomaly_score || 0).toFixed(3)}
                    </span>
                  </div>

                  {/* Command */}
                  <div className="command-code mb-2">
                    {truncateCommand(session.command || 'No command', 60)}
                  </div>

                  {/* Response Preview */}
                  {session.response && (
                    <div className="text-sm text-gray-500 mb-2">
                      Response: <code className="text-gray-400">{session.response.substring(0, 100)}</code>
                    </div>
                  )}
                </div>
              </div>

              {/* Time and Actions */}
              <div className="flex flex-col items-end space-y-2 text-right">
                <div className="timestamp text-xs">
                  {formatTimestamp(session.timestamp)}
                </div>
                
                {!(session.command || '').includes('test') && (
                  <button 
                    onClick={(e) => handleButtonClick(session, e)}
                    className="mt-2 px-3 py-1.5 bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white text-xs font-semibold rounded-lg shadow-lg hover:shadow-xl transition-all duration-300 transform hover:scale-105 hover:-translate-y-0.5 border border-blue-400/30"
                  >
                    🔍 Click to Inspect
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Load More Hint */}
      {sessions.length >= 50 && (
        <div className="text-center mt-8">
          <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4">
            <p className="text-gray-400 text-sm">
              Showing recent sessions • More data available in API
            </p>
          </div>
        </div>
      )}
    </div>
  );
};

export default SessionList;