import React from 'react';
import { ShieldCheck, ShieldAlert, Activity, RefreshCw } from 'lucide-react';

export default function Header({ backendConnected, checkingBackend, onRefreshHealth }) {
  return (
    <header className="bg-slate-900 text-white border-b border-slate-800 px-6 py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 shadow-md">
      {/* Title & Subtitle */}
      <div className="flex items-center gap-3">
        <div className="p-2.5 bg-blue-600/20 text-blue-400 rounded-xl border border-blue-500/30">
          <Activity size={24} />
        </div>
        <div>
          <h1 className="text-xl font-bold text-slate-100 tracking-tight">
            Online Payment Fraud Detection
          </h1>
          <p className="text-xs text-slate-400 font-medium">
            AI-powered transaction risk analysis using LightGBM
          </p>
        </div>
      </div>

      {/* Backend Status Indicator */}
      <div className="flex items-center gap-3 self-start sm:self-auto">
        <button
          onClick={onRefreshHealth}
          disabled={checkingBackend}
          className="text-slate-400 hover:text-slate-200 transition-colors p-1.5 rounded-lg hover:bg-slate-800"
          title="Refresh backend status"
        >
          <RefreshCw size={14} className={checkingBackend ? "animate-spin" : ""} />
        </button>

        <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full text-xs font-semibold border ${
          backendConnected
            ? 'bg-emerald-950/80 text-emerald-400 border-emerald-500/40'
            : 'bg-rose-950/80 text-rose-400 border-rose-500/40'
        }`}>
          <span className={`w-2 h-2 rounded-full ${
            backendConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-500'
          }`} />
          {backendConnected ? (
            <span className="flex items-center gap-1">
              <ShieldCheck size={14} /> Backend Connected
            </span>
          ) : (
            <span className="flex items-center gap-1">
              <ShieldAlert size={14} /> Backend Offline
            </span>
          )}
        </div>
      </div>
    </header>
  );
}
