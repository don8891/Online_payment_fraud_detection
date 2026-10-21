import React, { useState, useEffect, useMemo } from 'react';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import FileUploadSection from './components/FileUploadSection';
import AnalysisSummary from './components/AnalysisSummary';
import VisualSummary from './components/VisualSummary';
import TransactionTable from './components/TransactionTable';
import TransactionDetailsDrawer from './components/TransactionDetailsDrawer';
import EmptyState from './components/EmptyState';
import FraudAlertsView from './components/FraudAlertsView';
import { exportTransactionsToCsv } from './utils/exportCsv';
import { ArrowRight, ShieldAlert, FileSpreadsheet, Eye } from 'lucide-react';

const API_BASE_URL = 'http://localhost:5000';

export default function App() {
  // Navigation State
  const [activeNav, setActiveNav] = useState('overview');
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  // Backend Connection & Model Metadata State
  const [backendConnected, setBackendConnected] = useState(false);
  const [checkingBackend, setCheckingBackend] = useState(false);
  const [modelInfo, setModelInfo] = useState({
    model: 'FedProx DNN',
    num_features: 421,
    threshold: 0.85
  });

  // File Upload State
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileMeta, setFileMeta] = useState({ rowCount: 0 });

  // Machine Learning Analysis State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Transaction Inspection Drawer State
  const [selectedTransaction, setSelectedTransaction] = useState(null);

  // Check Backend Health & Fetch Model Metadata
  const checkHealth = async () => {
    setCheckingBackend(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/health`, { method: 'GET' });
      if (res.ok) {
        const data = await res.json();
        setBackendConnected(true);
        if (data.model || data.num_features || data.threshold !== undefined) {
          setModelInfo(prev => ({
            ...prev,
            model: data.model || prev.model,
            num_features: data.num_features || prev.num_features,
            threshold: data.threshold !== undefined ? data.threshold : prev.threshold
          }));
        }
      } else {
        setBackendConnected(false);
      }
    } catch (err) {
      setBackendConnected(false);
    } finally {
      setCheckingBackend(false);
    }
  };

  useEffect(() => {
    checkHealth();
    // Poll backend health every 15 seconds
    const interval = setInterval(checkHealth, 15000);
    return () => clearInterval(interval);
  }, []);

  // Handle File Selection
  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setAnalysisResult(null);
    setErrorMessage(null);
    setFileMeta({ rowCount: 0 });

    // Estimate line count from initial byte sample
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split('\n').filter(l => l.trim().length > 0);
      if (lines.length > 1) {
        const sampleBytes = e.target.loaded;
        const totalBytes = file.size;
        const avgBytesPerLine = sampleBytes / lines.length;
        const estRows = Math.max(1, Math.round(totalBytes / avgBytesPerLine) - 1);
        setFileMeta({ rowCount: estRows });
      }
    };
    reader.readAsText(file.slice(0, 64 * 1024)); // Read first 64KB
  };

  // Download Sample CSV
  const handleDownloadSample = () => {
    window.open(`${API_BASE_URL}/api/sample-csv`, '_blank');
  };

  // Run ML Prediction via Flask API
  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setErrorMessage(null);
    setAnalysisStep(0);

    const timer1 = setTimeout(() => setAnalysisStep(1), 500);
    const timer2 = setTimeout(() => setAnalysisStep(2), 1100);

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await fetch(`${API_BASE_URL}/api/predict`, {
        method: 'POST',
        body: formData,
      });

      setAnalysisStep(3);
      const data = await response.json();

      if (response.ok && data.success) {
        setAnalysisResult(data);
        setBackendConnected(true);
        if (data.model_info) {
          setModelInfo(prev => ({
            ...prev,
            ...data.model_info
          }));
        }
      } else {
        setErrorMessage(data.error || 'Prediction failed. Please inspect the uploaded CSV file format.');
      }
    } catch (err) {
      setErrorMessage('Unable to connect to Flask backend. Please verify that backend server is running on http://localhost:5000.');
      setBackendConnected(false);
    } finally {
      clearTimeout(timer1);
      clearTimeout(timer2);
      setIsAnalyzing(false);
    }
  };

  // Export Results to CSV
  const handleExportResults = () => {
    if (analysisResult?.transactions) {
      const filename = `fraud_analysis_${selectedFile?.name?.replace('.csv', '') || 'results'}.csv`;
      exportTransactionsToCsv(analysisResult.transactions, filename);
    }
  };

  // Calculate Fraud Alerts Count
  const fraudAlertCount = useMemo(() => {
    if (!analysisResult?.transactions) return 0;
    return analysisResult.transactions.filter(
      t => t.prediction === 1 || Number(t.fraud_probability) >= (modelInfo?.threshold || 0.85)
    ).length;
  }, [analysisResult, modelInfo]);

  // Top 5 recent transactions for quick overview preview
  const previewTransactions = useMemo(() => {
    if (!analysisResult?.transactions) return [];
    return analysisResult.transactions.slice(0, 6);
  }, [analysisResult]);

  return (
    <div className="min-h-screen bg-slate-100 flex font-sans text-slate-900 antialiased selection:bg-blue-600 selection:text-white">
      
      {/* Sidebar Navigation */}
      <Sidebar
        activeNav={activeNav}
        onNavigate={setActiveNav}
        collapsed={sidebarCollapsed}
        onToggleCollapse={() => setSidebarCollapsed(prev => !prev)}
        mobileOpen={mobileMenuOpen}
        onCloseMobile={() => setMobileMenuOpen(false)}
        fraudAlertCount={fraudAlertCount}
        backendConnected={backendConnected}
        modelInfo={modelInfo}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto min-h-screen">
        
        {/* Top Header */}
        <Header
          activeNav={activeNav}
          backendConnected={backendConnected}
          checkingBackend={checkingBackend}
          onRefreshHealth={checkHealth}
          sidebarCollapsed={sidebarCollapsed}
          onToggleSidebar={() => setSidebarCollapsed(prev => !prev)}
          onOpenMobileMenu={() => setMobileMenuOpen(true)}
          activeFileName={selectedFile?.name}
          totalTransactions={analysisResult?.summary?.total_transactions}
          modelInfo={modelInfo}
        />

        {/* Dynamic View Container */}
        <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
          
          {/* TAB 1: OVERVIEW */}
          {activeNav === 'overview' && (
            <div className="space-y-6 animate-fade-in">
              
              {/* Primary Action: CSV File Upload Section */}
              <section id="upload-section">
                <FileUploadSection
                  selectedFile={selectedFile}
                  fileMeta={fileMeta}
                  onFileSelect={handleFileSelect}
                  onAnalyze={handleAnalyze}
                  onDownloadSample={handleDownloadSample}
                  isAnalyzing={isAnalyzing}
                  analysisStep={analysisStep}
                  errorMessage={errorMessage}
                  modelInfo={modelInfo}
                />
              </section>

              {/* 4 KPI Summary Cards */}
              <section id="summary-section">
                <AnalysisSummary
                  summary={analysisResult?.summary || {
                    total_transactions: 0,
                    fraudulent_transactions: 0,
                    legitimate_transactions: 0,
                    fraud_rate: 0.0
                  }}
                  modelInfo={modelInfo}
                />
              </section>

              {/* Visual Analytics Charts (When analyzed) */}
              {analysisResult?.transactions ? (
                <section id="visuals-section">
                  <VisualSummary
                    transactions={analysisResult.transactions}
                    summary={analysisResult.summary}
                    modelInfo={modelInfo}
                  />
                </section>
              ) : null}

              {/* Evaluated Transactions Preview (When analyzed) */}
              {analysisResult?.transactions ? (
                <section id="preview-section" className="bg-white rounded-2xl border border-slate-200 shadow-xs p-6 space-y-4">
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 pb-3 border-b border-slate-100">
                    <div>
                      <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                        <FileSpreadsheet size={18} className="text-blue-600" />
                        Evaluated Batch Preview (First 6 Records)
                      </h3>
                      <p className="text-xs text-slate-500 mt-0.5">
                        Click any row or switch to the Transaction Analysis tab to search all {analysisResult.transactions.length.toLocaleString()} records
                      </p>
                    </div>

                    <button
                      onClick={() => setActiveNav('analysis')}
                      type="button"
                      className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-600 hover:text-blue-800 self-start sm:self-auto cursor-pointer"
                    >
                      View Full Analysis Ledger
                      <ArrowRight size={14} />
                    </button>
                  </div>

                  {/* Compact Preview Table */}
                  <div className="overflow-x-auto border border-slate-200 rounded-xl">
                    <table className="w-full text-left text-xs">
                      <thead className="bg-slate-100 text-slate-700 uppercase font-bold text-[10px] tracking-wider border-b border-slate-200">
                        <tr>
                          <th className="py-2.5 px-3">Transaction ID</th>
                          <th className="py-2.5 px-3">Amount</th>
                          <th className="py-2.5 px-3">Fraud Prob</th>
                          <th className="py-2.5 px-3">Risk Level</th>
                          <th className="py-2.5 px-3">Status</th>
                          <th className="py-2.5 px-3 text-center">Inspect</th>
                        </tr>
                      </thead>
                      <tbody className="divide-y divide-slate-200">
                        {previewTransactions.map((t, idx) => {
                          const isFraud = t.prediction === 1;
                          const prob = Number(t.fraud_probability) || 0;
                          return (
                            <tr
                              key={t.transaction_id || idx}
                              onClick={() => setSelectedTransaction(t)}
                              className={`hover:bg-blue-50/50 cursor-pointer transition-colors ${
                                isFraud ? 'bg-rose-50/30' : ''
                              }`}
                            >
                              <td className="py-2.5 px-3 font-mono font-bold text-slate-900">
                                {t.transaction_id || `TXN${String(idx + 1).padStart(4, '0')}`}
                              </td>
                              <td className="py-2.5 px-3 font-semibold text-slate-800">
                                {t.amount !== null && t.amount !== undefined
                                  ? new Intl.NumberFormat('en-IN', { style: 'currency', currency: 'INR' }).format(t.amount)
                                  : 'N/A'}
                              </td>
                              <td className="py-2.5 px-3 font-mono font-bold">
                                <span className={isFraud ? 'text-rose-600' : 'text-slate-800'}>
                                  {(prob * 100).toFixed(1)}%
                                </span>
                              </td>
                              <td className="py-2.5 px-3">
                                <span className={`px-2 py-0.5 rounded-full text-[10px] font-extrabold uppercase border ${
                                  t.risk_level === 'HIGH'
                                    ? 'bg-rose-100 text-rose-800 border-rose-300'
                                    : t.risk_level === 'MEDIUM'
                                    ? 'bg-amber-100 text-amber-800 border-amber-300'
                                    : 'bg-emerald-100 text-emerald-800 border-emerald-300'
                                }`}>
                                  {t.risk_level}
                                </span>
                              </td>
                              <td className="py-2.5 px-3">
                                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                                  isFraud ? 'bg-rose-600 text-white' : 'bg-slate-200 text-slate-700'
                                }`}>
                                  {isFraud ? 'Flagged' : 'Safe'}
                                </span>
                              </td>
                              <td className="py-2.5 px-3 text-center">
                                <button
                                  type="button"
                                  onClick={(e) => {
                                    e.stopPropagation();
                                    setSelectedTransaction(t);
                                  }}
                                  className="text-blue-600 hover:text-blue-800 font-semibold text-xs inline-flex items-center gap-1 cursor-pointer"
                                >
                                  <Eye size={13} /> View
                                </button>
                              </td>
                            </tr>
                          );
                        })}
                      </tbody>
                    </table>
                  </div>
                </section>
              ) : null}

              {/* Empty State before dataset upload */}
              {!analysisResult && !isAnalyzing && (
                <section id="empty-state">
                  <EmptyState onDownloadSample={handleDownloadSample} />
                </section>
              )}

            </div>
          )}

          {/* TAB 2: TRANSACTION ANALYSIS */}
          {activeNav === 'analysis' && (
            <div className="space-y-6 animate-fade-in">
              <TransactionTable
                transactions={analysisResult?.transactions || []}
                onSelectTransaction={setSelectedTransaction}
                onExport={handleExportResults}
                modelInfo={modelInfo}
              />
            </div>
          )}

          {/* TAB 3: FRAUD ALERTS */}
          {activeNav === 'alerts' && (
            <div className="space-y-6 animate-fade-in">
              <FraudAlertsView
                transactions={analysisResult?.transactions || []}
                onSelectTransaction={setSelectedTransaction}
                onNavigateToOverview={() => setActiveNav('overview')}
                modelInfo={modelInfo}
              />
            </div>
          )}

        </main>

        {/* Feature Inspection Drawer */}
        <TransactionDetailsDrawer
          transaction={selectedTransaction}
          onClose={() => setSelectedTransaction(null)}
          modelInfo={modelInfo}
        />

        {/* Footer */}
        <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
          <p className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
            <span>
              <strong>FraudGuard AI</strong> &bull; Online Payment Fraud Detection System Using Federated Learning
            </span>
            <span className="text-[11px] text-slate-400">
              FedProx Global DNN &bull; IEEE-CIS Benchmark &bull; Cutoff ≥ {Number(modelInfo?.threshold || 0.85).toFixed(2)}
            </span>
          </p>
        </footer>

      </div>
    </div>
  );
}
