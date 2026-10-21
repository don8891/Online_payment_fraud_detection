import React from 'react';
import {
  Shield,
  Lock,
  Cpu,
  Layers,
  HelpCircle,
  FileText,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  BookOpen
} from 'lucide-react';

export default function AboutProjectView() {
  const vivaQuestions = [
    {
      q: "Why use Federated Learning instead of centralized machine learning?",
      a: "Financial institutions and payment processors cannot legally pool customer transaction records into a single central server due to strict privacy regulations (GDPR, PCI-DSS, RBI guidelines). Federated Learning enables multiple institutions to collaboratively train a global fraud detection model while keeping sensitive transaction data strictly on local premise."
    },
    {
      q: "What makes FedProx superior to FedAvg for payment fraud?",
      a: "Payment transaction distributions across banks are inherently Non-IID (different customer demographics, transaction amounts, and fraud ratios). Standard FedAvg often suffers from client weight drift when clients take multiple local gradient steps. FedProx introduces a proximal regularization term (μ/2)||w - w^t||² that restrains local updates from deviating too far from the global model, stabilizing convergence."
    },
    {
      q: "Why was the fraud decision threshold set to 0.85?",
      a: "In real-world fraud detection with severe class imbalance (only ~3.5% fraud in IEEE-CIS), raw probabilities tend to be calibrated to favor the majority legitimate class. Threshold optimization balances recall (catching true fraud) against precision (minimizing false positives that block innocent cardholders)."
    },
    {
      q: "What was the cause and resolution of the 0.508 constant probability bug?",
      a: "During the training phase, client datasets were already StandardScaled. An accidental secondary StandardScaler transformation in the client loader double-scaled inputs into an extreme ~30σ magnitude. The neural network learned saturated weights that produced near-zero logits (prob ≈ 0.508) during normal inference. Removing the redundant scaling and retraining across 30 rounds restored healthy probability variance and lifted validation ROC-AUC to 0.8319."
    }
  ];

  return (
    <div className="space-y-6">
      
      {/* Project Header Banner */}
      <div className="bg-slate-900 text-white rounded-2xl p-6 sm:p-8 border border-slate-800 shadow-sm space-y-4">
        <div className="flex items-center gap-2 text-blue-400 font-bold uppercase tracking-wider text-xs">
          <Shield size={18} />
          Final-Year Engineering Project &bull; Computer Science & Engineering
        </div>

        <h2 className="text-xl sm:text-2xl font-black text-white tracking-tight">
          Online Payment Fraud Detection System Using Federated Learning
        </h2>

        <p className="text-xs sm:text-sm text-slate-300 max-w-3xl leading-relaxed">
          A privacy-preserving machine learning system designed to detect online payment fraud across decentralized banking partitions. Powered by a Deep Neural Network trained with the <strong>FedProx</strong> federated optimization algorithm on the <strong>IEEE-CIS Fraud Detection</strong> benchmark.
        </p>

        <div className="flex flex-wrap items-center gap-3 pt-2 text-xs">
          <span className="bg-slate-800 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 font-medium">
            Framework: <strong>PyTorch + Flower FL</strong>
          </span>
          <span className="bg-slate-800 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 font-medium">
            Backend: <strong>Python Flask REST API</strong>
          </span>
          <span className="bg-slate-800 text-slate-300 px-3 py-1.5 rounded-lg border border-slate-700 font-medium">
            Frontend: <strong>React 18 + Tailwind CSS + Recharts</strong>
          </span>
        </div>
      </div>

      {/* Core Architectural Pillars */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs space-y-2">
          <div className="p-2.5 bg-blue-50 text-blue-600 rounded-xl w-fit">
            <Lock size={20} />
          </div>
          <h3 className="text-sm font-bold text-slate-900">Privacy-Preserving Training</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Raw financial records never leave client nodes. Each simulated banking client computes gradient updates locally, transmitting only mathematical model weights to the central aggregator.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs space-y-2">
          <div className="p-2.5 bg-emerald-50 text-emerald-600 rounded-xl w-fit">
            <Cpu size={20} />
          </div>
          <h3 className="text-sm font-bold text-slate-900">FedProx Heterogeneity Handling</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Addresses non-IID transaction frequency variations across simulated banking clients by introducing a proximal regularization term (<code className="text-emerald-700 font-mono">μ = 0.01</code>) that controls local gradient drift.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-5 border border-slate-200 shadow-xs space-y-2">
          <div className="p-2.5 bg-purple-50 text-purple-600 rounded-xl w-fit">
            <Layers size={20} />
          </div>
          <h3 className="text-sm font-bold text-slate-900">High-Dimensional Feature Space</h3>
          <p className="text-xs text-slate-500 leading-relaxed">
            Processes 421 continuous and categorical features including device fingerprints, card details, timedelta counts, and Vesta engineered behavioral interactions.
          </p>
        </div>
      </div>

      {/* Viva / Defense Q&A Section */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-xs space-y-4">
        <div className="flex items-center gap-2 pb-3 border-b border-slate-100">
          <BookOpen size={18} className="text-blue-600" />
          <div>
            <h3 className="text-base font-bold text-slate-900">Project Review & Viva Defense Questions</h3>
            <p className="text-xs text-slate-500">Key technical concepts and architecture rationales for project evaluation</p>
          </div>
        </div>

        <div className="space-y-3">
          {vivaQuestions.map((item, idx) => (
            <div key={idx} className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-1.5">
              <h4 className="text-xs font-bold text-slate-900 flex items-start gap-2">
                <span className="text-blue-600 font-mono">Q{idx + 1}:</span>
                {item.q}
              </h4>
              <p className="text-xs text-slate-600 leading-relaxed pl-6">
                {item.a}
              </p>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
