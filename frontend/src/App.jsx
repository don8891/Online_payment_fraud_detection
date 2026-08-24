import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import FileUploadSection from './components/FileUploadSection';
import AnalysisSummary from './components/AnalysisSummary';
import VisualSummary from './components/VisualSummary';
import TransactionTable from './components/TransactionTable';
import TransactionDetailsDrawer from './components/TransactionDetailsDrawer';
import EmptyState from './components/EmptyState';
import { exportTransactionsToCsv } from './utils/exportCsv';

const API_BASE_URL = 'http://localhost:5000';

export default function App() {
  // Backend connection state
  const [backendConnected, setBackendConnected] = useState(false);
  const [checkingBackend, setCheckingBackend] = useState(false);

  // File Upload State
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileMeta, setFileMeta] = useState({ rowCount: 0 });

  // Analysis / ML State
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState(0);
  const [analysisResult, setAnalysisResult] = useState(null);
  const [errorMessage, setErrorMessage] = useState(null);

  // Detail Drawer State
  const [selectedTransaction, setSelectedTransaction] = useState(null);

  // Check Backend Health
  const checkHealth = async () => {
    setCheckingBackend(true);
    try {
      const res = await fetch(`${API_BASE_URL}/api/health`, { method: 'GET' });
      if (res.ok) {
        setBackendConnected(true);
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

  // Handle File Selection and parse estimated row count
  const handleFileSelect = (file) => {
    setSelectedFile(file);
    setAnalysisResult(null);
    setErrorMessage(null);
    setFileMeta({ rowCount: 0 });

    // Read first few KB to estimate line count
    const reader = new FileReader();
    reader.onload = (e) => {
      const text = e.target.result;
      const lines = text.split('\n').filter(l => l.trim().length > 0);
      if (lines.length > 1) {
        // Approximate total lines based on slice vs file size
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

  // Run ML Analysis via POST /api/predict
  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setErrorMessage(null);
    setAnalysisStep(0);

    // Multi-stage visual progress timers
    const timer1 = setTimeout(() => setAnalysisStep(1), 600);
    const timer2 = setTimeout(() => setAnalysisStep(2), 1200);

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
      } else {
        setErrorMessage(data.error || 'Prediction failed. Please check the uploaded CSV file.');
      }
    } catch (err) {
      setErrorMessage('Unable to connect to Flask backend. Please verify that backend is running on http://localhost:5000.');
      setBackendConnected(false);
    } finally {
      clearTimeout(timer1);
      clearTimeout(timer2);
      setIsAnalyzing(false);
    }
  };

  // Export Results to CSV
  const handleExportResults = () => {
    if (analysisResult && analysisResult.transactions) {
      exportTransactionsToCsv(analysisResult.transactions, `fraud_analysis_${selectedFile?.name || 'results'}.csv`);
    }
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-900 selection:bg-blue-600 selection:text-white">
      {/* Header */}
      <Header
        backendConnected={backendConnected}
        checkingBackend={checkingBackend}
        onRefreshHealth={checkHealth}
      />

      {/* Single-Page Main Dashboard Layout */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 space-y-6">

        {/* Section 2: File Upload Area */}
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
          />
        </section>

        {/* Section 3: Analysis Summary (KPI Cards) */}
        {analysisResult && (
          <section id="summary-section">
            <AnalysisSummary
              summary={analysisResult.summary}
              modelInfo={analysisResult.model_info}
            />
          </section>
        )}

        {/* Section 5: Visual Summary / Charts */}
        {analysisResult && analysisResult.transactions && (
          <section id="visuals-section">
            <VisualSummary
              transactions={analysisResult.transactions}
              summary={analysisResult.summary}
            />
          </section>
        )}

        {/* Section 4: Fraud Detection Results Table & Section 7: Export */}
        {analysisResult && analysisResult.transactions && (
          <section id="results-section">
            <TransactionTable
              transactions={analysisResult.transactions}
              onSelectTransaction={setSelectedTransaction}
              onExport={handleExportResults}
            />
          </section>
        )}

        {/* Section 8: Empty State (When no analysis performed yet) */}
        {!analysisResult && !isAnalyzing && (
          <section id="empty-state">
            <EmptyState onDownloadSample={handleDownloadSample} />
          </section>
        )}

      </main>

      {/* Section 6: Transaction Details Right Drawer */}
      <TransactionDetailsDrawer
        transaction={selectedTransaction}
        onClose={() => setSelectedTransaction(null)}
      />

      {/* Footer */}
      <footer className="bg-white border-t border-slate-200 py-4 text-center text-xs text-slate-500">
        <p>Online Payment Fraud Detection System &bull; Single-Page Analyst Dashboard &bull; LightGBM Model (Threshold 0.20)</p>
      </footer>
    </div>
  );
}
