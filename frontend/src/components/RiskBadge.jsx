import React from 'react';

const RISK_CONFIGS = {
  'LOW':        { label: 'LOW RISK',   classes: 'bg-emerald-50 text-emerald-700 border border-emerald-200' },
  'MEDIUM':     { label: 'MEDIUM RISK',classes: 'bg-amber-50 text-amber-700 border border-amber-200' },
  'HIGH':       { label: 'HIGH RISK',  classes: 'bg-red-50 text-red-700 border border-red-200' },
  'FRAUD':      { label: 'FRAUD',      classes: 'bg-red-600 text-white' },
  'LEGITIMATE': { label: 'LEGITIMATE', classes: 'bg-emerald-600 text-white' },
  'BLOCKED':    { label: 'BLOCKED',    classes: 'bg-red-100 text-red-700 border border-red-300' },
  'SAFE':       { label: 'SAFE',       classes: 'bg-emerald-100 text-emerald-700 border border-emerald-300' },
  'REVIEW':     { label: 'UNDER REVIEW', classes: 'bg-amber-100 text-amber-700 border border-amber-300' },
};

/**
 * @param {'LOW'|'MEDIUM'|'HIGH'|'FRAUD'|'LEGITIMATE'|'BLOCKED'|'SAFE'|'REVIEW'} type
 */
export default function RiskBadge({ type, className = '' }) {
  const key = (type || '').toUpperCase().replace(/\s+/g, '');
  const config = RISK_CONFIGS[key] || { label: type, classes: 'bg-slate-100 text-slate-600' };

  return (
    <span
      className={`
        inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold tracking-wide
        ${config.classes} ${className}
      `}
    >
      {config.label}
    </span>
  );
}

/** Derive risk level string from a 0-1 score */
export function getRiskLevel(score) {
  if (score < 0.20) return 'LOW';
  if (score < 0.50) return 'MEDIUM';
  return 'HIGH';
}
