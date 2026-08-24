import React from 'react';
import {
  PieChart, Pie, Cell, BarChart, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import {
  Activity, ShieldAlert, Percent, TrendingUp,
  Target, SlidersHorizontal, AlertCircle, CheckCircle2
} from 'lucide-react';
import MetricCard from '../components/MetricCard';
import TransactionTable from '../components/TransactionTable';
import SystemFlow from '../components/SystemFlow';
import {
  SYSTEM_METRICS, FRAUD_VS_LEGIT_DATA, PERFORMANCE_METRICS_DATA,
  CONFUSION_MATRIX, RISK_DISTRIBUTION, MOCK_TRANSACTIONS
} from '../data/mockData';

const PIE_COLORS = ['#10b981', '#ef4444'];

const CUSTOM_TOOLTIP = ({ active, payload }) => {
  if (active && payload?.length) {
    return (
      <div className="bg-white border border-slate-200 rounded-lg px-3 py-2 shadow-lg text-xs">
        <p className="font-semibold text-slate-800">{payload[0].name}</p>
        <p className="text-slate-600">{payload[0].value?.toLocaleString()}</p>
      </div>
    );
  }
  return null;
};

const BAR_TOOLTIP = ({ active, payload, label }) => {
  if (active && payload?.length) {
    return (
      <div className="bg-white border border-slate-200 rounded-lg px-3 py-2 shadow-lg text-xs">
        <p className="font-semibold text-slate-800">{label}</p>
        <p className="text-blue-600 font-mono">{payload[0].value?.toFixed(4)}</p>
      </div>
    );
  }
  return null;
};

// Confusion matrix cell
const CMCell = ({ value, label, color, textColor }) => (
  <div className={`flex flex-col items-center justify-center p-4 rounded-xl ${color}`}>
    <p className={`text-2xl font-black ${textColor}`}>{value.toLocaleString()}</p>
    <p className={`text-xs font-semibold mt-1 text-center ${textColor} opacity-80`}>{label}</p>
  </div>
);

export default function Dashboard() {
  const recentTxns = MOCK_TRANSACTIONS.slice(0, 8);

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      {/* Header */}
      <div>
        <h2 className="text-xl font-bold text-slate-900">Fraud Detection Dashboard</h2>
        <p className="text-sm text-slate-500 mt-0.5">Online Payment Fraud Risk Monitoring</p>
        <div className="inline-flex items-center gap-1.5 mt-2 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-medium px-2.5 py-1 rounded-full">
          <AlertCircle size={11} />
          All metrics are from Model Test Set Evaluation — not live banking data
        </div>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4">
        <MetricCard
          title="Total Transactions"
          value="88,581"
          subtitle="Test set size"
          icon={Activity}
          iconBg="bg-blue-100"
          iconColor="text-blue-600"
          badge="Test Set"
          badgeColor="bg-blue-50 text-blue-700"
        />
        <MetricCard
          title="Fraudulent Transactions"
          value="3,083"
          subtitle="Predicted fraud"
          icon={ShieldAlert}
          iconBg="bg-red-100"
          iconColor="text-red-600"
          valueColor="text-red-600"
          badge="Flagged"
          badgeColor="bg-red-50 text-red-700"
        />
        <MetricCard
          title="Fraud Rate"
          value="3.48%"
          subtitle="Of total transactions"
          icon={Percent}
          iconBg="bg-orange-100"
          iconColor="text-orange-600"
          valueColor="text-orange-600"
          badge="Test Set"
          badgeColor="bg-orange-50 text-orange-700"
        />
        <MetricCard
          title="Model ROC-AUC"
          value="0.8899"
          subtitle="Area under ROC curve"
          icon={TrendingUp}
          iconBg="bg-emerald-100"
          iconColor="text-emerald-600"
          valueColor="text-emerald-700"
          badge="LightGBM"
          badgeColor="bg-emerald-50 text-emerald-700"
        />
        <MetricCard
          title="Average Precision"
          value="0.5032"
          subtitle="Precision-recall AUC"
          icon={Target}
          iconBg="bg-violet-100"
          iconColor="text-violet-600"
          badge="Test Set"
          badgeColor="bg-violet-50 text-violet-700"
        />
        <MetricCard
          title="Risk Threshold"
          value="0.20"
          subtitle="Current detection cutoff"
          icon={SlidersHorizontal}
          iconBg="bg-amber-100"
          iconColor="text-amber-600"
          valueColor="text-amber-700"
          badge="Configurable"
          badgeColor="bg-amber-50 text-amber-700"
        />
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Donut Chart */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-800 mb-1">Fraud vs Legitimate</h3>
          <p className="text-xs text-slate-500 mb-4">Distribution across test set</p>
          <div className="flex items-center gap-4">
            <ResponsiveContainer width="60%" height={160}>
              <PieChart>
                <Pie
                  data={FRAUD_VS_LEGIT_DATA}
                  cx="50%" cy="50%"
                  innerRadius={45} outerRadius={70}
                  dataKey="value" paddingAngle={3}
                >
                  {FRAUD_VS_LEGIT_DATA.map((entry, i) => (
                    <Cell key={i} fill={PIE_COLORS[i]} />
                  ))}
                </Pie>
                <Tooltip content={<CUSTOM_TOOLTIP />} />
              </PieChart>
            </ResponsiveContainer>
            <div className="space-y-3 flex-1">
              {FRAUD_VS_LEGIT_DATA.map((d, i) => (
                <div key={i}>
                  <div className="flex items-center gap-2 mb-1">
                    <div className="w-2.5 h-2.5 rounded-full shrink-0" style={{ backgroundColor: PIE_COLORS[i] }} />
                    <span className="text-xs font-semibold text-slate-700">{d.name}</span>
                  </div>
                  <p className="text-lg font-black text-slate-900 leading-none ml-4">{d.value.toLocaleString()}</p>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Performance Bar Chart */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm lg:col-span-2">
          <h3 className="text-sm font-bold text-slate-800 mb-1">Fraud Detection Performance</h3>
          <p className="text-xs text-slate-500 mb-4">Test set evaluation metrics — LightGBM</p>
          <ResponsiveContainer width="100%" height={160}>
            <BarChart data={PERFORMANCE_METRICS_DATA} barSize={28}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="metric" tick={{ fontSize: 11, fill: '#64748b' }} />
              <YAxis domain={[0, 1]} tick={{ fontSize: 11, fill: '#64748b' }} />
              <Tooltip content={<BAR_TOOLTIP />} />
              <Bar dataKey="score" radius={[4, 4, 0, 0]}>
                {PERFORMANCE_METRICS_DATA.map((entry, i) => (
                  <Cell key={i} fill={i === 0 ? '#10b981' : i === 1 ? '#3b82f6' : '#6366f1'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4">
        {/* Confusion Matrix */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-800 mb-1">Confusion Matrix</h3>
          <p className="text-xs text-slate-500 mb-4">Test set — threshold 0.20</p>
          <div className="grid grid-cols-2 gap-2 mb-3">
            <CMCell
              value={CONFUSION_MATRIX.actualLegitPredictedLegit}
              label="True Negative (Legit → Legit)"
              color="bg-emerald-50 border border-emerald-200"
              textColor="text-emerald-800"
            />
            <CMCell
              value={CONFUSION_MATRIX.actualLegitPredictedFraud}
              label="False Positive (Legit → Fraud)"
              color="bg-amber-50 border border-amber-200"
              textColor="text-amber-800"
            />
            <CMCell
              value={CONFUSION_MATRIX.actualFraudPredictedLegit}
              label="False Negative (Fraud → Legit)"
              color="bg-orange-50 border border-orange-200"
              textColor="text-orange-800"
            />
            <CMCell
              value={CONFUSION_MATRIX.actualFraudPredictedFraud}
              label="True Positive (Fraud → Fraud)"
              color="bg-red-50 border border-red-200"
              textColor="text-red-800"
            />
          </div>
          <div className="flex justify-between text-xs text-slate-400 px-1">
            <span>← Predicted: Legit</span>
            <span>Predicted: Fraud →</span>
          </div>
        </div>

        {/* Risk Distribution */}
        <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm lg:col-span-2">
          <h3 className="text-sm font-bold text-slate-800 mb-1">Fraud Risk Distribution</h3>
          <p className="text-xs text-slate-500 mb-5">Transactions grouped by predicted risk level — demonstration data</p>
          <div className="space-y-4">
            {RISK_DISTRIBUTION.map((item, i) => {
              const total = RISK_DISTRIBUTION.reduce((s, x) => s + x.count, 0);
              const pct = ((item.count / total) * 100).toFixed(1);
              const colors = [
                { bar: 'bg-emerald-500', text: 'text-emerald-700', bg: 'bg-emerald-50' },
                { bar: 'bg-amber-500',   text: 'text-amber-700',   bg: 'bg-amber-50' },
                { bar: 'bg-red-500',     text: 'text-red-700',     bg: 'bg-red-50' },
              ];
              return (
                <div key={i}>
                  <div className="flex justify-between items-center mb-1.5">
                    <span className="text-xs font-semibold text-slate-700">{item.name}</span>
                    <div className="flex items-center gap-2">
                      <span className={`text-xs font-bold ${colors[i].text}`}>{item.count.toLocaleString()}</span>
                      <span className={`text-xs font-medium px-1.5 py-0.5 rounded ${colors[i].bg} ${colors[i].text}`}>{pct}%</span>
                    </div>
                  </div>
                  <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full ${colors[i].bar} transition-all duration-500`}
                      style={{ width: `${pct}%` }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>

      {/* Bottom Row: Table + System Flow */}
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
        {/* Recent Transactions */}
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm xl:col-span-3">
          <div className="flex items-center justify-between px-5 py-4 border-b border-slate-100">
            <div>
              <h3 className="text-sm font-bold text-slate-800">Recent Transactions</h3>
              <p className="text-xs text-slate-500 mt-0.5">Latest 8 mock transactions</p>
            </div>
            <div className="flex items-center gap-1.5 text-xs text-emerald-600 font-medium bg-emerald-50 px-2.5 py-1 rounded-full">
              <CheckCircle2 size={12} />
              Live mock data
            </div>
          </div>
          <TransactionTable transactions={recentTxns} />
        </div>

        {/* System Flow */}
        <SystemFlow />
      </div>
    </div>
  );
}
