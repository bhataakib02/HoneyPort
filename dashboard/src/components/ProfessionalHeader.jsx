import React from 'react';

const ProfessionalHeader = ({ 
  lastUpdate, 
  autoRefresh, 
  setAutoRefresh, 
  onRefresh, 
  onScan, 
  loading, 
  activeTab, 
  setActiveTab,
  currentPage,
  setCurrentPage
}) => {
  const formatTime = (date) => {
    return date.toLocaleTimeString('en-US', { 
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <header className="bg-gradient-to-r from-slate-950/90 via-slate-800/80 to-blue-950/90 backdrop-blur-xl border-b border-white/5 sticky top-0 z-50 shadow-2xl shadow-black/20">
      <div className="container mx-auto px-6 py-3">
        <div className="flex items-center justify-between">
          {/* Professional Branding */}
          <div className="flex items-center space-x-4">
            <div className="flex items-center space-x-3">
              <div className="relative group">
                <div className="w-10 h-10 bg-gradient-to-br from-blue-500 via-purple-500 to-pink-500 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/25">
                  <span className="text-white text-lg font-bold">🛡️</span>
                </div>
                <div className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full border border-slate-950 animate-pulse"></div>
              </div>
              <div>
                <h1 className="text-2xl font-black text-transparent bg-clip-text bg-gradient-to-r from-white via-blue-200 to-purple-200 tracking-tight">
                  AetherionBot
              </h1>
                <div className="flex items-center space-x-3 text-xs">
                  <span className="text-blue-300 font-medium">• CYBER DECEPTION ENGINE</span>
                  <span className="text-gray-500">|</span>
                  <span className="text-emerald-300 font-medium">• LIVE MONITORING</span>
                </div>
              </div>
            </div>
          </div>
          
          {/* Desktop Navigation */}
          <div className="hidden lg:flex space-x-1 bg-gray-800 bg-opacity-30 rounded-lg p-1 backdrop-blur-sm">
            <button
              onClick={() => setCurrentPage('dashboard')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                currentPage === 'dashboard' 
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                  : 'text-gray-400 hover:text-white hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <span>📊</span>
              <span>Dashboard</span>
            </button>
            
            <button
              onClick={() => setCurrentPage('analytics')}
              className={`flex items-center space-x-2 px-4 py-2 rounded-md text-sm font-medium transition-all duration-200 ${
                currentPage === 'analytics'
                  ? 'bg-gradient-to-r from-blue-600 to-purple-600 text-white shadow-lg' 
                  : 'text-gray-400 hover:text-white hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <span>📈</span>
              <span>Advanced Analytics</span>
            </button>
          </div>

          {/* Professional Status & Controls */}
          <div className="flex items-center space-x-4">
            {/* System Status */}
            <div className="text-right">
              <div className="flex items-center space-x-2">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span className="text-sm font-semibold text-green-400">System Operational</span>
              </div>
              <p className="text-xs text-gray-400">
                Last sync: {formatTime(lastUpdate)} | {autoRefresh ? 'Auto-refresh ON' : 'Manual mode'}
              </p>
            </div>
            
            {/* Professional Action Buttons */}
            <div className="flex space-x-2">
              {/* Professional Scan Button */}
              <button
                onClick={onScan}
                disabled={loading}
                className="px-3 py-1.5 bg-gray-700 border border-gray-600 text-gray-300 hover:bg-gray-600 rounded-lg text-xs font-medium transition-all duration-200 flex items-center space-x-1"
                title="Execute Professional Threat Scan"
              >
                <span className="text-sm">🎯</span>
                <span>PROFESSIONAL SCAN</span>
              </button>
              
              {/* Refresh Control */}
              <button
                onClick={onRefresh}
                disabled={loading}
                className="px-3 py-1.5 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-lg text-xs font-medium transition-all duration-200 flex items-center space-x-1"
              >
                <span className={loading ? 'animate-spin' : ''}>🔄</span>
                <span>REFRESH DATA</span>
              </button>
              
            </div>
          </div>
        </div>

        {/* Mobile Top Navigation */}
        <div className="lg:hidden mt-2 pb-1">
          <nav className="flex space-x-1 bg-gray-800 bg-opacity-30 rounded-lg p-1 backdrop-blur-sm overflow-x-auto">
            <button
              onClick={() => setCurrentPage('dashboard')}
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-xs font-medium transition-all duration-200 whitespace-nowrap ${
                currentPage === 'dashboard' 
                  ? 'bg-gradient-to-r from-purple-600 to-blue-800 text-white shadow-md' 
                  : 'text-gray-400 hover:text-white hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <span className="text-xs">📊</span>
              <span>Dashboard</span>
            </button>
            
            <button
              onClick={() => setCurrentPage('analytics')}
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-xs font-medium transition-all duration-200 whitespace-nowrap ${
                currentPage === 'analytics'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-800 text-white shadow-md' 
                  : 'text-gray-400 hover:text-white hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <span className="text-xs">📈</span>
              <span>Analytics</span>
            </button>
            
            <button
              onClick={() => setActiveTab('intelligence')}
              className={`flex items-center space-x-2 px-3 py-2 rounded-md text-xs font-medium transition-all duration-200 whitespace-nowrap ${
                activeTab === 'intelligence'
                  ? 'bg-gradient-to-r from-purple-600 to-blue-800 text-white shadow-md' 
                  : 'text-gray-400 hover:text-white hover:bg-white hover:bg-opacity-10'
              }`}
            >
              <span className="text-xs">🧠</span>
              <span>Intelligence</span>
            </button>
            
            <button
              onClick={() => window.open('http://localhost:8001/docs', '_blank')}
              className="flex items-center space-x-2 px-3 py-2 rounded-md text-xs font-medium transition-all duration-200 text-gray-400 hover:text-white hover:bg-white hover:bg-opacity-10 whitespace-nowrap"
            >
              <span className="text-xs">📍</span>
              <span>API Docs</span>
            </button>
          </nav>
        </div>


      </div>
    </header>
  );
};

export default ProfessionalHeader;
