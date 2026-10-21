import React from 'react';
import {
  FileCheck2,
  Cpu,
  ShieldCheck,
  BarChart2,
  Download,
  ArrowRight
} from 'lucide-react';

export default function EmptyState({ onDownloadSample }) {
  return (
    <div className="bg-white rounded-2xl p-8 sm:p-10 border border-slate-200 shadow-xs text-center max-w-3xl mx-auto space-y-6">
      
      {/* Icon */}
      <div className="w-16 h-16 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center mx-auto border border-blue-100 shadow-2xs">
        <FileCheck2 size={32} />
      </div>

      {/* Main Copy */}
      <div className="space-y-1.5">
        <h3 className="text-lg sm:text-xl font-extrabold text-slate-900 tracking-tight">
          Upload a transaction dataset to start fraud analysis
        </h3>
        <p className="text-xs text-slate-500 max-w-lg mx-auto leading-relaxed">
          Select or drag & drop a transaction CSV batch above to generate real-time machine learning predictions evaluated through the FedProx Global Deep Neural Network.
        </p>
      </div>

      {/* Highlights */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3.5 text-left pt-2">
        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
          <div className="p-1.5 bg-blue-100 text-blue-600 rounded-lg w-fit">
            <Cpu size={16} />
          </div>
          <h4 className="text-xs font-bold text-slate-900">421-Feature FedProx DNN</h4>
          <p className="text-[11px] text-slate-500 leading-snug">
            Evaluates card details, device fingerprints, transaction amounts, and behavioral timestamps.
          </p>
        </div>

        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
          <div className="p-1.5 bg-amber-100 text-amber-600 rounded-lg w-fit">
            <ShieldCheck size={16} />
          </div>
          <h4 className="text-xs font-bold text-slate-900">Decision Threshold</h4>
          <p className="text-[11px] text-slate-500 leading-snug">
            Optimized decision boundary (cutoff ≥ 0.85) calibrated to reduce false alerts on legitimate payments.
          </p>
        </div>

        <div className="p-4 bg-slate-50 rounded-xl border border-slate-200 space-y-1.5">
          <div className="p-1.5 bg-emerald-100 text-emerald-600 rounded-lg w-fit">
            <BarChart2 size={16} />
          </div>
          <h4 className="text-xs font-bold text-slate-900">Visual Analytics</h4>
          <p className="text-[11px] text-slate-500 leading-snug">
            Interactive fraud-ratio charts, probability spread histograms, and exportable ledger CSVs.
          </p>
        </div>
      </div>

      {/* Download Action */}
      <div className="pt-2">
        <button
          onClick={onDownloadSample}
          type="button"
          className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-800 hover:underline cursor-pointer"
        >
          <Download size={14} />
          Need test data? Download sample transaction CSV
        </button>
      </div>

    </div>
  );
}
