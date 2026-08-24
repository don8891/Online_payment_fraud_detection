import React from 'react';
import {
  LayoutDashboard, Search, TrendingUp, ShieldAlert,
  BarChart3, Brain, ListOrdered, Settings, Shield,
  Cpu, CheckCircle2
} from 'lucide-react';

const navItems = [
  { id: 'dashboard',           label: 'Dashboard',            icon: LayoutDashboard },
  { id: 'transaction-analysis',label: 'Transaction Analysis', icon: Search },
  { id: 'fraud-detection',     label: 'Fraud Detection',      icon: ShieldAlert },
  { id: 'model-performance',   label: 'Model Performance',    icon: TrendingUp },
  { id: 'explainable-ai',      label: 'Explainable AI',       icon: Brain },
  { id: 'transactions',        label: 'Transactions',         icon: ListOrdered },
  { id: 'settings',            label: 'Settings',             icon: Settings },
];

export default function Sidebar({ activePage, onNavigate, collapsed }) {
  return (
    <aside
      className={`
        flex flex-col bg-slate-900 text-slate-100 h-screen sticky top-0
        transition-all duration-300 ease-in-out shrink-0
        ${collapsed ? 'w-16' : 'w-60'}
      `}
    >
      {/* Logo */}
      <div className="flex items-center gap-2.5 px-4 py-5 border-b border-slate-700">
        <div className="flex items-center justify-center w-8 h-8 rounded-lg bg-blue-600 shrink-0">
          <Shield size={17} className="text-white" />
        </div>
        {!collapsed && (
          <div className="overflow-hidden">
            <p className="text-sm font-bold text-white leading-tight whitespace-nowrap">FraudShield AI</p>
            <p className="text-xs text-slate-400 whitespace-nowrap">Fraud Detection System</p>
          </div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 px-2 py-4 space-y-0.5 overflow-y-auto">
        {!collapsed && (
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-widest px-3 pb-2">Navigation</p>
        )}
        {navItems.map(({ id, label, icon: Icon }) => {
          const active = activePage === id;
          return (
            <button
              key={id}
              onClick={() => onNavigate(id)}
              title={collapsed ? label : undefined}
              className={`
                w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium
                transition-colors duration-150 text-left
                ${active
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }
              `}
            >
              <Icon size={17} className="shrink-0" />
              {!collapsed && <span className="truncate">{label}</span>}
            </button>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="border-t border-slate-700 px-3 py-4 space-y-2">
        <div className={`flex items-center gap-2.5 ${collapsed ? 'justify-center' : ''}`}>
          <div className="flex items-center justify-center w-7 h-7 rounded-md bg-slate-700 shrink-0">
            <Cpu size={13} className="text-blue-400" />
          </div>
          {!collapsed && (
            <div>
              <p className="text-xs font-semibold text-slate-300">ML Model: LightGBM</p>
              <div className="flex items-center gap-1 mt-0.5">
                <CheckCircle2 size={10} className="text-emerald-400" />
                <p className="text-xs text-emerald-400 font-medium">Status: Active</p>
              </div>
            </div>
          )}
        </div>
        {!collapsed && (
          <p className="text-xs text-slate-500 px-0.5">© 2026 FraudShield AI Prototype</p>
        )}
      </div>
    </aside>
  );
}
