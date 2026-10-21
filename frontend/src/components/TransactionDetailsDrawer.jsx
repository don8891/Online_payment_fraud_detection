import React from 'react';
import {
  X,
  ShieldAlert,
  ShieldCheck,
  HelpCircle,
  Layers,
  CreditCard,
  Laptop,
  Mail,
  MapPin,
  Activity,
  Sliders
} from 'lucide-react';

export default function TransactionDetailsDrawer({
  transaction,
  onClose,
  modelInfo = {}
}) {
  if (!transaction) return null;

  const {
    transaction_id,
    amount,
    fraud_probability = 0,
    prediction = 0,
    risk_level = 'LOW',
    raw_features = {},
    explanation = []
  } = transaction;

  const threshold = modelInfo?.threshold !== undefined ? Number(modelInfo.threshold) : 0.85;
  const isFraud = prediction === 1;
  const probNum = Number(fraud_probability) || 0;
  const probPct = (probNum * 100).toFixed(1);

  // Group IEEE-CIS raw features logically
  const featureGroups = {
    "Transaction Metadata": ["TransactionID", "TransactionDT", "TransactionAmt", "ProductCD"],
    "Payment Card Details": ["card1", "card2", "card3", "card4", "card5", "card6"],
    "Email Domains": ["P_emaildomain", "R_emaildomain"],
    "Location & Region": ["addr1", "addr2", "dist1", "dist2"],
    "Device & Environment": ["DeviceType", "DeviceInfo", "id_30", "id_31", "id_33"],
    "Verification & Match Indicators": ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9"],
  };

  const categorizedKeys = new Set(Object.values(featureGroups).flat());
  const otherKeys = Object.keys(raw_features).filter(k => !categorizedKeys.has(k));

  const formatAmount = (amt) => {
    if (amt === null || amt === undefined || isNaN(amt)) return 'N/A';
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(amt);
  };

  return (
    <div className="fixed inset-0 z-50 overflow-hidden bg-slate-950/60 backdrop-blur-xs flex justify-end transition-opacity">
      <div className="w-full max-w-lg bg-white h-full shadow-2xl flex flex-col overflow-hidden border-l border-slate-200">
        
        {/* Drawer Header */}
        <div className="bg-slate-900 text-white p-5 flex items-center justify-between border-b border-slate-800">
          <div>
            <span className="text-[10px] font-mono uppercase tracking-widest text-slate-400">
              Transaction Details & Features
            </span>
            <h3 className="text-lg font-bold text-slate-100 flex items-center gap-2 mt-0.5 font-mono">
              {transaction_id}
            </h3>
          </div>
          <button
            onClick={onClose}
            type="button"
            className="p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors cursor-pointer"
            title="Close drawer"
          >
            <X size={20} />
          </button>
        </div>

        {/* Scrollable Body */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          
          {/* Risk Prediction Summary Card */}
          <div className={`p-5 rounded-2xl border space-y-4 ${
            isFraud ? 'bg-rose-50/70 border-rose-200' : 'bg-emerald-50/70 border-emerald-200'
          }`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2.5">
                {isFraud ? (
                  <ShieldAlert size={26} className="text-rose-600 shrink-0" />
                ) : (
                  <ShieldCheck size={26} className="text-emerald-600 shrink-0" />
                )}
                <div>
                  <h4 className={`text-base font-extrabold ${isFraud ? 'text-rose-900' : 'text-emerald-900'}`}>
                    {isFraud ? 'Flagged Fraudulent' : 'Classified Legitimate'}
                  </h4>
                  <p className="text-xs text-slate-500">
                    Decision cutoff: ≥ {threshold.toFixed(2)}
                  </p>
                </div>
              </div>

              <span className={`px-3 py-1 rounded-full text-xs font-black uppercase border ${
                risk_level === 'HIGH'
                  ? 'bg-rose-600 text-white border-rose-700'
                  : risk_level === 'MEDIUM'
                  ? 'bg-amber-500 text-white border-amber-600'
                  : 'bg-emerald-600 text-white border-emerald-700'
              }`}>
                {risk_level} RISK
              </span>
            </div>

            {/* Probability Gauge Bar */}
            <div className="space-y-1.5">
              <div className="flex justify-between text-xs font-semibold text-slate-700">
                <span>Fraud Probability Score:</span>
                <strong className={`font-mono ${isFraud ? 'text-rose-600' : 'text-emerald-700'}`}>
                  {probPct}% ({probNum.toFixed(4)})
                </strong>
              </div>
              <div className="w-full bg-slate-200 rounded-full h-2.5 overflow-hidden">
                <div
                  className={`h-full ${
                    probNum >= 0.90 ? 'bg-rose-600' : probNum >= 0.50 ? 'bg-amber-500' : 'bg-emerald-500'
                  }`}
                  style={{ width: `${Math.min(100, Math.max(4, probNum * 100))}%` }}
                />
              </div>
            </div>

            {/* Amount & Classification */}
            <div className="pt-2 border-t border-slate-200/70 flex justify-between items-center text-xs">
              <span className="text-slate-600 font-medium">Transaction Amount:</span>
              <span className="text-sm font-bold text-slate-900 font-mono">
                {formatAmount(amount)}
              </span>
            </div>
          </div>

          {/* Explainability Section */}
          <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 space-y-2">
            <h4 className="text-xs font-bold text-slate-800 uppercase tracking-wider flex items-center gap-1.5">
              <HelpCircle size={15} className="text-blue-600" />
              Model Feature Explanation
            </h4>
            
            {explanation && explanation.length > 0 ? (
              <div className="space-y-2.5 pt-1">
                <p className="text-xs text-slate-600 leading-relaxed">
                  Top input attributes influencing the FedProx DNN prediction score:
                </p>

                {explanation.map((item, index) => {
                  const positive = item.shap_value > 0;
                  return (
                    <div
                      key={`${item.feature}-${index}`}
                      className="bg-white p-3 rounded-lg border border-slate-200"
                    >
                      <div className="flex items-center justify-between gap-3">
                        <span className="text-xs font-semibold text-slate-800 font-mono">
                          {item.feature}
                        </span>
                        <span className={`text-[10px] font-bold rounded-full px-2 py-0.5 ${
                          positive ? 'bg-rose-100 text-rose-700' : 'bg-emerald-100 text-emerald-700'
                        }`}>
                          {positive ? 'Increases Risk' : 'Reduces Risk'}
                        </span>
                      </div>
                      <div className="mt-1 flex items-center justify-between text-xs text-slate-500">
                        <span>Contribution:</span>
                        <strong className="font-mono text-slate-700">
                          {Number(item.shap_value).toFixed(6)}
                        </strong>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="text-xs text-slate-500 leading-relaxed bg-white p-3 rounded-lg border border-slate-200/80">
                Evaluation performed using FedProx 421-feature feedforward inference. The global DNN predicts risk from the full composite feature vector.
              </p>
            )}
          </div>

          {/* Categorized Raw Feature Ledger */}
          <div className="space-y-4">
            <h4 className="text-xs font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2 pb-2 border-b border-slate-200">
              <Layers size={16} className="text-blue-600" />
              Transaction Features ({Object.keys(raw_features).length} fields detected)
            </h4>

            {Object.entries(featureGroups).map(([groupTitle, fields]) => {
              const presentFields = fields.filter(f => raw_features.hasOwnProperty(f));
              if (presentFields.length === 0) return null;

              return (
                <div key={groupTitle} className="space-y-1.5">
                  <h5 className="text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
                    {groupTitle.includes("Card") && <CreditCard size={12} className="text-slate-400" />}
                    {groupTitle.includes("Device") && <Laptop size={12} className="text-slate-400" />}
                    {groupTitle.includes("Email") && <Mail size={12} className="text-slate-400" />}
                    {groupTitle.includes("Location") && <MapPin size={12} className="text-slate-400" />}
                    {groupTitle}
                  </h5>
                  <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-xl border border-slate-200">
                    {presentFields.map(key => (
                      <div key={key} className="overflow-hidden">
                        <span className="text-[10px] text-slate-400 block font-mono truncate">{key}</span>
                        <strong className="text-slate-800 font-mono truncate block">{String(raw_features[key])}</strong>
                      </div>
                    ))}
                  </div>
                </div>
              );
            })}

            {/* Other Attributes */}
            {otherKeys.length > 0 && (
              <div className="space-y-1.5">
                <h5 className="text-[11px] font-bold text-slate-600 uppercase tracking-wider">
                  Remaining Attributes ({otherKeys.length})
                </h5>
                <div className="grid grid-cols-2 gap-2 text-xs bg-slate-50 p-3 rounded-xl border border-slate-200 max-h-48 overflow-y-auto">
                  {otherKeys.map(key => (
                    <div key={key} className="overflow-hidden">
                      <span className="text-[10px] text-slate-400 block font-mono truncate">{key}</span>
                      <strong className="text-slate-800 font-mono truncate block">{String(raw_features[key])}</strong>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

        </div>

        {/* Footer */}
        <div className="p-4 bg-slate-50 border-t border-slate-200">
          <button
            onClick={onClose}
            type="button"
            className="w-full py-2.5 bg-slate-800 hover:bg-slate-900 text-white text-xs font-bold rounded-xl transition-colors cursor-pointer"
          >
            Close Details Panel
          </button>
        </div>

      </div>
    </div>
  );
}
