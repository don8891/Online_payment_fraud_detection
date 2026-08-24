import React from 'react';
import {
  PieChart, Pie, Cell, ResponsiveContainer, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid
} from 'recharts';
import { PieChart as PieIcon, BarChart2, TrendingUp } from 'lucide-react';

export default function VisualSummary({ transactions, summary }) {
  if (!transactions || transactions.length === 0) return null;

  // Chart 1 Data: Fraud vs Legitimate
  const fraudVsLegitData = [
    { name: 'Legitimate', value: summary?.legitimate_transactions || 0, color: '#10b981' },
    { name: 'Fraudulent', value: summary?.fraudulent_transactions || 0, color: '#f43f5e' }
  ];

  // Chart 2 Data: Risk Distribution
  const riskCounts = { HIGH: 0, MEDIUM: 0, LOW: 0 };
  transactions.forEach(t => {
    if (t.risk_level === 'HIGH') riskCounts.HIGH++;
    else if (t.risk_level === 'MEDIUM') riskCounts.MEDIUM++;
    else riskCounts.LOW++;
  });

  const riskDistributionData = [
    { name: 'High Risk (≥0.70)', count: riskCounts.HIGH, fill: '#ef4444' },
    { name: 'Medium Risk (0.20-0.69)', count: riskCounts.MEDIUM, fill: '#f59e0b' },
    { name: 'Low Risk (<0.20)', count: riskCounts.LOW, fill: '#10b981' }
  ];

  // Chart 3 Data: Probability Distribution Histogram (10 bins: 0-0.1, 0.1-0.2, ..., 0.9-1.0)
  const probBins = Array.from({ length: 10 }, (_, i) => {
    const min = (i / 10).toFixed(1);
    const max = ((i + 1) / 10).toFixed(1);
    return {
      range: `${min}-${max}`,
      count: 0,
      isFraudZone: i >= 2 // 0.20 threshold
    };
  });

  transactions.forEach(t => {
    const prob = t.fraud_probability;
    let binIdx = Math.floor(prob * 10);
    if (binIdx >= 10) binIdx = 9;
    if (binIdx < 0) binIdx = 0;
    probBins[binIdx].count++;
  });

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-6">
      <div className="pb-3 border-b border-slate-100 flex items-center justify-between">
        <div>
          <h2 className="text-lg font-bold text-slate-800 tracking-tight flex items-center gap-2">
            <PieIcon size={20} className="text-blue-600" />
            Visual Summary & Distribution Analytics
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Statistical breakdown of risk scores and fraud probability distributions
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Chart 1: Fraud vs Legitimate Donut Chart */}
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <PieIcon size={14} className="text-blue-600" />
              Fraud vs Legitimate Ratio
            </h3>
          </div>
          <div className="h-56 w-full py-2">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={fraudVsLegitData}
                  cx="50%"
                  cy="50%"
                  innerRadius={55}
                  outerRadius={75}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {fraudVsLegitData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val) => [val.toLocaleString(), 'Transactions']}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px', boxShadow: '0 4px 6px -1px rgba(0,0,0,0.1)' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '12px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 2: Risk Distribution Bar Chart */}
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <BarChart2 size={14} className="text-amber-600" />
              Risk Level Distribution
            </h3>
          </div>
          <div className="h-56 w-full py-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDistributionData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" tick={{ fontSize: 10 }} interval={0} angle={-15} textAnchor="end" />
                <YAxis tick={{ fontSize: 10 }} allowDecimals={false} />
                <Tooltip
                  formatter={(val) => [val.toLocaleString(), 'Count']}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {riskDistributionData.map((entry, index) => (
                    <Cell key={`cell-bar-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Chart 3: Fraud Probability Distribution Histogram */}
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/60">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp size={14} className="text-rose-600" />
              Probability Distribution Bins
            </h3>
            <span className="text-[10px] bg-rose-100 text-rose-800 font-semibold px-2 py-0.5 rounded">
              &ge;0.20 Flagged
            </span>
          </div>
          <div className="h-56 w-full py-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={probBins} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="range" tick={{ fontSize: 9 }} interval={0} angle={-30} textAnchor="end" />
                <YAxis tick={{ fontSize: 10 }} allowDecimals={false} />
                <Tooltip
                  formatter={(val) => [val.toLocaleString(), 'Transactions']}
                  labelFormatter={(lbl) => `Probability: ${lbl}`}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {probBins.map((entry, index) => (
                    <Cell key={`cell-prob-${index}`} fill={entry.isFraudZone ? '#f43f5e' : '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
}
