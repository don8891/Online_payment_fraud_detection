import React from 'react';
import { ShieldCheck, FileCheck2, Cpu, BarChart2 } from 'lucide-react';

export default function EmptyState({ onDownloadSample }) {
  return (
    <div className="bg-white rounded-2xl p-10 border border-slate-200 shadow-sm text-center max-w-3xl mx-auto space-y-6">
      <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto border border-blue-100 shadow-inner">
        <FileCheck2 size={32} />
      </div>

      <div className="space-y-2">
        <h3 className="text-xl font-bold text-slate-900 tracking-tight">
          Upload a transaction file to begin fraud analysis.
        </h3>
        <p className="text-xs text-slate-500 max-w-lg mx-auto leading-relaxed">
          Select or drag & drop a transaction CSV dataset into the upload area above to generate real-time machine learning predictions powered by LightGBM.
        </p>
      </div>

      {/* Feature Highlights Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-left pt-2">
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 space-y-1.5">
          <div className="p-1.5 bg-blue-100 text-blue-600 rounded-lg w-fit">
            <Cpu size={16} />
          </div>
          <h4 className="text-xs font-bold text-slate-800">421 Feature LightGBM</h4>
          <p className="text-[11px] text-slate-500">Evaluates cards, devices, amounts, and email domain signatures.</p>
        </div>

        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 space-y-1.5">
          <div className="p-1.5 bg-amber-100 text-amber-600 rounded-lg w-fit">
            <ShieldCheck size={16} />
          </div>
          <h4 className="text-xs font-bold text-slate-800">0.20 Decision Threshold</h4>
          <p className="text-[11px] text-slate-500">Optimized fraud threshold calibrated for high recall risk detection.</p>
        </div>

        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200/80 space-y-1.5">
          <div className="p-1.5 bg-emerald-100 text-emerald-600 rounded-lg w-fit">
            <BarChart2 size={16} />
          </div>
          <h4 className="text-xs font-bold text-slate-800">Visual Analytics</h4>
          <p className="text-[11px] text-slate-500">Interactive charts, risk levels, and exportable ledger CSVs.</p>
        </div>
      </div>

      <div className="pt-2">
        <button
          onClick={onDownloadSample}
          type="button"
          className="inline-flex items-center gap-2 text-xs font-bold text-blue-600 hover:text-blue-800 hover:underline"
        >
          Don't have a dataset? Download sample transaction CSV
        </button>
      </div>
    </div>
  );
}
