import React from 'react';
import { ArrowDown, ArrowRight, Server, Database, Cpu, BarChart2, AlertTriangle, User } from 'lucide-react';

const steps = [
  { icon: User,         label: 'User / Analyst',           desc: 'Enters transaction data via React dashboard', color: 'bg-blue-100 text-blue-700 border-blue-200' },
  { icon: BarChart2,    label: 'React Dashboard',           desc: 'Frontend UI — validates & sends request',     color: 'bg-indigo-100 text-indigo-700 border-indigo-200' },
  { icon: Database,     label: 'Transaction Data',          desc: 'Structured feature vector (421 features)',     color: 'bg-slate-100 text-slate-700 border-slate-200' },
  { icon: Server,       label: 'Python / Flask API',        desc: 'REST endpoint — receives & preprocesses data',color: 'bg-violet-100 text-violet-700 border-violet-200' },
  { icon: Cpu,          label: 'LightGBM Model',            desc: 'Trained classifier — predicts fraud probability',color:'bg-orange-100 text-orange-700 border-orange-200'},
  { icon: AlertTriangle,label: 'Risk Threshold (0.20)',     desc: 'If P(fraud) ≥ threshold → Fraud',              color: 'bg-amber-100 text-amber-700 border-amber-200' },
  { icon: BarChart2,    label: 'SHAP Explanation (Future)', desc: 'Highlights top features driving the prediction',color:'bg-emerald-100 text-emerald-700 border-emerald-200'},
];

export default function SystemFlow() {
  return (
    <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
      <h3 className="text-sm font-bold text-slate-800 mb-1">System Architecture</h3>
      <p className="text-xs text-slate-500 mb-5">Planned data flow from UI to ML model and back</p>
      <div className="flex flex-col items-center gap-0">
        {steps.map((step, i) => {
          const Icon = step.icon;
          return (
            <React.Fragment key={i}>
              <div className={`flex items-start gap-3 w-full max-w-xs border rounded-lg px-4 py-3 ${step.color}`}>
                <Icon size={16} className="mt-0.5 shrink-0" />
                <div>
                  <p className="text-xs font-bold leading-tight">{step.label}</p>
                  <p className="text-xs opacity-70 mt-0.5">{step.desc}</p>
                </div>
              </div>
              {i < steps.length - 1 && (
                <ArrowDown size={14} className="text-slate-400 my-1" />
              )}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
}
