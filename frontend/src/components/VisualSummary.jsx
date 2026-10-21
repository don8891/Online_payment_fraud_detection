import React, { useMemo } from 'react';
import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid
} from 'recharts';
import {
  PieChart as PieIcon,
  BarChart2,
  TrendingUp,
  Activity,
  AlertCircle
} from 'lucide-react';

export default function VisualSummary({ transactions, summary, modelInfo }) {
  if (!transactions || transactions.length === 0) {
    return (
      <div className="bg-white rounded-2xl p-8 border border-slate-200 text-center space-y-2">
        <Activity size={32} className="text-slate-300 mx-auto" />
        <h3 className="text-sm font-bold text-slate-700">No Analytics to Display</h3>
        <p className="text-xs text-slate-400 max-w-sm mx-auto">
          Upload and analyze a transaction dataset to generate fraud distributions and probability charts.
        </p>
      </div>
    );
  }

  const threshold = modelInfo?.threshold !== undefined ? Number(modelInfo.threshold) : 0.85;

  // Chart 1 Data: Fraud vs Legitimate
  const fraudVsLegitData = useMemo(() => [
    { name: 'Legitimate', value: summary?.legitimate_transactions || 0, color: '#10b981' },
    { name: 'Fraudulent', value: summary?.fraudulent_transactions || 0, color: '#ef4444' }
  ], [summary]);

  // Chart 2 Data: Risk Distribution (Backend classifies: HIGH >=0.90, MEDIUM >=0.50, LOW <0.50)
  const riskDistributionData = useMemo(() => {
    let high = 0, med = 0, low = 0;
    transactions.forEach(t => {
      if (t.risk_level === 'HIGH') high++;
      else if (t.risk_level === 'MEDIUM') med++;
      else low++;
    });

    return [
      { name: 'High (≥0.90)', count: high, fill: '#ef4444' },
      { name: 'Medium (0.50-0.89)', count: med, fill: '#f59e0b' },
      { name: 'Low (<0.50)', count: low, fill: '#10b981' }
    ];
  }, [transactions]);

  // Chart 3 Data: Probability Distribution Histogram (10 bins)
  const probBins = useMemo(() => {
    const bins = Array.from({ length: 10 }, (_, i) => {
      const min = (i / 10).toFixed(1);
      const max = ((i + 1) / 10).toFixed(1);
      return {
        range: `${min}-${max}`,
        count: 0,
        isFraudZone: (i + 1) / 10 > threshold
      };
    });

    transactions.forEach(t => {
      const prob = Number(t.fraud_probability) || 0;
      let binIdx = Math.floor(prob * 10);
      if (binIdx >= 10) binIdx = 9;
      if (binIdx < 0) binIdx = 0;
      bins[binIdx].count++;
    });

    return bins;
  }, [transactions, threshold]);

  // Summary Metrics
  const avgProb = useMemo(() => {
    const sum = transactions.reduce((acc, t) => acc + (Number(t.fraud_probability) || 0), 0);
    return (sum / transactions.length * 100).toFixed(2);
  }, [transactions]);

  const maxProb = useMemo(() => {
    const max = Math.max(...transactions.map(t => Number(t.fraud_probability) || 0));
    return (max * 100).toFixed(1);
  }, [transactions]);

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-6">
      
      {/* Header */}
      <div className="pb-3 border-b border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <PieIcon size={20} className="text-blue-600" />
            Transaction Analytics & Probability Distributions
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Statistical breakdown of risk scores and model prediction outputs for the current dataset
          </p>
        </div>

        {/* Quick Analytical Callouts */}
        <div className="flex items-center gap-2 text-[11px] self-start sm:self-auto">
          <span className="bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg font-medium border border-slate-200">
            Avg Risk: <strong className="font-mono text-slate-900">{avgProb}%</strong>
          </span>
          <span className="bg-slate-100 text-slate-700 px-2.5 py-1 rounded-lg font-medium border border-slate-200">
            Max Risk: <strong className="font-mono text-rose-600">{maxProb}%</strong>
          </span>
        </div>
      </div>

      {/* 3 Analytics Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        
        {/* Chart 1: Fraud vs Legitimate Donut Chart */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/70">
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
                  innerRadius={50}
                  outerRadius={75}
                  paddingAngle={4}
                  dataKey="value"
                >
                  {fraudVsLegitData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(val) => [val.toLocaleString(), 'Transactions']}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px', border: '1px solid #cbd5e1' }}
                />
                <Legend verticalAlign="bottom" height={36} iconType="circle" wrapperStyle={{ fontSize: '11px' }} />
              </PieChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[10px] text-slate-500 text-center">
            Evaluated under decision threshold ≥ {threshold.toFixed(2)}
          </p>
        </div>

        {/* Chart 2: Risk Distribution Bar Chart */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/70">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <BarChart2 size={14} className="text-amber-600" />
              Risk Level Distribution
            </h3>
          </div>

          <div className="h-56 w-full py-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={riskDistributionData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="name" tick={{ fontSize: 10, fill: '#64748b' }} interval={0} angle={-10} textAnchor="end" />
                <YAxis tick={{ fontSize: 10, fill: '#64748b' }} allowDecimals={false} />
                <Tooltip
                  formatter={(val) => [val.toLocaleString(), 'Transactions']}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px', border: '1px solid #cbd5e1' }}
                />
                <Bar dataKey="count" radius={[5, 5, 0, 0]}>
                  {riskDistributionData.map((entry, index) => (
                    <Cell key={`cell-bar-${index}`} fill={entry.fill} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[10px] text-slate-500 text-center">
            Transactions grouped by backend risk policy
          </p>
        </div>

        {/* Chart 3: Probability Distribution Histogram */}
        <div className="bg-slate-50/70 rounded-xl p-4 border border-slate-200 flex flex-col justify-between">
          <div className="flex items-center justify-between pb-2 border-b border-slate-200/70">
            <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <TrendingUp size={14} className="text-rose-600" />
              Probability Spread (0.0 - 1.0)
            </h3>
            <span className="text-[10px] bg-rose-100 text-rose-800 font-bold px-2 py-0.5 rounded">
              ≥{threshold.toFixed(2)} Flagged
            </span>
          </div>

          <div className="h-56 w-full py-2">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={probBins} margin={{ top: 10, right: 10, left: -20, bottom: 25 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="range" tick={{ fontSize: 9, fill: '#64748b' }} interval={0} angle={-30} textAnchor="end" />
                <YAxis tick={{ fontSize: 10, fill: '#64748b' }} allowDecimals={false} />
                <Tooltip
                  formatter={(val) => [val.toLocaleString(), 'Count']}
                  labelFormatter={(lbl) => `Risk Range: ${lbl}`}
                  contentStyle={{ borderRadius: '8px', fontSize: '12px', border: '1px solid #cbd5e1' }}
                />
                <Bar dataKey="count" radius={[4, 4, 0, 0]}>
                  {probBins.map((entry, index) => (
                    <Cell key={`cell-prob-${index}`} fill={entry.isFraudZone ? '#ef4444' : '#3b82f6'} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
          <p className="text-[10px] text-slate-500 text-center">
            Red bars denote transactions exceeding the {threshold.toFixed(2)} threshold
          </p>
        </div>

      </div>
    </div>
  );
}
