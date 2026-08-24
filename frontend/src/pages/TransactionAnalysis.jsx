import React, { useState } from 'react';
import { Send, AlertTriangle, CheckCircle2, Info, Loader2 } from 'lucide-react';
import RiskGauge from '../components/RiskGauge';
import RiskBadge from '../components/RiskBadge';

const PRODUCTS = ['W', 'C', 'H', 'R', 'S'];
const CARD_TYPES = ['Visa', 'Mastercard', 'Discover', 'Amex'];
const CARD_CATEGORIES = ['Standard', 'Classic', 'Gold', 'Platinum', 'Signature', 'Black', 'Centurion'];
const DEVICE_TYPES = ['desktop', 'mobile', 'tablet'];

/** Mock scoring logic — frontend only, will be replaced by Flask API */
function computeMockScore(form) {
  let score = 0.05;
  const amt = parseFloat(form.amount) || 0;
  if (amt > 1000) score += 0.3;
  else if (amt > 500) score += 0.15;
  else if (amt > 200) score += 0.06;

  const suspiciousDomains = ['protonmail.com', 'tempmail.xyz', 'yandex.ru', 'mail.ru', 'anonymous.net'];
  if (suspiciousDomains.includes(form.payerEmail)) score += 0.25;
  if (suspiciousDomains.includes(form.receiverEmail)) score += 0.20;

  if (form.product === 'C') score += 0.10;
  if (form.product === 'R') score += 0.08;
  if (form.cardType === 'Amex') score += 0.05;
  if (form.cardCategory === 'Black' || form.cardCategory === 'Centurion') score += 0.08;
  if (form.deviceType === 'mobile') score += 0.05;

  return Math.min(Math.max(score, 0), 0.99);
}

export default function TransactionAnalysis() {
  const [form, setForm] = useState({
    amount: '', product: 'W', cardType: 'Visa',
    cardCategory: 'Standard', payerEmail: 'gmail.com',
    receiverEmail: 'gmail.com', deviceType: 'desktop', deviceInfo: ''
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleChange = (field) => (e) => setForm(prev => ({ ...prev, [field]: e.target.value }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setResult(null);
    await new Promise(r => setTimeout(r, 900)); // Simulate API latency
    const score = computeMockScore(form);
    const threshold = 0.20;
    const riskLevel = score < 0.20 ? 'LOW' : score < 0.50 ? 'MEDIUM' : 'HIGH';
    const prediction = score >= threshold ? 'Fraud' : 'Legitimate';
    setResult({ score, riskLevel, prediction, threshold });
    setLoading(false);
  };

  const fieldClass = "w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition text-slate-800";
  const labelClass = "block text-xs font-semibold text-slate-600 mb-1.5";

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Transaction Analysis</h2>
        <p className="text-sm text-slate-500 mt-0.5">Analyze a transaction for fraud risk using mock scoring logic</p>
        <div className="inline-flex items-center gap-1.5 mt-2 bg-amber-50 border border-amber-200 text-amber-700 text-xs font-medium px-2.5 py-1 rounded-full">
          <Info size={11} />
          Frontend mock only — will connect to Flask / LightGBM API in Phase 2
        </div>
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-5 gap-6">
        {/* Form */}
        <form onSubmit={handleSubmit} className="xl:col-span-3 bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-5">
          <h3 className="text-sm font-bold text-slate-800 border-b border-slate-100 pb-3">Transaction Details</h3>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div>
              <label className={labelClass}>Transaction Amount ($)</label>
              <input
                type="number" min="0" step="0.01" required
                placeholder="e.g. 845.00"
                value={form.amount} onChange={handleChange('amount')}
                className={fieldClass}
              />
            </div>
            <div>
              <label className={labelClass}>Product Code</label>
              <select value={form.product} onChange={handleChange('product')} className={fieldClass}>
                {PRODUCTS.map(p => <option key={p}>{p}</option>)}
              </select>
            </div>
            <div>
              <label className={labelClass}>Card Type</label>
              <select value={form.cardType} onChange={handleChange('cardType')} className={fieldClass}>
                {CARD_TYPES.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className={labelClass}>Card Category</label>
              <select value={form.cardCategory} onChange={handleChange('cardCategory')} className={fieldClass}>
                {CARD_CATEGORIES.map(c => <option key={c}>{c}</option>)}
              </select>
            </div>
            <div>
              <label className={labelClass}>Payer Email Domain</label>
              <input
                type="text" placeholder="e.g. gmail.com"
                value={form.payerEmail} onChange={handleChange('payerEmail')}
                className={fieldClass}
              />
            </div>
            <div>
              <label className={labelClass}>Receiver Email Domain</label>
              <input
                type="text" placeholder="e.g. outlook.com"
                value={form.receiverEmail} onChange={handleChange('receiverEmail')}
                className={fieldClass}
              />
            </div>
            <div>
              <label className={labelClass}>Device Type</label>
              <select value={form.deviceType} onChange={handleChange('deviceType')} className={fieldClass}>
                {DEVICE_TYPES.map(d => <option key={d}>{d}</option>)}
              </select>
            </div>
            <div>
              <label className={labelClass}>Device Information</label>
              <input
                type="text" placeholder="e.g. Windows/Chrome"
                value={form.deviceInfo} onChange={handleChange('deviceInfo')}
                className={fieldClass}
              />
            </div>
          </div>

          <button
            type="submit"
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 bg-slate-900 hover:bg-slate-700 text-white text-sm font-semibold py-2.5 px-6 rounded-lg transition-colors disabled:opacity-60 disabled:cursor-not-allowed"
          >
            {loading
              ? <><Loader2 size={15} className="animate-spin" /> Analyzing...</>
              : <><Send size={14} /> Analyze Transaction</>
            }
          </button>
        </form>

        {/* Result panel */}
        <div className="xl:col-span-2 space-y-4">
          {!result && !loading && (
            <div className="bg-white border border-slate-200 rounded-xl p-8 flex flex-col items-center justify-center text-center h-full min-h-64 shadow-sm">
              <div className="w-12 h-12 rounded-full bg-slate-100 flex items-center justify-center mb-3">
                <Send size={20} className="text-slate-400" />
              </div>
              <p className="text-sm font-semibold text-slate-700">No analysis yet</p>
              <p className="text-xs text-slate-400 mt-1">Fill in the form and click Analyze Transaction</p>
            </div>
          )}

          {result && (
            <div className="animate-fade-in space-y-4">
              {/* Gauge */}
              <div className={`bg-white border rounded-xl p-6 shadow-sm text-center ${
                result.prediction === 'Fraud' ? 'border-red-200' : 'border-emerald-200'
              }`}>
                <p className="text-xs font-semibold text-slate-500 mb-3">Risk Score</p>
                <RiskGauge score={result.score} />
                <div className="mt-4 space-y-2">
                  <div className="flex items-center justify-center gap-2">
                    <span className="text-xs text-slate-500">Prediction:</span>
                    <RiskBadge type={result.prediction} />
                  </div>
                  <div className="flex items-center justify-center gap-2">
                    <span className="text-xs text-slate-500">Risk Score:</span>
                    <span className="text-xs font-bold font-mono text-slate-800">{result.score.toFixed(4)}</span>
                  </div>
                  <div className="flex items-center justify-center gap-2">
                    <span className="text-xs text-slate-500">Threshold:</span>
                    <span className="text-xs font-mono text-slate-600">≥ {result.threshold}</span>
                  </div>
                </div>
              </div>

              {/* Decision banner */}
              {result.prediction === 'Fraud' ? (
                <div className="flex items-start gap-3 bg-red-50 border border-red-200 rounded-xl p-4">
                  <AlertTriangle size={18} className="text-red-600 shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-bold text-red-800">Transaction Flagged</p>
                    <p className="text-xs text-red-600 mt-0.5">This transaction has been flagged for further investigation. Risk score ({result.score.toFixed(2)}) exceeds threshold ({result.threshold}).</p>
                  </div>
                </div>
              ) : (
                <div className="flex items-start gap-3 bg-emerald-50 border border-emerald-200 rounded-xl p-4">
                  <CheckCircle2 size={18} className="text-emerald-600 shrink-0 mt-0.5" />
                  <div>
                    <p className="text-sm font-bold text-emerald-800">Transaction Approved</p>
                    <p className="text-xs text-emerald-600 mt-0.5">Risk score ({result.score.toFixed(2)}) is below threshold ({result.threshold}). Transaction appears legitimate.</p>
                  </div>
                </div>
              )}

              <p className="text-xs text-center text-slate-400 italic">
                ⚠ Mock scoring — Flask/LightGBM API integration pending
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
