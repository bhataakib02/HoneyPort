import React from 'react';

const StatsCards = ({ stats, loading, className = "", professionalMode = false }) => {
  const formatNumber = (num) => {
    return new Intl.NumberFormat().format(num);
  };

  const formatScore = (score) => {
    return score.toFixed(3);
  };

  const getThreatColor = (level) => {
    return {
      LOW: 'from-green-500 to-green-600',
      MEDIUM: 'from-yellow-500 to-yellow-600',
      HIGH: 'from-orange-500 to-orange-600',
      CRITICAL: 'from-red-500 to-red-600'
    }[level] || 'from-gray-500 to-gray-600';
  };

  if (loading) {
    return (
      <div className={`animate-pulse ${className}`}>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
          {[...Array(4)].map((_, i) => (
            <div key={i} className="stat-card">
              <div className="text-gray-400 text-sm mb-2">Loading...</div>
              <div className="bg-gray-600 h-8 rounded mb-2"></div>
              <div className="bg-gray-600 h-4 w-20 rounded"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className={`${className}`}>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-3">
        {/* Total Sessions */}
        <div className="stat-card group hover:bg-gradient-to-br hover:from-blue-500/10 hover:to-purple-600/20 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-blue-500/20">
          <div className="flex items-center justify-between mb-3">
            <div className="text-gray-300 text-sm font-medium flex items-center">
              <span className="w-2 h-2 bg-blue-400 rounded-full mr-2 shadow-lg shadow-blue-400/50"></span>
              Total Sessions
            </div>
            <div className="text-3xl group-hover:animate-pulse group-hover:text-blue-400">🎯</div>
          </div>
          <div className="text-3xl font-bold bg-gradient-to-r from-blue-400 via-purple-400 to-blue-400 bg-clip-text text-transparent mb-2 animate-pulse">
            {formatNumber(stats.total_sessions || 0)}
          </div>
          <div className="text-xs text-gray-400 mb-3">
            Attacks captured since startup
          </div>
          <div className="relative w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-blue-500 via-purple-500 to-pink-500 opacity-30"></div>
            <div className="bg-gradient-to-r from-blue-500 to-purple-500 h-2 rounded-full transition-all duration-700 shadow-lg shadow-blue-500/30" style={{width: `${Math.min((stats.total_sessions || 0) * 10, 100)}%`}}></div>
          </div>
        </div>

        {/* High Threats */}
        <div className="stat-card group hover:bg-gradient-to-br hover:from-red-500/10 hover:to-orange-600/20 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-red-500/20">
          <div className="flex items-center justify-between mb-3">
            <div className="text-gray-300 text-sm font-medium flex items-center">
              <span className="w-2 h-2 bg-red-400 rounded-full mr-2 shadow-lg shadow-red-400/50"></span>
              High Threats
            </div>
            <div className="text-3xl group-hover:animate-bounce group-hover:text-red-400">🚨</div>
          </div>
          <div className="text-3xl font-bold bg-gradient-to-r from-red-400 via-orange-400 to-pink-400 bg-clip-text text-transparent mb-2 animate-pulse">
            {formatNumber(stats.total_threats || 0)}
          </div>
          <div className="text-xs text-gray-400 mb-3">
            Require immediate attention
          </div>
          <div className="flex space-x-1">
            {Object.entries(stats.threat_levels || {}).map(([level, count], index) => (
              <div key={level} className={`flex-1 h-3 rounded-full bg-gradient-to-r ${getThreatColor(level)} shadow-lg transition-all duration-300 hover:scale-110`} title={`${level}: ${count}`}></div>
            ))}
          </div>
        </div>

        {/* Average Threat Score */}
        <div className="stat-card group hover:bg-gradient-to-br hover:from-purple-500/10 hover:to-blue-600/20 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-purple-500/20">
          <div className="flex items-center justify-between mb-3">
            <div className="text-gray-300 text-sm font-medium flex items-center">
              <span className="w-2 h-2 bg-purple-400 rounded-full mr-2 shadow-lg shadow-purple-400/50"></span>
              Average Score
            </div>
            <div className="text-3xl group-hover:animate-spin group-hover:text-purple-400">🧠</div>
          </div>
          <div className="text-3xl font-bold bg-gradient-to-r from-purple-400 via-blue-400 to-indigo-400 bg-clip-text text-transparent mb-2">
            {formatScore(stats.avg_score || 0)}
          </div>
          <div className="text-xs text-gray-400 mb-3">
            AI anomaly detection score
          </div>
          <div className="relative w-full bg-gray-700/50 rounded-full h-2 overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-r from-purple-500 via-blue-500 to-indigo-500 opacity-30"></div>
            <div className="bg-gradient-to-r from-purple-500 to-blue-500 h-2 rounded-full transition-all duration-700 shadow-lg shadow-purple-500/30" style={{width: `${(stats.avg_score || 0) * 100}%`}}></div>
          </div>
        </div>

        {/* System Status */}
        <div className="stat-card group hover:bg-gradient-to-br hover:from-green-500/10 hover:to-emerald-600/20 transition-all duration-500 hover:scale-105 hover:shadow-2xl hover:shadow-green-500/20">
          <div className="flex items-center justify-between mb-3">
            <div className="text-gray-300 text-sm font-medium flex items-center">
              <span className="w-2 h-2 bg-green-400 rounded-full mr-2 shadow-lg shadow-green-400/50 animate-pulse"></span>
              System Status
            </div>
            <div className="text-3xl group-hover:animate-pulse group-hover:text-green-400">🟢</div>
          </div>
          <div className="text-2xl font-bold bg-gradient-to-r from-green-400 via-emerald-400 to-teal-400 bg-clip-text text-transparent mb-2">
            Online
          </div>
          <div className="text-xs text-gray-400 mb-3">
            All services running
          </div>
          <div className="flex items-center space-x-2">
            <div className="w-2 h-2 bg-green-400 rounded-full shadow-lg shadow-green-400/50"></div>
            <div className="text-xs text-green-400 font-medium">All systems operational</div>
          </div>
        </div>

      </div>

      {/* Threat Level Breakdown */}
      {stats.threat_levels && (
        <div className="mt-6">
          <h3 className="text-lg font-bold mb-3 text-white flex items-center">
            <span className="text-purple-400 mr-2">🎯</span>
            Threat Level Distribution
          </h3>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
            {Object.entries(stats.threat_levels).map(([level, count]) => (
              <div key={level} className="text-center">
                <div 
                  className={`inline-flex items-center justify-center w-10 h-10 rounded-full text-white font-bold text-sm bg-gradient-to-br ${getThreatColor(level)} mb-1 shadow-lg`}
                >
                  {count}
                </div>
                <div className={`text-xs font-medium capitalize ${level === 'LOW' ? 'text-green-400' : level === 'MEDIUM' ? 'text-yellow-400' : level === 'HIGH' ? 'text-orange-400' : 'text-red-400'}`}>
                  {level}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

    </div>
  );
};

export default StatsCards;