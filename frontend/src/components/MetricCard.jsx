import React from 'react';

export default function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  iconBg = 'bg-blue-100',
  iconColor = 'text-blue-600',
  valueColor = 'text-slate-900',
  badge,
  badgeColor = 'bg-slate-100 text-slate-600',
}) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between gap-3">
        <div className="flex-1 min-w-0">
          <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider truncate">{title}</p>
          <p className={`text-2xl font-bold mt-1 leading-tight ${valueColor}`}>{value}</p>
          {subtitle && <p className="text-xs text-slate-400 mt-1 leading-snug">{subtitle}</p>}
        </div>
        {Icon && (
          <div className={`flex items-center justify-center w-10 h-10 rounded-lg shrink-0 ${iconBg}`}>
            <Icon size={20} className={iconColor} />
          </div>
        )}
      </div>
      {badge && (
        <div className="mt-3 pt-3 border-t border-slate-100">
          <span className={`inline-flex items-center text-xs font-medium px-2 py-0.5 rounded-full ${badgeColor}`}>
            {badge}
          </span>
        </div>
      )}
    </div>
  );
}
