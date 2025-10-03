import React from 'react';

const SessionViewer = ({ session, onClose }) => {
  const analyzePatterns = (command) => {
    const patterns = [];
    
    // Command analysis
    if (command.includes('rm -rf')) patterns.push({ category: '🗑️ Deletion', severity: 'CRITICAL', description: 'File/directory deletion command' });
    if (command.includes('cat /etc/passwd')) patterns.push({ category: '🔍 Reconnaissance', severity: 'HIGH', description: 'Attempting to read system password file' });
    if (command.includes('sudo')) patterns.push({ category: '🔐 Privilege Escalation', severity: 'MEDIUM', description: 'Attempting privilege escalation' });
    if (command.includes('wget') || command.includes('curl')) patterns.push({ category: '📥 Download', severity: 'HIGH', description: 'Attempting to download files' });
    if (command.includes('bash -c') || command.includes('sh -c')) patterns.push({ category: '⚡ Command Execution', severity: 'CRITICAL', description: 'Dangerous command execution pattern' });
    if (command.includes('chmod +x')) patterns.push({ category: '🔧 Permissions', severity: 'MEDIUM', description: 'Changing file permissions to executables' });
    if (command.includes('python -c') || command.includes('python3 -c')) patterns.push({ category: '🐍 Code Execution', severity: 'HIGH', description: 'Attempting to execute Python code' });
    if (command.includes('nc ') || command.includes('netcat')) patterns.push({ category: '🔗 Networking', severity: 'HIGH' , description: 'Network connection attempt' });
    if (command.includes('systemctl')) patterns.push({ category: '⚙️ System Control', severity: 'MEDIUM', description: 'System service access attempt' });
    
    return patterns.length > 0 ? patterns : [{ category: '❓ General', severity: 'UNKNOWN', description: 'Standard command execution' }];
  };

  const getLocationInfo = (ip) => {
    // Mock location for demo (in real app, use IP geolocation API)
    const mockLocations = {
      '10.0.0.100': { country: 'Internal Network', city: 'LAN', isp: 'Local' },
      '192.168.1.200': { country: 'Internal Network', city: 'LAN', isp: 'Local' },
      '203.0.113.15': { country: 'Unknown', city: 'Unknown', isp: 'Public Network' }
    };
    
    return mockLocations[ip] || { country: 'Unknown', city: 'Unknown', isp: 'Unknown' };
  };

  const formatTimestamp = (timestamp) => {
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return 'Unknown';
    }
  };

  const getThreatScore = (level) => {
    const scores = {
      'CRITICAL': 95,
      'HIGH': 80,
      'MEDIUM': 60,
      'LOW': 20
    };
    return scores[level] || 0;
  };

  const getThreatColor = (level) => {
    const colors = {
      'CRITICAL': 'text-red-400 bg-red-900 bg-opacity-20 border-red-500',
      'HIGH': 'text-orange-400 bg-orange-900 bg-opacity-20 border-orange-500',
      'MEDIUM': 'text-yellow-400 bg-yellow-900 bg-opacity-20 border-yellow-500',
      'LOW': 'text-green-400 bg-green-900 bg-opacity-20 border-green-500'
    };
    return colors[level] || 'text-gray-400 bg-gray-900 bg-opacity-20 border-gray-500';
  };

  if (!session) return null;

  const patterns = analyzePatterns(session.command);
  const location = getLocationInfo(session.ip);

  return (
    <div className="dashboard-container">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-xl font-semibold">🕵️ Session Inspector</h3>
        <button
          onClick={onClose}
          className="px-3 py-1 bg-gray-600 hover:bg-gray-700 rounded-lg transition-colors text-sm"
        >
          ✕ Close
        </button>
      </div>

      {/* Threat Overview */}
      <div className={`p-4 rounded-lg border ${getThreatColor(session.threat_level)} mb-6`}>
        <div className="flex items-center justify-between">
          <div>
            <div className="text-lg font-bold mb-1">
              {session.threat_level} THREAT DETECTED
            </div>
            <div className="text-sm opacity-75">
              Anomaly Score: {(session.anomaly_score || 0).toFixed(3)} / 1.000
            </div>
          </div>
          <div className="text-right">
            <div className="text-2xl font-bold">
              {getThreatScore(session.threat_level)}%
            </div>
            <div className="text-sm opacity-75">Risk Level</div>
          </div>
        </div>
      </div>

      {/* Session Details */}
      <div className="space-y-6">
        {/* Basic Info */}
        <div>
          <h4 className="font-semibold text-white mb-3">📋 Session Information</h4>
          <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4 space-y-3">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-gray-400 text-sm">Session ID:</span>
                <div className="command-code">{session.session_id}</div>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Timestamp:</span>
                <div className="text-white">{formatTimestamp(session.timestamp)}</div>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Source IP:</span>
                <div className="ip-badge">{session.ip}</div>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Location:</span>
                <div className="text-white">{location.city}, {location.country}</div>
              </div>
            </div>
          </div>
        </div>

        {/* Command Analysis */}
        <div>
          <h4 className="font-semibold text-white mb-3">🔍 Command Analysis</h4>
          <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4">
            <div className="mb-3">
              <span className="text-gray-400 text-sm">Executed Command:</span>
              <div className="command-code mt-1 text-base">
                {session.command || 'No command recorded'}
              </div>
            </div>
            
            <div>
              <span className="text-gray-400 text-sm">System Response:</span>
              <div className="command-code mt-1 bg-gray-900 bg-opacity-50">
                {session.response || 'No response recorded'}
              </div>
            </div>
          </div>
        </div>

        {/* Threat Patterns */}
        <div>
          <h4 className="font-semibold text-white mb-3">🎯 Detected Patterns</h4>
          <div className="space-y-2">
            {patterns.map((pattern, index) => (
              <div key={index} className="bg-gray-800 bg-opacity-30 rounded-lg p-3">
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-2">
                    <span>{pattern.category}</span>
                    <span className={`px-2 py-1 rounded-full text-xs font-semibold ${getThreatColor(pattern.severity)}`}>
                      {pattern.severity}
                    </span>
                  </div>
                </div>
                <div className="text-gray-400 text-sm mt-1">
                  {pattern.description}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Network Information */}
        <div>
          <h4 className="font-semibold text-white mb-3">🌐 Network Analysis</h4>
          <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <span className="text-gray-400 text-sm">IP Address:</span>
                <div className="text-white">{session.ip}</div>
              </div>
              <div>
                <span className="text-gray-400 text-sm">IP Type:</span>
                <div className="text-white">
                  {session.ip.startsWith('192.168') || session.ip.startsWith('10.') ? 'Private' : 'Public'}
                </div>
              </div>
              <div>
                <span className="text-gray-400 text-sm">Country:</span>
                <div className="text-white">{location.country}</div>
              </div>
              <div>
                <span className="text-gray-400 text-sm">ISP:</span>
                <div className="text-white">{location.isp}</div>
              </div>
            </div>
          </div>
        </div>

        {/* AI Analysis */}
        <div>
          <h4 className="font-semibold text-white mb-3">🧠 AI Analysis Details</h4>
          <div className="bg-gray-800 bg-opacity-30 rounded-lg p-4">
            <div className="space-y-3">
              <div className="flex justify-between">
                <span className="text-gray-400">Anomaly Score:</span>
                <span className="text-white font-mono">{(session.anomaly_score || 0).toFixed(6)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Threat Level:</span>
                <span className={`font-semibold ${session.threat_level === 'CRITICAL' ? 'text-red-400' : session.threat_level === 'HIGH' ? 'text-orange-400' : 'text-yellow-400'}`}>
                  {session.threat_level}
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Confidence:</span>
                <span className="text-white">{Math.round((session.anomaly_score || 0) * 100)}%</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Analysis Time:</span>
                <span className="text-white">&lt;1ms (Real-time)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div>
          <h4 className="font-semibold text-white mb-3">⚡ Recommended Actions</h4>
          <div className="space-y-2">
            {session.threat_level === 'CRITICAL' && (
              <div className="bg-red-900 bg-opacity-20 border border-red-500 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-red-400">🚨</span>
                  <span className="font-semibold text-red-400">Immediate Action Required</span>
                </div>
                <div className="text-sm text-red-300 space-y-1">
                  <div>• Block IP address immediately</div>
                  <div>• Investigate for system compromise</div>
                  <div>• Review system logs for related activity</div>
                  <div>• Consider incident response procedures</div>
                </div>
              </div>
            )}
            
            {session.threat_level === 'HIGH' && (
              <div className="bg-orange-900 bg-opacity-20 border border-orange-500 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-orange-400">⚠️</span>
                  <span className="font-semibold text-orange-400">High Priority Investigation</span>
                </div>
                <div className="text-sm text-orange-300 space-y-1">
                  <div>• Monitor IP for additional activity</div>
                  <div>• Check for successful exploitation</div>
                  <div>• Review related network traffic</div>
                </div>
              </div>
            )}
            
            {(session.threat_level === 'MEDIUM' || session.threat_level === 'LOW') && (
              <div className="bg-yellow-900 bg-opacity-20 border border-yellow-500 rounded-lg p-3">
                <div className="flex items-center space-x-2 mb-2">
                  <span className="text-yellow-400">⚡</span>
                  <span className="font-semibold text-yellow-400">Standard Monitoring</span>
                </div>
                <div className="text-sm text-yellow-300 space-y-1">
                  <div>• Add to watchlist for pattern analysis</div>
                  <div>• Continue normal monitoring</div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SessionViewer;