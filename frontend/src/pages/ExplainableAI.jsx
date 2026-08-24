import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell
} from 'recharts';
import { Brain, Info, AlertTriangle, TrendingUp } from 'lucide-react';
import { SHAP_FEATURE_IMPORTANCE } from '../data/mockData';
import RiskBadge from '../components/RiskBadge';

const CONTRIBUTING_FACTORS = [
  { factor: 'High transaction amount', direction: 'increase', weight: 'Strong' },
  { factor: 'Unusual payer email domain (protonmail.com)', direction: 'increase', weight: 'Strong' },
  { factor: 'Suspicious device characteristics', direction: 'increase', weight: 'Moderate' },
  { factor: 'Unfamiliar card issuer code (card1)', direction: 'increase', weight: 'Moderate' },
  { factor: 'Product type C (higher-risk category)', direction: 'increase', weight: 'Mild' },
  { factor: 'Consistent payer device history', direction: 'decrease', weight: 'Mild' },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    const f = SHAP_FEATURE_IMPORTANCE.find(x => x.feature === label);
    return (
      <div className="bg-white border border-slate-200 rounded-lg px-3 py-2 shadow-lg text-xs max-w-[200px]">
        <p className="font-bold text-slate-800">{label}</p>
        {f && <p className="text-slate-500 mt-0.5">{f.description}</p>}
        <p className="text-blue-600 font-mono mt-1">Importance: {payload[0].value.toFixed(3)}</p>
      </div>
    );
  }
  return null;
};

export default function ExplainableAI() {
  const sorted = [...SHAP_FEATURE_IMPORTANCE].sort((a, b) => b.importance - a.importance);

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Explainable AI</h2>
        <p className="text-sm text-slate-500 mt-0.5">Understand why the ML model classifies a transaction as risky</p>
        <div className="inline-flex items-center gap-1.5 mt-2 bg-amber-50 border border-amber-200 text-amber-700 text-xs font-medium px-2.5 py-1 rounded-full">
          <Info size={11} />
          Demonstration — SHAP integration with the trained LightGBM model is planned for Phase 2
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-3 gap-6">
        {/* Global Feature Importance */}
        <div className="xl:col-span-2 bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <div className="flex items-center gap-2 mb-1">
            <Brain size={16} className="text-violet-600" />
            <h3 className="text-sm font-bold text-slate-800">Global Feature Importance</h3>
          </div>
          <p className="text-xs text-slate-500 mb-5">Top features influencing the LightGBM fraud detection model — demonstration values</p>

          <ResponsiveContainer width="100%" height={280}>
            <BarChart data={sorted} layout="vertical" barSize={16} margin={{ left: 10 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" horizontal={false} />
              <XAxis type="number" domain={[0, 0.35]} tick={{ fontSize: 10, fill: '#94a3b8' }} />
              <YAxis type="category" dataKey="feature" tick={{ fontSize: 11, fill: '#475569', fontWeight: 600 }} width={100} />
              <Tooltip content={<CustomTooltip />} />
              <Bar dataKey="importance" radius={[0, 4, 4, 0]}>
                {sorted.map((entry, i) => (
                  <Cell
                    key={i}
                    fill={i === 0 ? '#ef4444' : i === 1 ? '#f97316' : i <= 3 ? '#f59e0b' : i <= 6 ? '#3b82f6' : '#6366f1'}
                  />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>

          <div className="flex items-center gap-3 mt-4 flex-wrap">
            {[
              { label: 'Highest Impact', color: 'bg-red-500' },
              { label: 'High Impact',    color: 'bg-orange-500' },
              { label: 'Medium Impact',  color: 'bg-amber-500' },
              { label: 'Lower Impact',   color: 'bg-blue-500' },
            ].map(({ label, color }) => (
              <div key={label} className="flex items-center gap-1.5 text-xs text-slate-600">
                <div className={`w-2.5 h-2.5 rounded-sm ${color}`} />
                {label}
              </div>
            ))}
          </div>
        </div>

        {/* Transaction Explanation Panel */}
        <div className="space-y-4">
          <div className="bg-white border border-red-200 rounded-xl p-5 shadow-sm">
            <div className="flex items-center gap-2 mb-3">
              <AlertTriangle size={15} className="text-red-500" />
              <h3 className="text-sm font-bold text-slate-800">Transaction Explanation</h3>
            </div>
            <div className="bg-slate-50 rounded-lg p-3 space-y-2 mb-4">
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-500">Transaction ID</span>
                <span className="text-xs font-mono font-bold text-slate-800">TXN-10002</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-500">Amount</span>
                <span className="text-xs font-bold text-slate-900">$845.20</span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-500">Prediction</span>
                <RiskBadge type="Fraud" />
              </div>
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-500">Risk Score</span>
                <span className="text-xs font-mono font-bold text-red-600">0.87</span>
              </div>
            </div>

            <div>
              <p className="text-xs font-bold text-slate-700 mb-2.5">Contributing Factors</p>
              <div className="space-y-2">
                {CONTRIBUTING_FACTORS.map((cf, i) => (
                  <div key={i} className="flex items-start gap-2.5 text-xs">
                    <div className={`mt-0.5 w-4 h-4 rounded-full flex items-center justify-center shrink-0 ${
                      cf.direction === 'increase' ? 'bg-red-100' : 'bg-emerald-100'
                    }`}>
                      <TrendingUp size={9} className={cf.direction === 'increase' ? 'text-red-600' : 'text-emerald-600 rotate-180'} />
                    </div>
                    <div className="flex-1">
                      <p className={`font-medium leading-tight ${
                        cf.direction === 'increase' ? 'text-red-700' : 'text-emerald-700'
                      }`}>{cf.factor}</p>
                      <p className="text-slate-400 text-xs">{cf.weight} influence</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4">
            <div className="flex items-start gap-2">
              <Info size={14} className="text-amber-600 mt-0.5 shrink-0" />
              <div className="text-xs text-amber-700">
                <p className="font-bold mb-1">Demonstration Explanation</p>
                <p>These factors are illustrative examples. Actual SHAP values will be computed from the trained LightGBM model via the Flask API in Phase 2.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
