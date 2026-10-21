import React from 'react';
import {
  LayoutDashboard,
  Search,
  ShieldAlert,
  Cpu,
  Shield,
  X
} from 'lucide-react';

const navItems = [
  { id: 'overview',       label: 'Overview',              icon: LayoutDashboard, desc: 'Dataset & Key Metrics' },
  { id: 'analysis',       label: 'Transaction Analysis',  icon: Search,          desc: 'Search & Results Ledger' },
  { id: 'alerts',         label: 'Fraud Alerts',          icon: ShieldAlert,     desc: 'Flagged High-Risk Cases' },
];

export default function Sidebar({
  activeNav,
  onNavigate,
  collapsed,
  onToggleCollapse,
  mobileOpen,
  onCloseMobile,
  fraudAlertCount = 0,
  backendConnected = false,
  modelInfo = {}
}) {
  const modelName = modelInfo?.model || 'FedProx DNN';
  const numFeatures = modelInfo?.num_features || 421;
  const threshold = modelInfo?.threshold !== undefined ? Number(modelInfo.threshold).toFixed(2) : '0.85';

  const sidebarContent = (
    <div className="flex flex-col h-full bg-slate-900 text-slate-100 select-none">
      {/* Brand Header */}
      <div className="flex items-center justify-between px-4 py-5 border-b border-slate-800">
        <div className="flex items-center gap-3 overflow-hidden">
          <div className="flex items-center justify-center w-9 h-9 rounded-xl bg-blue-600 text-white shadow-md shadow-blue-600/30 shrink-0">
            <Shield size={20} className="stroke-[2.5]" />
          </div>
          {!collapsed && (
            <div className="min-w-0">
              <div className="flex items-center gap-1.5">
                <span className="text-base font-extrabold tracking-tight text-white truncate">FraudGuard AI</span>
                <span className="text-[10px] bg-blue-500/20 text-blue-400 font-bold px-1.5 py-0.5 rounded border border-blue-500/30">FL</span>
              </div>
              <p className="text-[11px] text-slate-400 font-medium truncate">Federated Fraud Analytics</p>
            </div>
          )}
        </div>

        {/* Mobile close button */}
        {mobileOpen && (
          <button
            onClick={onCloseMobile}
            className="md:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800"
          >
            <X size={18} />
          </button>
        )}
      </div>

      {/* Navigation Links */}
      <nav className="flex-1 px-3 py-5 space-y-1.5 overflow-y-auto">
        {!collapsed && (
          <p className="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-3 mb-2">
            Navigation
          </p>
        )}

        {navItems.map(({ id, label, icon: Icon, desc }) => {
          const isActive = activeNav === id;
          const isAlertTab = id === 'alerts';

          return (
            <button
              key={id}
              onClick={() => {
                onNavigate(id);
                if (mobileOpen) onCloseMobile();
              }}
              title={collapsed ? label : undefined}
              className={`
                w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-xs font-semibold
                transition-all duration-150 text-left group relative
                ${isActive
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-600/25'
                  : 'text-slate-300 hover:bg-slate-800/80 hover:text-white'
                }
              `}
            >
              <Icon size={18} className={`shrink-0 ${isActive ? 'text-white' : 'text-slate-400 group-hover:text-blue-400'}`} />

              {!collapsed && (
                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between">
                    <span className="truncate">{label}</span>
                    {isAlertTab && fraudAlertCount > 0 && (
                      <span className="ml-2 px-1.5 py-0.5 text-[10px] font-black rounded-full bg-rose-500 text-white shadow-xs">
                        {fraudAlertCount}
                      </span>
                    )}
                  </div>
                  <p className={`text-[10px] truncate ${isActive ? 'text-blue-100' : 'text-slate-500'}`}>
                    {desc}
                  </p>
                </div>
              )}

              {/* Collapsed dot badge for alerts */}
              {collapsed && isAlertTab && fraudAlertCount > 0 && (
                <span className="absolute top-2 right-2 w-2 h-2 rounded-full bg-rose-500" />
              )}
            </button>
          );
        })}
      </nav>

      {/* Model & System Status Widget */}
      <div className="border-t border-slate-800 p-3 bg-slate-950/60">
        {!collapsed ? (
          <div className="bg-slate-900/90 border border-slate-800 rounded-xl p-3 space-y-2">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-1.5">
                <Cpu size={14} className="text-blue-400" />
                <span className="text-[11px] font-bold text-slate-200">{modelName}</span>
              </div>
              <span className={`inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full ${
                backendConnected
                  ? 'bg-emerald-500/15 text-emerald-400 border border-emerald-500/30'
                  : 'bg-rose-500/15 text-rose-400 border border-rose-500/30'
              }`}>
                <span className={`w-1.5 h-1.5 rounded-full ${backendConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`} />
                {backendConnected ? 'Active' : 'Offline'}
              </span>
            </div>

            <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-400 pt-1 border-t border-slate-800">
              <div>
                <span className="block text-slate-500">Features</span>
                <strong className="text-slate-200 font-mono">{numFeatures}</strong>
              </div>
              <div>
                <span className="block text-slate-500">Cutoff Threshold</span>
                <strong className="text-amber-400 font-mono">≥ {threshold}</strong>
              </div>
            </div>
          </div>
        ) : (
          <div className="flex justify-center py-2" title={`${modelName} - Threshold ${threshold}`}>
            <div className="w-8 h-8 rounded-lg bg-slate-800 flex items-center justify-center text-blue-400">
              <Cpu size={16} />
            </div>
          </div>
        )}

        {!collapsed && (
          <p className="text-[10px] text-slate-500 text-center mt-2">
            IEEE-CIS Benchmark &bull; CS Project
          </p>
        )}
      </div>
    </div>
  );

  return (
    <>
      {/* Desktop Sidebar */}
      <aside
        className={`
          hidden md:flex flex-col h-screen sticky top-0 shrink-0 border-r border-slate-800
          transition-all duration-300 ease-in-out z-30
          ${collapsed ? 'w-16' : 'w-64'}
        `}
      >
        {sidebarContent}
      </aside>

      {/* Mobile Backdrop & Drawer */}
      {mobileOpen && (
        <div className="fixed inset-0 z-50 md:hidden flex">
          <div
            className="fixed inset-0 bg-slate-950/60 backdrop-blur-xs transition-opacity"
            onClick={onCloseMobile}
          />
          <div className="relative flex-1 flex flex-col max-w-xs w-full bg-slate-900 shadow-2xl">
            {sidebarContent}
          </div>
        </div>
      )}
    </>
  );
}
