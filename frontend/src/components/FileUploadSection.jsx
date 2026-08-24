import React, { useState, useRef } from 'react';
import { UploadCloud, FileText, Download, Play, CheckCircle2, Loader2, AlertCircle } from 'lucide-react';

export default function FileUploadSection({
  selectedFile,
  fileMeta,
  onFileSelect,
  onAnalyze,
  onDownloadSample,
  isAnalyzing,
  analysisStep,
  errorMessage
}) {
  const [isDragOver, setIsDragOver] = useState(false);
  const fileInputRef = useRef(null);

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const file = e.dataTransfer.files[0];
      if (file.name.toLowerCase().endsWith('.csv')) {
        onFileSelect(file);
      } else {
        alert("Please select a valid CSV file (.csv)");
      }
    }
  };

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      onFileSelect(file);
    }
  };

  const formatSize = (bytes) => {
    if (!bytes) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const steps = [
    "Uploading...",
    "Processing...",
    "Running fraud detection...",
    "Generating results..."
  ];

  return (
    <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-5">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-100">
        <div>
          <h2 className="text-lg font-bold text-slate-800 tracking-tight flex items-center gap-2">
            <UploadCloud size={20} className="text-blue-600" />
            Upload Transaction Dataset
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            Select or drag & drop your transaction batch CSV for instant LightGBM ML evaluation
          </p>
        </div>

        <button
          onClick={onDownloadSample}
          type="button"
          className="inline-flex items-center gap-2 px-4 py-2 text-xs font-semibold text-blue-700 bg-blue-50 border border-blue-200 rounded-xl hover:bg-blue-100 transition-colors self-start sm:self-auto"
        >
          <Download size={14} />
          Download Sample CSV
        </button>
      </div>

      {/* Drag & Drop Dropzone */}
      <div
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        onClick={() => !isAnalyzing && fileInputRef.current?.click()}
        className={`relative border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 ${
          isDragOver
            ? 'border-blue-500 bg-blue-50/60 scale-[1.005]'
            : selectedFile
            ? 'border-emerald-300 bg-emerald-50/20'
            : 'border-slate-300 hover:border-blue-400 bg-slate-50/50 hover:bg-slate-50'
        } ${isAnalyzing ? 'pointer-events-none opacity-80' : ''}`}
      >
        <input
          ref={fileInputRef}
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          className="hidden"
        />

        <div className="flex flex-col items-center justify-center space-y-3">
          <div className={`p-4 rounded-2xl transition-transform ${
            selectedFile ? 'bg-emerald-100 text-emerald-600' : 'bg-blue-100 text-blue-600'
          }`}>
            <UploadCloud size={36} />
          </div>

          <div>
            <h3 className="text-base font-bold text-slate-800">
              Upload Transaction File
            </h3>
            <p className="text-xs text-slate-500 mt-1">
              Drag & drop a CSV file here or <span className="text-blue-600 font-semibold underline">browse from your computer</span>
            </p>
          </div>

          <span className="inline-block px-3 py-1 bg-slate-200/60 text-slate-600 text-[11px] font-semibold rounded-md">
            Accepted format: .csv
          </span>
        </div>
      </div>

      {/* Selected File Details */}
      {selectedFile && (
        <div className="bg-slate-50 rounded-xl p-4 border border-slate-200 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-blue-600 text-white rounded-lg">
              <FileText size={20} />
            </div>
            <div>
              <p className="text-sm font-bold text-slate-900 truncate max-w-xs sm:max-w-md">
                {selectedFile.name}
              </p>
              <div className="flex items-center gap-3 text-xs text-slate-500 mt-0.5">
                <span>Size: <strong className="text-slate-700">{formatSize(selectedFile.size)}</strong></span>
                <span>•</span>
                <span>Rows: <strong className="text-slate-700">{fileMeta.rowCount > 0 ? fileMeta.rowCount.toLocaleString() : 'Calculating...'}</strong></span>
              </div>
            </div>
          </div>

          <button
            onClick={onAnalyze}
            disabled={isAnalyzing}
            type="button"
            className="inline-flex items-center justify-center gap-2 px-6 py-2.5 text-sm font-bold text-white bg-blue-600 hover:bg-blue-700 active:bg-blue-800 rounded-xl shadow-md shadow-blue-500/20 disabled:opacity-50 transition-all"
          >
            {isAnalyzing ? (
              <>
                <Loader2 size={18} className="animate-spin" />
                Analyzing...
              </>
            ) : (
              <>
                <Play size={18} className="fill-white" />
                Analyze Transactions
              </>
            )}
          </button>
        </div>
      )}

      {/* Analysis Progress Loading State */}
      {isAnalyzing && (
        <div className="bg-blue-50/70 border border-blue-200 rounded-xl p-5 space-y-4">
          <div className="flex items-center justify-between">
            <h4 className="text-xs font-bold text-blue-900 uppercase tracking-wider flex items-center gap-2">
              <Loader2 size={16} className="animate-spin text-blue-600" />
              Machine Learning Analysis in Progress
            </h4>
            <span className="text-xs font-bold text-blue-700">
              Step {analysisStep + 1} of 4
            </span>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-blue-200/80 rounded-full h-2 overflow-hidden">
            <div
              className="bg-blue-600 h-full transition-all duration-500 ease-out"
              style={{ width: `${((analysisStep + 1) / 4) * 100}%` }}
            />
          </div>

          {/* Steps List */}
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
            {steps.map((stepText, idx) => (
              <div
                key={idx}
                className={`p-2.5 rounded-lg flex items-center gap-2 font-semibold transition-colors ${
                  idx < analysisStep
                    ? 'bg-emerald-100/80 text-emerald-800 border border-emerald-300/50'
                    : idx === analysisStep
                    ? 'bg-white text-blue-900 border border-blue-300 shadow-sm font-bold'
                    : 'bg-blue-100/40 text-blue-400'
                }`}
              >
                {idx < analysisStep ? (
                  <CheckCircle2 size={14} className="text-emerald-600 shrink-0" />
                ) : idx === analysisStep ? (
                  <Loader2 size={14} className="animate-spin text-blue-600 shrink-0" />
                ) : (
                  <span className="w-3.5 h-3.5 rounded-full border border-blue-300 shrink-0" />
                )}
                <span className="truncate">{stepText}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Error Message Display */}
      {errorMessage && (
        <div className="bg-rose-50 border border-rose-200 text-rose-800 rounded-xl p-4 flex items-start gap-3 text-xs font-medium">
          <AlertCircle size={18} className="text-rose-600 shrink-0 mt-0.5" />
          <div className="space-y-1">
            <p className="font-bold text-rose-900">Analysis Error</p>
            <p>{errorMessage}</p>
          </div>
        </div>
      )}
    </div>
  );
}
