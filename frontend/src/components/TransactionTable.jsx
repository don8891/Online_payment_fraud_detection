import React, { useState, useMemo } from 'react';
import {
  Search,
  Filter,
  ArrowUpDown,
  ChevronLeft,
  ChevronRight,
  ShieldAlert,
  ShieldCheck,
  Eye,
  Download,
  FileSpreadsheet
} from 'lucide-react';

export default function TransactionTable({
  transactions = [],
  onSelectTransaction,
  onExport,
  modelInfo = {}
}) {
  const [searchTerm, setSearchTerm] = useState('');
  const [riskFilter, setRiskFilter] = useState('ALL');
  const [predFilter, setPredFilter] = useState('ALL');
  const [sortOrder, setSortOrder] = useState('DESC'); // 'DESC' | 'ASC'
  const [currentPage, setCurrentPage] = useState(1);
  const [pageSize, setPageSize] = useState(10);

  const modelName = modelInfo?.model || 'FedProx DNN';
  const threshold = modelInfo?.threshold !== undefined ? Number(modelInfo.threshold).toFixed(2) : '0.85';

  // Filter & Sort
  const filteredTransactions = useMemo(() => {
    if (!transactions || transactions.length === 0) return [];

    return transactions
      .filter((t) => {
        // Search filter
        const idMatch = t.transaction_id ? String(t.transaction_id).toLowerCase().includes(searchTerm.toLowerCase()) : false;
        const amtMatch = t.amount !== null && t.amount !== undefined ? String(t.amount).includes(searchTerm) : false;
        const matchSearch = !searchTerm || idMatch || amtMatch;

        // Risk filter
        const matchRisk = riskFilter === 'ALL' || t.risk_level === riskFilter;

        // Prediction filter
        const matchPred =
          predFilter === 'ALL' ||
          (predFilter === 'FRAUD' && t.prediction === 1) ||
          (predFilter === 'LEGIT' && t.prediction === 0);

        return matchSearch && matchRisk && matchPred;
      })
      .sort((a, b) => {
        const probA = Number(a.fraud_probability) || 0;
        const probB = Number(b.fraud_probability) || 0;
        return sortOrder === 'DESC' ? probB - probA : probA - probB;
      });
  }, [transactions, searchTerm, riskFilter, predFilter, sortOrder]);

  // Pagination
  const totalItems = filteredTransactions.length;
  const totalPages = Math.ceil(totalItems / pageSize) || 1;
  const safePage = Math.min(Math.max(1, currentPage), totalPages);

  const paginatedTransactions = useMemo(() => {
    const start = (safePage - 1) * pageSize;
    return filteredTransactions.slice(start, start + pageSize);
  }, [filteredTransactions, safePage, pageSize]);

  const handlePageChange = (newPage) => {
    if (newPage >= 1 && newPage <= totalPages) {
      setCurrentPage(newPage);
    }
  };

  const formatAmount = (amt) => {
    if (amt === null || amt === undefined || isNaN(amt)) return 'N/A';
    return new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(amt);
  };

  if (!transactions || transactions.length === 0) {
    return (
      <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center space-y-3">
        <FileSpreadsheet size={40} className="text-slate-300 mx-auto" />
        <h3 className="text-base font-bold text-slate-800">No Evaluated Transactions</h3>
        <p className="text-xs text-slate-500 max-w-md mx-auto">
          Upload a transaction batch CSV above to display the evaluated transaction ledger with FedProx risk scores.
        </p>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 shadow-xs overflow-hidden space-y-4 p-6">
      
      {/* Table Header & Controls */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-100">
        <div>
          <h2 className="text-base sm:text-lg font-bold text-slate-900 tracking-tight flex items-center gap-2">
            <ShieldAlert size={20} className="text-blue-600" />
            Transaction Evaluation Ledger
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Showing {totalItems.toLocaleString()} of {transactions.length.toLocaleString()} records evaluated by {modelName} (Cutoff ≥ {threshold})
          </p>
        </div>

        {onExport && (
          <button
            onClick={onExport}
            type="button"
            className="inline-flex items-center gap-2 px-4 py-2 text-xs font-bold text-white bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 rounded-xl shadow-xs transition-colors self-start lg:self-auto cursor-pointer"
          >
            <Download size={15} />
            Export Results (CSV)
          </button>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-4 gap-3 bg-slate-50/80 p-3 rounded-xl border border-slate-200">
        
        {/* Search */}
        <div className="relative flex items-center">
          <Search size={15} className="absolute left-3 text-slate-400 pointer-events-none" />
          <input
            type="text"
            placeholder="Search ID or Amount..."
            value={searchTerm}
            onChange={(e) => { setSearchTerm(e.target.value); setCurrentPage(1); }}
            className="w-full pl-9 pr-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 font-medium text-slate-800"
          />
        </div>

        {/* Risk Level Filter */}
        <div className="flex items-center gap-2">
          <Filter size={14} className="text-slate-400 shrink-0" />
          <select
            value={riskFilter}
            onChange={(e) => { setRiskFilter(e.target.value); setCurrentPage(1); }}
            className="w-full px-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700 font-semibold cursor-pointer"
          >
            <option value="ALL">All Risk Levels</option>
            <option value="HIGH">High Risk (≥0.90)</option>
            <option value="MEDIUM">Medium Risk (0.50-0.89)</option>
            <option value="LOW">Low Risk (&lt;0.50)</option>
          </select>
        </div>

        {/* Prediction Filter */}
        <div className="flex items-center gap-2">
          <select
            value={predFilter}
            onChange={(e) => { setPredFilter(e.target.value); setCurrentPage(1); }}
            className="w-full px-3 py-1.5 text-xs bg-white border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700 font-semibold cursor-pointer"
          >
            <option value="ALL">All Predictions</option>
            <option value="FRAUD">Fraud Flagged (≥ {threshold})</option>
            <option value="LEGIT">Legitimate (&lt; {threshold})</option>
          </select>
        </div>

        {/* Sort Order Toggle */}
        <div className="flex items-center gap-2">
          <button
            onClick={() => setSortOrder(prev => prev === 'DESC' ? 'ASC' : 'DESC')}
            type="button"
            className="w-full flex items-center justify-center gap-2 px-3 py-1.5 text-xs font-semibold bg-white border border-slate-300 hover:bg-slate-100 rounded-lg text-slate-700 transition-colors cursor-pointer"
          >
            <ArrowUpDown size={14} className="text-blue-600" />
            Prob: {sortOrder === 'DESC' ? 'High → Low' : 'Low → High'}
          </button>
        </div>

      </div>

      {/* Results Table */}
      <div className="overflow-x-auto border border-slate-200 rounded-xl">
        <table className="w-full text-left text-xs">
          <thead className="bg-slate-100 text-slate-700 uppercase font-bold text-[11px] tracking-wider border-b border-slate-200">
            <tr>
              <th className="py-3 px-4">Transaction ID</th>
              <th className="py-3 px-4">Amount</th>
              <th className="py-3 px-4">Fraud Probability</th>
              <th className="py-3 px-4">Risk Level</th>
              <th className="py-3 px-4">Classification</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4 text-center">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-200">
            {paginatedTransactions.length === 0 ? (
              <tr>
                <td colSpan={7} className="py-8 text-center text-slate-500">
                  No transactions match the selected filter or search criteria.
                </td>
              </tr>
            ) : (
              paginatedTransactions.map((txn, idx) => {
                const isFraud = txn.prediction === 1;
                const prob = Number(txn.fraud_probability) || 0;
                const probPct = (prob * 100).toFixed(1);

                return (
                  <tr
                    key={txn.transaction_id || `txn-${idx}`}
                    onClick={() => onSelectTransaction(txn)}
                    className={`hover:bg-blue-50/50 cursor-pointer transition-colors ${
                      isFraud ? 'bg-rose-50/30' : ''
                    }`}
                  >
                    {/* Transaction ID */}
                    <td className="py-3 px-4 font-mono font-bold text-slate-900">
                      {txn.transaction_id || `TXN${String(idx + 1).padStart(4, '0')}`}
                    </td>

                    {/* Amount */}
                    <td className="py-3 px-4 font-semibold text-slate-800">
                      {formatAmount(txn.amount)}
                    </td>

                    {/* Probability */}
                    <td className="py-3 px-4">
                      <div className="flex items-center gap-2">
                        <div className="w-16 bg-slate-200 rounded-full h-2 overflow-hidden shrink-0">
                          <div
                            className={`h-full ${
                              prob >= 0.90
                                ? 'bg-rose-600'
                                : prob >= 0.50
                                ? 'bg-amber-500'
                                : 'bg-emerald-500'
                            }`}
                            style={{ width: `${Math.min(100, Math.max(4, prob * 100))}%` }}
                          />
                        </div>
                        <span className="font-mono font-bold text-slate-900">
                          {probPct}% <span className="text-[11px] font-normal text-slate-500">({prob.toFixed(4)})</span>
                        </span>
                      </div>
                    </td>

                    {/* Risk Level Badge */}
                    <td className="py-3 px-4">
                      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase border ${
                        txn.risk_level === 'HIGH'
                          ? 'bg-rose-100 text-rose-800 border-rose-300'
                          : txn.risk_level === 'MEDIUM'
                          ? 'bg-amber-100 text-amber-800 border-amber-300'
                          : 'bg-emerald-100 text-emerald-800 border-emerald-300'
                      }`}>
                        {txn.risk_level} RISK
                      </span>
                    </td>

                    {/* Classification */}
                    <td className="py-3 px-4">
                      <span className={`font-bold flex items-center gap-1.5 ${
                        isFraud ? 'text-rose-600' : 'text-emerald-700'
                      }`}>
                        {isFraud ? (
                          <>
                            <ShieldAlert size={14} /> Fraud
                          </>
                        ) : (
                          <>
                            <ShieldCheck size={14} /> Legitimate
                          </>
                        )}
                      </span>
                    </td>

                    {/* Status */}
                    <td className="py-3 px-4">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                        isFraud ? 'bg-rose-600 text-white' : 'bg-slate-200 text-slate-700'
                      }`}>
                        {isFraud ? 'Flagged' : 'Safe'}
                      </span>
                    </td>

                    {/* Action */}
                    <td className="py-3 px-4 text-center">
                      <button
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          onSelectTransaction(txn);
                        }}
                        className="inline-flex items-center gap-1 text-xs font-semibold text-blue-600 hover:text-blue-800 hover:underline cursor-pointer"
                      >
                        <Eye size={13} /> Details
                      </button>
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>

      {/* Pagination Bar */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs text-slate-500 pt-2">
        <div className="flex items-center gap-3">
          <span>
            Page <strong className="text-slate-900">{safePage}</strong> of <strong className="text-slate-900">{totalPages}</strong>
          </span>
          <select
            value={pageSize}
            onChange={(e) => { setPageSize(Number(e.target.value)); setCurrentPage(1); }}
            className="px-2 py-1 bg-white border border-slate-300 rounded text-xs text-slate-700 cursor-pointer"
          >
            <option value={10}>10 per page</option>
            <option value={25}>25 per page</option>
            <option value={50}>50 per page</option>
            <option value={100}>100 per page</option>
          </select>
        </div>

        <div className="flex items-center gap-1">
          <button
            onClick={() => handlePageChange(safePage - 1)}
            disabled={safePage <= 1}
            className="p-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-40 transition-colors cursor-pointer"
            title="Previous page"
          >
            <ChevronLeft size={16} />
          </button>
          <button
            onClick={() => handlePageChange(safePage + 1)}
            disabled={safePage >= totalPages}
            className="p-1.5 rounded-lg border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-40 transition-colors cursor-pointer"
            title="Next page"
          >
            <ChevronRight size={16} />
          </button>
        </div>
      </div>

    </div>
  );
}
