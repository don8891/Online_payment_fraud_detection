import React, { useState } from 'react';
import { Server, Cpu, SlidersHorizontal, ToggleLeft, ToggleRight, Info, CheckCircle2 } from 'lucide-react';

export default function Settings() {
  const [apiUrl, setApiUrl]         = useState('http://localhost:5000');
  const [threshold, setThreshold]   = useState('0.20');
  const [liveMode, setLiveMode]     = useState(false);
  const [shapEnabled, setShap]      = useState(false);
  const [savedMsg, setSavedMsg]     = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSavedMsg(true);
    setTimeout(() => setSavedMsg(false), 3000);
  };

  const fieldClass = "w-full px-3 py-2 text-sm bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-800 font-mono";
  const labelClass = "block text-xs font-semibold text-slate-600 mb-1.5";

  return (
    <div className="p-6 space-y-6 animate-fade-in">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Settings</h2>
        <p className="text-sm text-slate-500 mt-0.5">Configure API endpoints, model preferences, and feature toggles</p>
        <div className="inline-flex items-center gap-1.5 mt-2 bg-blue-50 border border-blue-200 text-blue-700 text-xs font-medium px-2.5 py-1 rounded-full">
          <Info size={11} />
          These settings will take effect when the Flask API backend is connected
        </div>
      </div>

      <form onSubmit={handleSave} className="space-y-5 max-w-2xl">
        {/* API Configuration */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
            <Server size={16} className="text-blue-600" />
            <h3 className="text-sm font-bold text-slate-800">Flask API Configuration</h3>
          </div>

          <div>
            <label className={labelClass}>Flask Server URL</label>
            <input
              type="url"
              value={apiUrl}
              onChange={(e) => setApiUrl(e.target.value)}
              className={fieldClass}
              placeholder="http://localhost:5000"
            />
            <p className="text-xs text-slate-400 mt-1">The base URL of your Python/Flask fraud detection API</p>
          </div>

          <div className="grid grid-cols-2 gap-4 bg-slate-50 border border-slate-200 rounded-lg p-3">
            {[
              ['/api/health', 'Health Check'],
              ['/api/predict', 'Fraud Prediction'],
              ['/api/explain', 'SHAP Explanation'],
              ['/api/metrics', 'Model Metrics'],
            ].map(([path, label]) => (
              <div key={path} className="flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-slate-400" />
                <div>
                  <p className="text-xs text-slate-400">{label}</p>
                  <p className="text-xs font-mono text-slate-700">{path}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Model Settings */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
            <Cpu size={16} className="text-violet-600" />
            <h3 className="text-sm font-bold text-slate-800">Model Configuration</h3>
          </div>

          <div>
            <label className={labelClass}>Default Risk Threshold</label>
            <input
              type="number" min="0.01" max="0.99" step="0.01"
              value={threshold}
              onChange={(e) => setThreshold(e.target.value)}
              className={fieldClass}
            />
            <p className="text-xs text-slate-400 mt-1">Transactions with fraud probability ≥ this threshold are classified as fraud</p>
          </div>

          <div className="bg-slate-50 border border-slate-200 rounded-lg p-3 grid grid-cols-2 gap-3 text-xs">
            {[
              ['Algorithm', 'LightGBM Classifier'],
              ['Task', 'Binary Classification'],
              ['Feature Count', '421'],
              ['Training Size', '150,000 samples'],
            ].map(([k, v]) => (
              <div key={k}>
                <p className="text-slate-400">{k}</p>
                <p className="font-semibold text-slate-700 font-mono">{v}</p>
              </div>
            ))}
          </div>
        </div>

        {/* Feature Toggles */}
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm space-y-4">
          <div className="flex items-center gap-2 pb-2 border-b border-slate-100">
            <SlidersHorizontal size={16} className="text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-800">Feature Toggles</h3>
          </div>

          {[
            { label: 'Live API Mode',           desc: 'Connect to Flask backend for real predictions (currently mock)',   state: liveMode, setter: setLiveMode },
            { label: 'SHAP Explanations',       desc: 'Enable SHAP feature contribution analysis (requires SHAP library)', state: shapEnabled, setter: setShap },
          ].map(({ label, desc, state, setter }) => (
            <div key={label} className="flex items-center justify-between gap-4 py-2">
              <div>
                <p className="text-sm font-semibold text-slate-800">{label}</p>
                <p className="text-xs text-slate-500 mt-0.5">{desc}</p>
              </div>
              <button
                type="button"
                onClick={() => setter(!state)}
                className={`shrink-0 transition-colors ${state ? 'text-blue-600' : 'text-slate-400'}`}
              >
                {state ? <ToggleRight size={28} /> : <ToggleLeft size={28} />}
              </button>
            </div>
          ))}
        </div>

        {/* Save */}
        <div className="flex items-center gap-3">
          <button
            type="submit"
            className="px-6 py-2.5 bg-slate-900 hover:bg-slate-700 text-white text-sm font-semibold rounded-lg transition-colors"
          >
            Save Settings
          </button>
          {savedMsg && (
            <div className="flex items-center gap-1.5 text-emerald-600 text-sm font-medium animate-fade-in">
              <CheckCircle2 size={16} />
              Settings saved
            </div>
          )}
        </div>
      </form>
    </div>
  );
}
