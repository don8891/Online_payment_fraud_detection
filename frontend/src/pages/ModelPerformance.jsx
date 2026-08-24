import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Legend
} from 'recharts';
import { Cpu, Database, GitBranch, CheckCircle2 } from 'lucide-react';
import { SYSTEM_METRICS, PERFORMANCE_METRICS_DATA, VAL_VS_TEST_PERFORMANCE } from '../data/mockData';

const statItems = [
  { label: 'Training Samples', value: SYSTEM_METRICS.trainingSamples.toLocaleString(), icon: Database, color: 'bg-blue-50 text-blue-700' },
  { label: 'Features', value: SYSTEM_METRICS.featuresCount, icon: GitBranch, color: 'bg-violet-50 text-violet-700' },
  { label: 'Fraud Samples', value: SYSTEM_METRICS.fraudSamples.toLocaleString(), icon: Database, color: 'bg-red-50 text-red-700' },
  { label: 'Fraud Rate (Train)', value: '3.52%', icon: Cpu, color: 'bg-amber-50 text-amber-700' },
];

const metricRows = [
  { name: 'ROC-AUC',          value: SYSTEM_METRICS.rocAuc,          color: 'bg-emerald-500', textColor: 'text-emerald-700' },
  { name: 'Average Precision', value: SYSTEM_METRICS.avgPrecision,    color: 'bg-blue-500',    textColor: 'text-blue-700' },
  { name: 'Precision',         value: 0.4826,                          color: 'bg-indigo-500',  textColor: 'text-indigo-700' },
  { name: 'Recall',            value: 0.4668,                          color: 'bg-violet-500',  textColor: 'text-violet-700' },
  { name: 'F1 Score',          value: 0.4745,                          color: 'bg-purple-500',  textColor: 'text-purple-700' },
  { name: 'Accuracy',          value: SYSTEM_METRICS.overallAccuracy,  color: 'bg-teal-500',    textColor: 'text-teal-700' },
];

const CustomTooltip = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="bg-white border border-slate-200 rounded-lg px-3 py-2 shadow-lg text-xs">
        <p className="font-semibold text-slate-700 mb-1">{label}</p>
        {payload.map((p, i) => (
          <p key={i} style={{ color: p.color }} className="font-mono">{p.name}: {p.value.toFixed(4)}</p>
        ))}
      </div>
    );
  }
  return null;
};

export default function ModelPerformance() {
  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Model Performance</h2>
        <p className="text-sm text-slate-500 mt-0.5">LightGBM Classifier — training configuration and evaluation metrics</p>
      </div>

      {/* Model Info Banner */}
      <div className="bg-slate-900 text-white rounded-xl p-5 flex flex-wrap gap-6 items-center">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-lg bg-blue-600 flex items-center justify-center">
            <Cpu size={20} />
          </div>
          <div>
            <p className="text-xs text-slate-400">Algorithm</p>
            <p className="text-base font-bold">LightGBM Classifier</p>
          </div>
        </div>
        <div className="flex gap-6 flex-wrap text-sm">
          {[
            ['Classification Type', 'Binary'],
            ['Class 0', 'Legitimate'],
            ['Class 1', 'Fraud'],
            ['Model Status', <span className="flex items-center gap-1"><CheckCircle2 size={13} className="text-emerald-400" /> Trained</span>],
          ].map(([k, v], i) => (
            <div key={i}>
              <p className="text-xs text-slate-400">{k}</p>
              <p className="font-semibold text-white">{v}</p>
            </div>
          ))}
        </div>
      </div>

      {/* Training Stats */}
      <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
        {statItems.map(({ label, value, icon: Icon, color }) => (
          <div key={label} className={`flex items-center gap-3 border border-slate-200 bg-white rounded-xl p-4 shadow-sm`}>
            <div className={`flex items-center justify-center w-9 h-9 rounded-lg ${color}`}>
              <Icon size={16} />
            </div>
            <div>
              <p className="text-xs text-slate-500">{label}</p>
              <p className="text-lg font-black text-slate-900">{value}</p>
            </div>
          </div>
        ))}
      </div>

      {/* Metrics table + bar chart */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {/* Metrics table */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-800 mb-4">Test Set Metrics</h3>
          <div className="space-y-3">
            {metricRows.map((m) => (
              <div key={m.name}>
                <div className="flex justify-between items-center mb-1">
                  <span className="text-xs font-semibold text-slate-700">{m.name}</span>
                  <span className={`text-xs font-bold font-mono ${m.textColor}`}>{m.value.toFixed(4)}</span>
                </div>
                <div className="h-2 bg-slate-100 rounded-full overflow-hidden">
                  <div
                    className={`h-full rounded-full ${m.color} transition-all duration-700`}
                    style={{ width: `${m.value * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Validation vs Test Chart */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-800 mb-1">Validation vs Test Performance</h3>
          <p className="text-xs text-slate-500 mb-4">Comparison of key metrics across evaluation sets</p>
          <ResponsiveContainer width="100%" height={220}>
            <BarChart data={VAL_VS_TEST_PERFORMANCE} barSize={28} barGap={8}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="name" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis domain={[0, 1]} tick={{ fontSize: 11, fill: '#64748b' }} />
              <Tooltip content={<CustomTooltip />} />
              <Legend wrapperStyle={{ fontSize: '12px' }} />
              <Bar dataKey="Validation" fill="#6366f1" radius={[4, 4, 0, 0]} />
              <Bar dataKey="Test"       fill="#3b82f6" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          <div className="mt-3 bg-slate-50 border border-slate-200 rounded-lg px-4 py-3 text-xs text-slate-600">
            <strong>Observation:</strong> Slight drop from validation to test metrics is expected and indicates the model generalizes reasonably.
            ROC-AUC dropped from <strong>0.8951 → 0.8899</strong>, Average Precision from <strong>0.5415 → 0.5032</strong>.
          </div>
        </div>
      </div>
    </div>
  );
}
