import React from 'react';

const SystemStatus = ({ stats, className = "" }) => {
  const formatTime = (timestamp) => {
    if (!timestamp) return 'N/A';
    try {
      return new Date(timestamp).toLocaleTimeString();
    } catch {
      return 'N/A';
    }
  };

  const StatusIndicator = ({ isActive, text }) => (
    <div className={`flex items-center space-x-2 group`}>
      <div className={`relative w-3 h-3 rounded-full ${isActive ? 'bg-green-500' : 'bg-red-500'}`}>
        <div className={`absolute inset-0 rounded-full bg-gradient-to-r ${isActive ? 'from-green-400 to-emerald-500' : 'from-red-400 to-red-500'} animate-pulse`}></div>
        <div className={`absolute inset-0 rounded-full ${isActive ? 'bg-green-500' : 'bg-red-500'} opacity-70`}></div>
      </div>
      <span className={`text-sm font-medium transition-colors group-hover:text-white ${isActive ? 'text-green-400' : 'text-red-400'}`}>
        {text}
      </span>
    </div>
  );

  const SecurityBadge = ({ enabled, text }) => (
    <div className={`inline-flex items-center space-x-1.5 px-2 py-1 rounded-lg font-medium text-xs transition-all duration-200 hover:scale-105 ${
      enabled 
        ? 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-300 border border-green-400/30 hover:from-green-500/30 hover:to-emerald-500/30' 
        : 'bg-gradient-to-r from-red-500/20 to-red-500/20 text-red-300 border border-red-400/30 hover:from-red-500/30 hover:to-red-500/30'
    }`}>
      <div className={`w-1.5 h-1.5 rounded-full ${enabled ? 'bg-green-400' : 'bg-red-400'}`}></div>
      <span>{enabled ? '✅' : '❌'}</span>
      <span>{text}</span>
    </div>
  );

  const MetricBadge = ({ label, value, color = "blue" }) => {
    const colorClasses = {
      blue: 'bg-gradient-to-r from-blue-500/20 to-cyan-500/20 text-blue-300 border-blue-400/30',
      purple: 'bg-gradient-to-r from-purple-500/20 to-violet-500/20 text-purple-300 border-purple-400/30',
      green: 'bg-gradient-to-r from-green-500/20 to-emerald-500/20 text-green-300 border-green-400/30'
    };

    return (
      <div className={`px-3 py-1 rounded-lg font-medium text-xs transition-all duration-200 hover:scale-105 bg-gradient-to-r ${colorClasses[color]}`}>
        <span className="text-xs opacity-70 block">{label}</span>
        <span className="font-bold">{value}</span>
      </div>
    );
  };

  return (
    <div className={`bg-gradient-to-br from-slate-900/90 via-slate-800/80 to-slate-900/90 backdrop-blur-xl rounded-xl p-3 border border-white/10 shadow-lg shadow-black/30 ${className}`}>
      {/* Enhanced Header */}
      <div className="flex items-center justify-between mb-3">
        <div className="flex items-center space-x-3">
          <div className="relative group">
            <div className="w-6 h-6 bg-gradient-to-br from-purple-500 via-pink-500 to-purple-600 rounded-lg flex items-center justify-center shadow-lg shadow-purple-500/25 transition-transform group-hover:scale-110">
              <span className="text-white text-sm font-bold">⚡</span>
            </div>
            <div className="absolute -top-1 -right-1 w-2 h-2 bg-green-500 rounded-full border border-slate-900 animate-pulse"></div>
          </div>
          <div>
            <h3 className="text-base font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-purple-200 to-pink-200">
              System Status Monitor
            </h3>
            <p className="text-xs text-gray-400">Real-time Intelligence</p>
          </div>
        </div>
      </div>

      {/* Enhanced Horizontal Layout */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Core Services */}
        <div className="space-y-2">
          <h4 className="text-xs font-bold text-gray-300 mb-2 uppercase tracking-wider flex items-center">
            <span className="w-1.5 h-1.5 bg-gradient-to-r from-blue-400 to-purple-400 rounded-full mr-2"></span>
            Core Services
          </h4>
          <div className="grid grid-cols-2 gap-x-3 gap-y-1">
            <StatusIndicator isActive={true} text="Threat Detection" />
            <StatusIndicator isActive={true} text="AI Analysis" />
            <StatusIndicator isActive={true} text="WebSocket" />
            <StatusIndicator isActive={true} text="Data Pipeline" />
            <StatusIndicator isActive={true} text="Telegram Alerts" />
            <StatusIndicator isActive={true} text="Geo Analysis" />
          </div>
        </div>

        {/* Connections */}
        <div className="space-y-2">
          <h4 className="text-xs font-bold text-gray-300 mb-2 uppercase tracking-wider flex items-center">
            <span className="w-1.5 h-1.5 bg-gradient-to-r from-cyan-400 to-blue-400 rounded-full mr-2"></span>
            Connections
          </h4>
          <div className="space-y-2">
            <MetricBadge label="WebSocket Clients" value="2 Active" color="blue" />
            <MetricBadge label="API Endpoints" value="8 Available" color="purple" />
            <div className="flex items-center justify-between">
              <span className="text-xs text-gray-400">Database Status</span>
              <StatusIndicator isActive={true} text="Connected" />
            </div>
          </div>
        </div>

        {/* Security Status */}
        <div className="space-y-2">
          <h4 className="text-xs font-bold text-gray-300 mb-2 uppercase tracking-wider flex items-center">
            <span className="w-1.5 h-1.5 bg-gradient-to-r from-emerald-400 to-green-400 rounded-full mr-2"></span>
            Security Status
          </h4>
          <div className="space-y-2">
            <SecurityBadge enabled={true} text="Rate Limiting" />
            <SecurityBadge enabled={true} text="CORS Protection" />
            <SecurityBadge enabled={true} text="Input Validation" />
            <SecurityBadge enabled={true} text="Threat Intelligence" />
          </div>
        </div>
      </div>

      {/* Enhanced Status Summary */}
      <div className="mt-4 pt-3 border-t border-gray-700">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="text-xs text-gray-400 font-medium">SYS HEALTH</span>
            <div className="flex space-x-1">
              <div className="w-1 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <div className="w-1 h-3 bg-green-400 rounded-full animate-pulse delay-100"></div>
              <div className="w-1 h-3 bg-green-300 rounded-full animate-pulse delay-200"></div>
            </div>
          </div>
          <div className="flex items-center space-x-2">
            <div className="relative">
              <div className="w-3 h-3 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full shadow-lg shadow-green-500/50"></div>
              <div className="absolute top-0 left-0 w-3 h-3 bg-green-500 rounded-full animate-ping opacity-30"></div>
            </div>
            <span className="text-green-400 font-bold text-sm">
              ALL OPERATIONAL
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SystemStatus;