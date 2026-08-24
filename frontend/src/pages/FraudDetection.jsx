import React, { useState } from 'react';
import { Info, ShieldCheck, ShieldX, SlidersHorizontal } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';

const EXAMPLE_TRANSACTIONS = [
  { id: 'TXN-A1', amount: '$15.99',   score: 0.03, product: 'W', email: 'gmail.com',       desc: 'Low-value, trusted domain, familiar card' },
  { id: 'TXN-A2', amount: '$320.45',  score: 0.21, product: 'H', email: 'yahoo.com',       desc: 'Moderate amount, slightly unusual product code' },
  { id: 'TXN-A3', amount: '$1,850.00',score: 0.87, product: 'C', email: 'protonmail.com',  desc: 'High value, suspicious email domain, anomalous device' },
];

export default function FraudDetection() {
  const [threshold, setThreshold] = useState(0.20);

  const classify = (score) => (score >= threshold ? 'Fraud' : 'Legitimate');
  const statusOf   = (score) => (score >= threshold ? 'BLOCKED' : 'SAFE');

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Fraud Detection</h2>
        <p className="text-sm text-slate-500 mt-0.5">Adjust the classification threshold and observe its effect on predictions</p>
      </div>

      {/* Threshold Configurator */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <div className="flex items-center gap-2 mb-1">
          <SlidersHorizontal size={16} className="text-slate-600" />
          <h3 className="text-sm font-bold text-slate-800">Risk Threshold</h3>
        </div>
        <p className="text-xs text-slate-500 mb-6">
          If predicted fraud probability is <strong>≥ threshold</strong>, the transaction is classified as <strong className="text-red-600">Fraud</strong>.
        </p>

        <div className="flex items-center gap-6">
          <div className="flex-1">
            <input
              type="range" min="0.01" max="0.99" step="0.01"
              value={threshold}
              onChange={(e) => setThreshold(parseFloat(e.target.value))}
              className="w-full h-2 appearance-none rounded-full bg-slate-200 cursor-pointer"
              style={{ background: `linear-gradient(to right, #0f172a ${threshold * 100}%, #e2e8f0 ${threshold * 100}%)` }}
            />
            <div className="flex justify-between text-xs text-slate-400 mt-1.5">
              <span>0.01 (More Sensitive)</span>
              <span>0.99 (Less Sensitive)</span>
            </div>
          </div>
          <div className="flex flex-col items-center bg-slate-900 text-white rounded-xl px-6 py-3 min-w-[90px]">
            <span className="text-xs text-slate-400">Threshold</span>
            <span className="text-2xl font-black font-mono">{threshold.toFixed(2)}</span>
          </div>
        </div>

        {/* Info box */}
        <div className="mt-5 flex items-start gap-2.5 bg-blue-50 border border-blue-200 rounded-lg px-4 py-3">
          <Info size={15} className="text-blue-600 mt-0.5 shrink-0" />
          <p className="text-xs text-blue-700">
            <strong>Trade-off:</strong> Lower thresholds increase fraud detection recall (catch more fraud) but may increase <strong>false positives</strong> — legitimate transactions incorrectly flagged as fraud.
            Higher thresholds reduce false positives but may <strong>miss actual fraud cases</strong>.
          </p>
        </div>
      </div>

      {/* Live Example Transactions */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-bold text-slate-800 mb-1">Live Classification Examples</h3>
        <p className="text-xs text-slate-500 mb-5">
          Observe how the threshold affects these 3 example transactions in real time
        </p>
        <div className="space-y-4">
          {EXAMPLE_TRANSACTIONS.map((tx) => {
            const prediction = classify(tx.score);
            const isFraud = prediction === 'Fraud';
            return (
              <div
                key={tx.id}
                className={`flex flex-col sm:flex-row sm:items-center gap-4 p-4 rounded-xl border transition-colors ${
                  isFraud ? 'bg-red-50 border-red-200' : 'bg-emerald-50 border-emerald-200'
                }`}
              >
                {/* Icon */}
                <div className={`flex items-center justify-center w-10 h-10 rounded-full shrink-0 ${
                  isFraud ? 'bg-red-100' : 'bg-emerald-100'
                }`}>
                  {isFraud
                    ? <ShieldX size={20} className="text-red-600" />
                    : <ShieldCheck size={20} className="text-emerald-600" />
                  }
                </div>

                {/* Details */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 flex-wrap">
                    <span className="text-sm font-bold text-slate-800 font-mono">{tx.id}</span>
                    <span className="text-sm font-bold text-slate-900">{tx.amount}</span>
                    <span className="text-xs text-slate-500">Product: {tx.product}</span>
                    <span className="text-xs text-slate-500">Email: {tx.email}</span>
                  </div>
                  <p className="text-xs text-slate-500 mt-1">{tx.desc}</p>
                </div>

                {/* Risk score + badges */}
                <div className="flex items-center gap-3 shrink-0">
                  <div className="text-center">
                    <p className="text-xs text-slate-500 mb-0.5">Risk Score</p>
                    <div className="flex items-center gap-1.5">
                      <div className="w-16 h-1.5 bg-slate-200 rounded-full overflow-hidden">
                        <div
                          className="h-full rounded-full"
                          style={{
                            width: `${tx.score * 100}%`,
                            backgroundColor: tx.score < 0.2 ? '#10b981' : tx.score < 0.5 ? '#f59e0b' : '#ef4444'
                          }}
                        />
                      </div>
                      <span className="text-xs font-bold font-mono text-slate-800">{tx.score.toFixed(2)}</span>
                    </div>
                    <p className="text-xs text-slate-400 mt-0.5">
                      {isFraud ? `≥ ${threshold.toFixed(2)} → FRAUD` : `< ${threshold.toFixed(2)} → LEGIT`}
                    </p>
                  </div>
                  <div className="flex flex-col gap-1.5 items-end">
                    <RiskBadge type={prediction} />
                    <RiskBadge type={statusOf(tx.score)} />
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Summary table */}
      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-sm font-bold text-slate-800 mb-4">Threshold Impact Summary</h3>
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: 'Classified as Fraud',     value: EXAMPLE_TRANSACTIONS.filter(t => t.score >= threshold).length, color: 'text-red-600',     bg: 'bg-red-50 border-red-200' },
            { label: 'Classified as Legitimate', value: EXAMPLE_TRANSACTIONS.filter(t => t.score < threshold).length,  color: 'text-emerald-700', bg: 'bg-emerald-50 border-emerald-200' },
            { label: 'Current Threshold',        value: threshold.toFixed(2),                                           color: 'text-slate-800',   bg: 'bg-slate-50 border-slate-200' },
          ].map((item, i) => (
            <div key={i} className={`rounded-xl border p-4 text-center ${item.bg}`}>
              <p className={`text-2xl font-black ${item.color}`}>{item.value}</p>
              <p className="text-xs text-slate-500 mt-1">{item.label}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
