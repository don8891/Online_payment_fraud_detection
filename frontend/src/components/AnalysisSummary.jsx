import React from 'react';
import {
  CreditCard,
  AlertTriangle,
  ShieldCheck,
  Percent,
  Cpu,
  Layers,
  Target,
  Database
} from 'lucide-react';

export default function AnalysisSummary({ summary, modelInfo }) {
  const {
    total_transactions = 0,
    fraudulent_transactions = 0,
    legitimate_transactions = 0,
    fraud_rate = 0.0
  } = summary || {};

  const {
    model = "FedProx DNN",
    num_features = 421,
    threshold = 0.85
  } = modelInfo || {};

  const formattedThreshold = Number(threshold).toFixed(2);

  return (
    <div className="space-y-4">
      {/* Model Information Pill Bar */}
      <div className="bg-slate-900 text-slate-200 rounded-2xl px-5 py-3 flex flex-wrap items-center justify-between gap-3 text-xs font-semibold shadow-sm border border-slate-800">
        <div className="flex items-center gap-2 text-blue-400 font-extrabold uppercase tracking-wider text-[11px]">
          <Cpu size={16} />
          Active Model: <span className="text-white normal-case text-xs font-bold">{model}</span>
        </div>

        <div className="flex flex-wrap items-center gap-2 sm:gap-4 text-slate-300">
          <div className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1 rounded-lg border border-slate-700">
            <Layers size={13} className="text-blue-400" />
            <span className="text-slate-400">Input Features:</span>
            <strong className="text-white font-mono">{num_features}</strong>
          </div>

          <div className="flex items-center gap-1.5 bg-slate-800/80 px-3 py-1 rounded-lg border border-slate-700">
            <Target size={13} className="text-amber-400" />
            <span className="text-slate-400">Fraud Cutoff:</span>
            <strong className="text-amber-300 font-mono">≥ {formattedThreshold}</strong>
          </div>

          <div className="hidden md:flex items-center gap-1.5 bg-slate-800/80 px-3 py-1 rounded-lg border border-slate-700">
            <Database size={13} className="text-emerald-400" />
            <span className="text-slate-400">Dataset:</span>
            <span className="text-slate-200">IEEE-CIS Fraud</span>
          </div>
        </div>
      </div>

      {/* 4 Main KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* 1. Transactions Analyzed */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[11px] font-bold text-slate-500 uppercase tracking-wider">
                Transactions Analyzed
              </p>
              <h3 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-1 font-mono tracking-tight">
                {total_transactions.toLocaleString()}
              </h3>
              <p className="text-[11px] text-slate-400 mt-1">
                Evaluated batch records
              </p>
            </div>
            <div className="p-3 bg-blue-50 text-blue-600 rounded-xl border border-blue-100">
              <CreditCard size={22} />
            </div>
          </div>
        </div>

        {/* 2. Fraudulent Transactions */}
        <div className="bg-white rounded-2xl p-5 border border-rose-200 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[11px] font-bold text-rose-600 uppercase tracking-wider">
                Fraudulent Transactions
              </p>
              <h3 className="text-2xl sm:text-3xl font-extrabold text-rose-600 mt-1 font-mono tracking-tight">
                {fraudulent_transactions.toLocaleString()}
              </h3>
              <p className="text-[11px] text-rose-500/80 mt-1">
                Model prob ≥ {formattedThreshold}
              </p>
            </div>
            <div className="p-3 bg-rose-50 text-rose-600 rounded-xl border border-rose-100">
              <AlertTriangle size={22} />
            </div>
          </div>
        </div>

        {/* 3. Legitimate Transactions */}
        <div className="bg-white rounded-2xl p-5 border border-emerald-200 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[11px] font-bold text-emerald-700 uppercase tracking-wider">
                Legitimate Transactions
              </p>
              <h3 className="text-2xl sm:text-3xl font-extrabold text-emerald-700 mt-1 font-mono tracking-tight">
                {legitimate_transactions.toLocaleString()}
              </h3>
              <p className="text-[11px] text-emerald-600/80 mt-1">
                Model prob &lt; {formattedThreshold}
              </p>
            </div>
            <div className="p-3 bg-emerald-50 text-emerald-600 rounded-xl border border-emerald-100">
              <ShieldCheck size={22} />
            </div>
          </div>
        </div>

        {/* 4. Fraud Detection Rate */}
        <div className="bg-white rounded-2xl p-5 border border-amber-200 shadow-xs hover:shadow-md transition-shadow">
          <div className="flex items-start justify-between">
            <div>
              <p className="text-[11px] font-bold text-amber-700 uppercase tracking-wider">
                Fraud Detection Rate
              </p>
              <h3 className="text-2xl sm:text-3xl font-extrabold text-amber-600 mt-1 font-mono tracking-tight">
                {fraud_rate.toFixed(2)}%
              </h3>
              <p className="text-[11px] text-amber-700/80 mt-1" title="Percentage of analyzed dataset flagged as fraud under threshold, not model test accuracy">
                % of batch flagged (not accuracy)
              </p>
            </div>
            <div className="p-3 bg-amber-50 text-amber-600 rounded-xl border border-amber-100">
              <Percent size={22} />
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
