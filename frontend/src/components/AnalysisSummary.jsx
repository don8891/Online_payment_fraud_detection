import React from 'react';
import { CreditCard, AlertTriangle, ShieldCheck, Percent, Cpu, Layers, Target } from 'lucide-react';

export default function AnalysisSummary({ summary, modelInfo }) {
  if (!summary) return null;

  const {
    total_transactions = 0,
    fraudulent_transactions = 0,
    legitimate_transactions = 0,
    fraud_rate = 0.0
  } = summary;

  const {
    model = "LightGBM",
    num_features = 421,
    threshold = 0.20
  } = modelInfo || {};

  return (
    <div className="space-y-4">
      {/* Model Information Pill Bar */}
      <div className="bg-slate-900 text-slate-200 rounded-xl px-5 py-3 flex flex-wrap items-center justify-between gap-3 text-xs font-semibold shadow-sm border border-slate-800">
        <div className="flex items-center gap-2 text-blue-400 font-bold uppercase tracking-wider text-[11px]">
          <Cpu size={16} />
          Active ML Inference Model
        </div>
        <div className="flex flex-wrap items-center gap-4 text-slate-300">
          <div className="flex items-center gap-1.5 bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">
            <span className="text-slate-400">Model:</span>
            <strong className="text-white">{model}</strong>
          </div>
          <div className="flex items-center gap-1.5 bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">
            <Layers size={13} className="text-blue-400" />
            <span className="text-slate-400">Features:</span>
            <strong className="text-white">{num_features}</strong>
          </div>
          <div className="flex items-center gap-1.5 bg-slate-800 px-3 py-1 rounded-lg border border-slate-700">
            <Target size={13} className="text-amber-400" />
            <span className="text-slate-400">Fraud Threshold:</span>
            <strong className="text-amber-300">{Number(threshold).toFixed(2)}</strong>
          </div>
        </div>
      </div>

      {/* 4 Main KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Transactions */}
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">Total Transactions</p>
            <h3 className="text-2xl font-black text-slate-900 mt-1">
              {total_transactions.toLocaleString()}
            </h3>
            <p className="text-[11px] text-slate-400 mt-1">Uploaded batch dataset</p>
          </div>
          <div className="p-3 bg-blue-100 text-blue-600 rounded-2xl">
            <CreditCard size={24} />
          </div>
        </div>

        {/* Fraudulent Transactions */}
        <div className="bg-white rounded-2xl p-5 border border-rose-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-bold text-rose-600 uppercase tracking-wider">Fraudulent</p>
            <h3 className="text-2xl font-black text-rose-600 mt-1">
              {fraudulent_transactions.toLocaleString()}
            </h3>
            <p className="text-[11px] text-rose-500/80 mt-1">Prob &ge; {Number(threshold).toFixed(2)}</p>
          </div>
          <div className="p-3 bg-rose-100 text-rose-600 rounded-2xl">
            <AlertTriangle size={24} />
          </div>
        </div>

        {/* Legitimate Transactions */}
        <div className="bg-white rounded-2xl p-5 border border-emerald-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-bold text-emerald-600 uppercase tracking-wider">Legitimate</p>
            <h3 className="text-2xl font-black text-emerald-600 mt-1">
              {legitimate_transactions.toLocaleString()}
            </h3>
            <p className="text-[11px] text-emerald-600/80 mt-1">Prob &lt; {Number(threshold).toFixed(2)}</p>
          </div>
          <div className="p-3 bg-emerald-100 text-emerald-600 rounded-2xl">
            <ShieldCheck size={24} />
          </div>
        </div>

        {/* Fraud Rate */}
        <div className="bg-white rounded-2xl p-5 border border-amber-200 shadow-sm flex items-center justify-between">
          <div>
            <p className="text-xs font-bold text-amber-600 uppercase tracking-wider">Fraud Rate</p>
            <h3 className="text-2xl font-black text-amber-600 mt-1">
              {fraud_rate.toFixed(2)}%
            </h3>
            <p className="text-[11px] text-amber-600/80 mt-1">Percentage of total</p>
          </div>
          <div className="p-3 bg-amber-100 text-amber-600 rounded-2xl">
            <Percent size={24} />
          </div>
        </div>
      </div>
    </div>
  );
}
