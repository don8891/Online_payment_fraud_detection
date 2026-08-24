import React from 'react';

/**
 * Semi-circular gauge that displays a 0–1 risk score with color-coded zones.
 * @param {number} score - 0.0 to 1.0
 */
export default function RiskGauge({ score = 0 }) {
  const pct = Math.min(Math.max(score, 0), 1);
  const percent = Math.round(pct * 100);

  // SVG arc math — half-circle, radius 70, center (80, 80)
  const R = 70;
  const cx = 80;
  const cy = 80;
  const startAngle = -180; // leftmost point
  const sweepDeg = 180 * pct;
  const toRad = (d) => (d * Math.PI) / 180;

  const x1 = cx + R * Math.cos(toRad(startAngle));
  const y1 = cy + R * Math.sin(toRad(startAngle));
  const x2 = cx + R * Math.cos(toRad(startAngle + sweepDeg));
  const y2 = cy + R * Math.sin(toRad(startAngle + sweepDeg));
  const largeArc = sweepDeg > 180 ? 1 : 0;

  const trackPath = `M ${cx - R} ${cy} A ${R} ${R} 0 0 1 ${cx + R} ${cy}`;
  const fillPath = pct > 0
    ? `M ${x1} ${y1} A ${R} ${R} 0 ${largeArc} 1 ${x2} ${y2}`
    : '';

  const color = pct < 0.2 ? '#10b981' : pct < 0.5 ? '#f59e0b' : '#ef4444';
  const label = pct < 0.2 ? 'LOW RISK' : pct < 0.5 ? 'MEDIUM RISK' : 'HIGH RISK';
  const labelColor = pct < 0.2 ? 'text-emerald-600' : pct < 0.5 ? 'text-amber-500' : 'text-red-600';

  return (
    <div className="flex flex-col items-center gap-1">
      <svg width="160" height="90" viewBox="0 0 160 90">
        {/* Background track */}
        <path d={trackPath} fill="none" stroke="#e2e8f0" strokeWidth="14" strokeLinecap="round" />
        {/* Colored fill */}
        {pct > 0 && (
          <path d={fillPath} fill="none" stroke={color} strokeWidth="14" strokeLinecap="round" />
        )}
        {/* Zone markers */}
        <text x="12" y="88" fontSize="9" fill="#94a3b8" textAnchor="middle">0</text>
        <text x="148" y="88" fontSize="9" fill="#94a3b8" textAnchor="middle">100</text>
      </svg>

      <div className="text-center -mt-2">
        <p className={`text-4xl font-black leading-none ${labelColor}`}>{percent}%</p>
        <p className={`text-xs font-bold mt-1 tracking-wider ${labelColor}`}>{label}</p>
      </div>
    </div>
  );
}
