import React, { useState, useMemo } from 'react';
import { Search, ChevronLeft, ChevronRight, Filter } from 'lucide-react';
import TransactionTable from '../components/TransactionTable';
import { MOCK_TRANSACTIONS } from '../data/mockData';
import { getRiskLevel } from '../components/RiskBadge';

const PAGE_SIZE = 8;

export default function Transactions({ searchQuery = '' }) {
  const [search, setSearch]         = useState(searchQuery);
  const [filterRisk, setFilterRisk] = useState('All');
  const [filterPred, setFilterPred] = useState('All');
  const [filterPay,  setFilterPay]  = useState('All');
  const [filterProd, setFilterProd] = useState('All');
  const [page, setPage]             = useState(1);

  const filtered = useMemo(() => {
    return MOCK_TRANSACTIONS.filter((tx) => {
      const q = search.toLowerCase();
      if (q && !tx.id.toLowerCase().includes(q) && !tx.emailDomain.toLowerCase().includes(q)) return false;
      if (filterRisk !== 'All' && getRiskLevel(tx.riskScore) !== filterRisk) return false;
      if (filterPred !== 'All' && tx.prediction !== filterPred) return false;
      if (filterPay  !== 'All' && tx.paymentType !== filterPay)  return false;
      if (filterProd !== 'All' && tx.product !== filterProd)     return false;
      return true;
    });
  }, [search, filterRisk, filterPred, filterPay, filterProd]);

  const totalPages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const paginated  = filtered.slice((page - 1) * PAGE_SIZE, page * PAGE_SIZE);

  const reset = () => setPage(1);

  const selectClass = "px-3 py-1.5 text-xs bg-white border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 text-slate-700 font-medium";

  return (
    <div className="p-6 space-y-5 animate-fade-in">
      <div>
        <h2 className="text-xl font-bold text-slate-900">Transactions</h2>
        <p className="text-sm text-slate-500 mt-0.5">Full transaction ledger — search, filter and paginate</p>
      </div>

      {/* Filters */}
      <div className="bg-white border border-slate-200 rounded-xl p-4 shadow-sm flex flex-wrap gap-3 items-center">
        <div className="relative flex items-center">
          <Search size={14} className="absolute left-3 text-slate-400 pointer-events-none" />
          <input
            type="text"
            placeholder="Search ID or domain..."
            value={search}
            onChange={(e) => { setSearch(e.target.value); reset(); }}
            className="pl-8 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 w-44 text-slate-700"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter size={13} className="text-slate-400" />
          <span className="text-xs text-slate-500 font-medium">Filters:</span>
        </div>

        <select value={filterRisk} onChange={e => { setFilterRisk(e.target.value); reset(); }} className={selectClass}>
          <option value="All">All Risk Levels</option>
          <option value="LOW">Low Risk</option>
          <option value="MEDIUM">Medium Risk</option>
          <option value="HIGH">High Risk</option>
        </select>

        <select value={filterPred} onChange={e => { setFilterPred(e.target.value); reset(); }} className={selectClass}>
          <option value="All">All Predictions</option>
          <option value="Legitimate">Legitimate</option>
          <option value="Fraud">Fraud</option>
        </select>

        <select value={filterPay} onChange={e => { setFilterPay(e.target.value); reset(); }} className={selectClass}>
          <option value="All">All Payment Types</option>
          <option value="Debit">Debit</option>
          <option value="Credit">Credit</option>
        </select>

        <select value={filterProd} onChange={e => { setFilterProd(e.target.value); reset(); }} className={selectClass}>
          <option value="All">All Products</option>
          {['W','C','H','R','S'].map(p => <option key={p}>{p}</option>)}
        </select>

        {/* Result count */}
        <span className="ml-auto text-xs text-slate-500">
          {filtered.length} of {MOCK_TRANSACTIONS.length} transactions
        </span>
      </div>

      {/* Table */}
      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
        <TransactionTable transactions={paginated} />
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between">
          <p className="text-xs text-slate-500">
            Page {page} of {totalPages} · showing {paginated.length} results
          </p>
          <div className="flex items-center gap-1">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="p-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft size={15} />
            </button>
            {Array.from({ length: totalPages }, (_, i) => i + 1).map((pg) => (
              <button
                key={pg}
                onClick={() => setPage(pg)}
                className={`w-7 h-7 rounded-lg text-xs font-semibold transition-colors ${
                  pg === page
                    ? 'bg-slate-900 text-white'
                    : 'border border-slate-200 text-slate-600 hover:bg-slate-50'
                }`}
              >
                {pg}
              </button>
            ))}
            <button
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="p-1.5 rounded-lg border border-slate-200 text-slate-600 hover:bg-slate-50 disabled:opacity-40 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronRight size={15} />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
