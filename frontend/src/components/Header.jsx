import React from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  RefreshCw,
  Menu,
  FileSpreadsheet,
  Cpu,
  Layers,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';

const NAV_TITLES = {
  'overview': {
    title: 'Fraud Detection Overview',
    subtitle: 'AI-powered online payment transaction risk analysis'
  },
  'analysis': {
    title: 'Transaction Analysis Ledger',
    subtitle: 'Search, filter, and inspect individual transaction features and risk predictions'
  },
  'alerts': {
    title: 'Fraud Alerts & Risk Flagged',
    subtitle: 'High-risk transactions flagged by the FedProx DNN decision cutoff'
  }
};

export default function Header({
  activeNav = 'overview',
  backendConnected = false,
  checkingBackend = false,
  onRefreshHealth,
  sidebarCollapsed = false,
  onToggleSidebar,
  onOpenMobileMenu,
  activeFileName = null,
  totalTransactions = null,
  modelInfo = {}
}) {
  const currentNav = NAV_TITLES[activeNav] || NAV_TITLES['overview'];
  const modelName = modelInfo?.model || 'FedProx DNN';
  const threshold = modelInfo?.threshold !== undefined ? Number(modelInfo.threshold).toFixed(2) : '0.85';

  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-20 shadow-xs">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-3.5 flex items-center justify-between gap-4">
        
        {/* Left: Hamburger (mobile) / Collapse (desktop) + Page Title */}
        <div className="flex items-center gap-3 min-w-0">
          {/* Mobile menu button */}
          <button
            onClick={onOpenMobileMenu}
            className="md:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition-colors"
            title="Open menu"
          >
            <Menu size={20} />
          </button>

          {/* Desktop collapse toggle */}
          <button
            onClick={onToggleSidebar}
            className="hidden md:flex p-1.5 rounded-lg text-slate-400 hover:text-slate-700 hover:bg-slate-100 transition-colors"
            title={sidebarCollapsed ? "Expand sidebar" : "Collapse sidebar"}
          >
            {sidebarCollapsed ? <ChevronRight size={18} /> : <ChevronLeft size={18} />}
          </button>

          <div className="min-w-0">
            <h1 className="text-lg sm:text-xl font-extrabold text-slate-900 tracking-tight truncate">
              {currentNav.title}
            </h1>
            <p className="text-xs text-slate-500 font-medium truncate hidden sm:block">
              {currentNav.subtitle}
            </p>
          </div>
        </div>

        {/* Right: Active Dataset badge (if any) + Health & Model Status */}
        <div className="flex items-center gap-2 sm:gap-3 shrink-0">
          
          {/* Active File Pill */}
          {activeFileName && (
            <div className="hidden lg:flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold bg-blue-50 text-blue-700 border border-blue-200">
              <FileSpreadsheet size={13} className="text-blue-600" />
              <span className="max-w-[140px] truncate">{activeFileName}</span>
              {totalTransactions && (
                <span className="text-[11px] font-mono opacity-80">({totalTransactions})</span>
              )}
            </div>
          )}

          {/* Health Refresh Button */}
          <button
            onClick={onRefreshHealth}
            disabled={checkingBackend}
            className="text-slate-500 hover:text-slate-800 transition-colors p-2 rounded-lg hover:bg-slate-100 active:bg-slate-200"
            title="Refresh backend status"
          >
            <RefreshCw size={15} className={checkingBackend ? "animate-spin text-blue-600" : ""} />
          </button>

          {/* Model & Backend Status Badge */}
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-bold border transition-colors ${
            backendConnected
              ? 'bg-emerald-50 text-emerald-800 border-emerald-300'
              : 'bg-rose-50 text-rose-800 border-rose-300'
          }`}>
            <span className={`w-2 h-2 rounded-full ${
              backendConnected ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'
            }`} />
            
            {backendConnected ? (
              <span className="flex items-center gap-1.5">
                <ShieldCheck size={14} className="text-emerald-600" />
                <span>Backend Connected</span>
                <span className="hidden sm:inline-block text-[11px] font-normal text-emerald-700">
                  &bull; {modelName}
                </span>
              </span>
            ) : (
              <span className="flex items-center gap-1.5">
                <ShieldAlert size={14} className="text-rose-600" />
                <span>Backend Offline</span>
              </span>
            )}
          </div>

        </div>

      </div>
    </header>
  );
}
