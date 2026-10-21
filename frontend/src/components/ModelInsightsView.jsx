import React from 'react';
import {
  Cpu,
  Layers,
  Target,
  Database,
  ArrowRight,
  ShieldCheck,
  CheckCircle2,
  Server,
  Activity,
  Sliders,
  FileCode2,
  GitBranch,
  BookOpen
} from 'lucide-react';

export default function ModelInsightsView({
  backendConnected = false,
  modelInfo = {}
}) {
  const modelName = modelInfo?.model || 'FedProx DNN';
  const numFeatures = modelInfo?.num_features || 421;
  const threshold = modelInfo?.threshold !== undefined ? Number(modelInfo.threshold).toFixed(2) : '0.85';

  const verifiedMetrics = [
    { label: 'Validation ROC-AUC', value: '0.8319', note: 'Measured on X_val_dnn.pkl test set', highlight: true },
    { label: 'Fraud Decision Cutoff', value: `≥ ${threshold}`, note: 'Backend decision boundary' },
    { label: 'Input Feature Vector', value: `${numFeatures} Dims`, note: 'Preprocessed IEEE-CIS features' },
    { label: 'Proximal Regularization', value: 'μ = 0.01', note: 'Restrains local client weight drift' },
  ];

  const trainingArchitectureSteps = [
    {
      title: '1. Non-IID Client Partitions',
      desc: 'Simulated financial institutions (5 clients) each holding heterogeneous, non-identically distributed transaction records.',
      status: 'Implemented (federated/data)'
    },
    {
      title: '2. Local SGD + Proximal Regularizer',
      desc: 'Clients compute 5 local training epochs with FedProx proximal loss term (μ/2)||w - w^t||² preventing divergence.',
      status: 'Implemented (federated/client.py)'
    },
    {
      title: '3. Federated Server Aggregation',
      desc: 'Server averages client parameters over 30 global communication rounds to produce the converged global model.',
      status: 'Implemented (federated/server.py)'
    },
    {
      title: '4. Global Model Checkpoint',
      desc: 'Consolidated weights saved to models/fedprox_global_dnn.pth (421 input units, sequential PyTorch DNN).',
      status: 'Active Artifact'
    },
    {
      title: '5. Flask Forward Inference Engine',
      desc: 'REST API performs real-time feature alignment, standard scaling, and logit sigmoid evaluation for uploaded batches.',
      status: 'Active Backend Service'
    }
  ];

  const featureFamilies = [
    { name: 'Transaction Metadata', count: '4 features', fields: 'TransactionID, TransactionDT, TransactionAmt, ProductCD' },
    { name: 'Payment Card Details', count: '6 features', fields: 'card1 - card6 (Issuer, design code, card type, category)' },
    { name: 'Address & Distance', count: '4 features', fields: 'addr1, addr2, dist1, dist2' },
    { name: 'Email Domain Signatures', count: '2 features', fields: 'P_emaildomain, R_emaildomain' },
    { name: 'Identity & Device Info', count: '13 features', fields: 'DeviceType, DeviceInfo, id_01 to id_38' },
    { name: 'Behavior & Count Features', count: '14 features', fields: 'C1 - C14 (Counts of phone, email, address associations)' },
    { name: 'Timedelta History Features', count: '15 features', fields: 'D1 - D15 (Days since previous transaction activity)' },
    { name: 'Match Indicators', count: '9 features', fields: 'M1 - M9 (Name, address match flags)' },
    { name: 'Vesta Engineered V-Features', count: '339 features', fields: 'V1 - V339 (Aggregated behavioral patterns & signals)' }
  ];

  return (
    <div className="space-y-6">
      
      {/* Top Banner: Model Metadata */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-sm border border-slate-800">
        <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="flex items-center gap-2">
              <span className="p-2 bg-blue-600/30 text-blue-400 rounded-xl border border-blue-500/30">
                <Cpu size={22} />
              </span>
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-xl font-extrabold tracking-tight text-white">{modelName}</h2>
                  <span className="text-[10px] bg-blue-500/20 text-blue-400 font-bold px-2 py-0.5 rounded border border-blue-500/30">
                    PyTorch DNN
                  </span>
                </div>
                <p className="text-xs text-slate-400">
                  Federated Optimization with Proximal Regularization &bull; IEEE-CIS Benchmark
                </p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-4 text-xs font-semibold">
            <div className="bg-slate-800/80 px-4 py-2.5 rounded-xl border border-slate-700">
              <span className="text-slate-400 block text-[10px]">Active Status</span>
              <span className={`inline-flex items-center gap-1.5 font-bold ${backendConnected ? 'text-emerald-400' : 'text-rose-400'}`}>
                <span className={`w-2 h-2 rounded-full ${backendConnected ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`} />
                {backendConnected ? 'Ready for Inference' : 'Backend Disconnected'}
              </span>
            </div>

            <div className="bg-slate-800/80 px-4 py-2.5 rounded-xl border border-slate-700">
              <span className="text-slate-400 block text-[10px]">Checkpoint</span>
              <span className="text-slate-200 font-mono text-xs">fedprox_global_dnn.pth</span>
            </div>
          </div>
        </div>
      </div>

      {/* Verified Empirical Metrics */}
      <div className="space-y-3">
        <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider flex items-center gap-2">
          <Activity size={16} className="text-blue-600" />
          Verified Test & Validation Metrics
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {verifiedMetrics.map((item, idx) => (
            <div
              key={idx}
              className={`bg-white rounded-2xl p-5 border shadow-xs ${
                item.highlight ? 'border-emerald-300 ring-2 ring-emerald-500/10' : 'border-slate-200'
              }`}
            >
              <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block">
                {item.label}
              </span>
              <p className={`text-2xl font-black mt-1 font-mono ${
                item.highlight ? 'text-emerald-700' : 'text-slate-900'
              }`}>
                {item.value}
              </p>
              <p className="text-[11px] text-slate-400 mt-1">
                {item.note}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Conceptual System Architecture Flow */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <GitBranch size={18} className="text-blue-600" />
            Federated Training & Inference Pipeline Architecture
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Decoupling decentralized federated training from lightweight global inference
          </p>
        </div>

        {/* Note on Inference vs Training */}
        <div className="p-3.5 bg-blue-50 border border-blue-200 rounded-xl text-xs text-blue-900 flex items-start gap-2.5">
          <CheckCircle2 size={16} className="text-blue-600 shrink-0 mt-0.5" />
          <p className="leading-relaxed">
            <strong>Training vs Inference Separation:</strong> Client-side local training and FedProx server aggregation occurred during the federated training stage. When you upload a CSV to this dashboard, the Flask backend performs <strong>direct forward inference</strong> against the compiled global model checkpoint (<code className="bg-blue-100 text-blue-900 px-1 py-0.5 rounded font-mono">models/fedprox_global_dnn.pth</code>).
          </p>
        </div>

        {/* Steps Flow */}
        <div className="space-y-3 pt-2">
          {trainingArchitectureSteps.map((step, idx) => (
            <div
              key={idx}
              className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 p-4 rounded-xl bg-slate-50 border border-slate-200"
            >
              <div className="space-y-1">
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-900">{step.title}</span>
                  <span className="text-[10px] bg-slate-200/80 text-slate-700 font-semibold px-2 py-0.5 rounded">
                    {step.status}
                  </span>
                </div>
                <p className="text-xs text-slate-600 leading-relaxed max-w-2xl">
                  {step.desc}
                </p>
              </div>

              {idx < trainingArchitectureSteps.length - 1 && (
                <div className="hidden lg:flex items-center text-slate-400">
                  <ArrowRight size={18} />
                </div>
              )}
            </div>
          ))}
        </div>
      </div>

      {/* Feature Space Breakdown */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-4">
        <div>
          <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
            <Layers size={18} className="text-blue-600" />
            421-Feature Vector Representation (IEEE-CIS Benchmark)
          </h3>
          <p className="text-xs text-slate-500 mt-0.5">
            Composition of input features preprocessed through medians imputation and StandardScaler
          </p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {featureFamilies.map((fam, idx) => (
            <div key={idx} className="p-3.5 bg-slate-50 rounded-xl border border-slate-200 space-y-1">
              <div className="flex items-center justify-between">
                <span className="text-xs font-bold text-slate-900">{fam.name}</span>
                <span className="text-[10px] font-mono font-bold bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded">
                  {fam.count}
                </span>
              </div>
              <p className="text-[11px] text-slate-500 font-mono leading-tight">
                {fam.fields}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
