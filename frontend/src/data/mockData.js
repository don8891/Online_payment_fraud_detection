// Mock Data for the Online Payment Fraud Detection System Dashboard
// Clearly separated for easy backend integration with Flask API later.

export const SYSTEM_METRICS = {
  totalTransactions: 88581,
  fraudulentTransactions: 3083,
  fraudRate: 3.48,
  rocAuc: 0.8899,
  avgPrecision: 0.5032,
  defaultThreshold: 0.20,
  algorithm: 'LightGBM Classifier',
  status: 'Trained & Active',
  trainingSamples: 150000,
  featuresCount: 421,
  fraudSamples: 5275,
  overallAccuracy: 0.9640
};

export const FRAUD_VS_LEGIT_DATA = [
  { name: 'Legitimate', value: 85498, color: '#10b981' },
  { name: 'Fraudulent', value: 3083, color: '#ef4444' }
];

export const PERFORMANCE_METRICS_DATA = [
  { metric: 'ROC-AUC', score: 0.8899 },
  { metric: 'Avg Precision', score: 0.5032 },
  { metric: 'Precision', score: 0.4826 },
  { metric: 'Recall', score: 0.4668 },
  { metric: 'F1 Score', score: 0.4745 }
];

export const CONFUSION_MATRIX = {
  actualLegitPredictedLegit: 83955,
  actualLegitPredictedFraud: 1543, // False Positive
  actualFraudPredictedLegit: 1644, // False Negative
  actualFraudPredictedFraud: 1439  // True Positive
};

export const RISK_DISTRIBUTION = [
  { name: 'Low Risk (0.00 - 0.19)', count: 81250, color: 'bg-emerald-500' },
  { name: 'Medium Risk (0.20 - 0.49)', count: 4250, color: 'bg-amber-500' },
  { name: 'High Risk (0.50 - 1.00)', count: 3081, color: 'bg-red-500' }
];

export const VAL_VS_TEST_PERFORMANCE = [
  { name: 'ROC-AUC', Validation: 0.8951, Test: 0.8899 },
  { name: 'Avg Precision', Validation: 0.5415, Test: 0.5032 }
];

export const SHAP_FEATURE_IMPORTANCE = [
  { feature: 'TransactionAmt', importance: 0.284, description: 'Amount of payment' },
  { feature: 'ProductCD', importance: 0.182, description: 'Product code of the item' },
  { feature: 'card1', importance: 0.153, description: 'Card issuer information' },
  { feature: 'card2', importance: 0.119, description: 'Card design/billing country code' },
  { feature: 'P_emaildomain', importance: 0.095, description: 'Purchaser email domain suffix' },
  { feature: 'C1', importance: 0.081, description: 'Count of addresses associated with card' },
  { feature: 'D1', importance: 0.063, description: 'Days since card first transaction' },
  { feature: 'V87', importance: 0.052, description: 'Vesta engineered feature: transaction frequency' },
  { feature: 'V258', importance: 0.041, description: 'Vesta engineered feature: device consistency' },
  { feature: 'id_02', importance: 0.032, description: 'Device security identifier match' }
];

export const MOCK_TRANSACTIONS = [
  {
    id: 'TXN-10001',
    amount: 125.50,
    product: 'W',
    paymentType: 'Debit',
    emailDomain: 'gmail.com',
    riskScore: 0.03,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 19:42',
    cardType: 'Visa',
    cardCategory: 'Classic',
    receiverEmail: 'gmail.com',
    deviceType: 'desktop',
    deviceInfo: 'Windows/Chrome'
  },
  {
    id: 'TXN-10002',
    amount: 845.20,
    product: 'C',
    paymentType: 'Credit',
    emailDomain: 'protonmail.com',
    riskScore: 0.87,
    prediction: 'Fraud',
    status: 'Blocked',
    date: '2026-08-17 19:40',
    cardType: 'Mastercard',
    cardCategory: 'Platinum',
    receiverEmail: 'outlook.com',
    deviceType: 'mobile',
    deviceInfo: 'iOS/Safari'
  },
  {
    id: 'TXN-10003',
    amount: 54.80,
    product: 'W',
    paymentType: 'Debit',
    emailDomain: 'gmail.com',
    riskScore: 0.12,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 19:35',
    cardType: 'Visa',
    cardCategory: 'Standard',
    receiverEmail: 'yahoo.com',
    deviceType: 'desktop',
    deviceInfo: 'macOS/Firefox'
  },
  {
    id: 'TXN-10004',
    amount: 1420.00,
    product: 'R',
    paymentType: 'Credit',
    emailDomain: 'yandex.ru',
    riskScore: 0.94,
    prediction: 'Fraud',
    status: 'Blocked',
    date: '2026-08-17 19:30',
    cardType: 'Discover',
    cardCategory: 'Gold',
    receiverEmail: 'mail.ru',
    deviceType: 'mobile',
    deviceInfo: 'Android/Chrome'
  },
  {
    id: 'TXN-10005',
    amount: 320.45,
    product: 'H',
    paymentType: 'Credit',
    emailDomain: 'yahoo.com',
    riskScore: 0.28,
    prediction: 'Fraud', // Threshold is 0.20
    status: 'Blocked',
    date: '2026-08-17 19:25',
    cardType: 'Visa',
    cardCategory: 'Signature',
    receiverEmail: 'gmail.com',
    deviceType: 'tablet',
    deviceInfo: 'iPadOS/Safari'
  },
  {
    id: 'TXN-10006',
    amount: 15.99,
    product: 'W',
    paymentType: 'Debit',
    emailDomain: 'gmail.com',
    riskScore: 0.01,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 19:15',
    cardType: 'Mastercard',
    cardCategory: 'Standard',
    receiverEmail: 'gmail.com',
    deviceType: 'desktop',
    deviceInfo: 'Windows/Edge'
  },
  {
    id: 'TXN-10007',
    amount: 1850.00,
    product: 'C',
    paymentType: 'Credit',
    emailDomain: 'tempmail.xyz',
    riskScore: 0.98,
    prediction: 'Fraud',
    status: 'Blocked',
    date: '2026-08-17 19:02',
    cardType: 'Mastercard',
    cardCategory: 'Black',
    receiverEmail: 'outlook.com',
    deviceType: 'mobile',
    deviceInfo: 'iOS/Unknown Browser'
  },
  {
    id: 'TXN-10008',
    amount: 95.00,
    product: 'W',
    paymentType: 'Debit',
    emailDomain: 'yahoo.com',
    riskScore: 0.05,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 18:50',
    cardType: 'Visa',
    cardCategory: 'Classic',
    receiverEmail: 'yahoo.com',
    deviceType: 'desktop',
    deviceInfo: 'macOS/Chrome'
  },
  {
    id: 'TXN-10009',
    amount: 612.30,
    product: 'R',
    paymentType: 'Credit',
    emailDomain: 'protonmail.com',
    riskScore: 0.65,
    prediction: 'Fraud',
    status: 'Blocked',
    date: '2026-08-17 18:45',
    cardType: 'Visa',
    cardCategory: 'Platinum',
    receiverEmail: 'gmail.com',
    deviceType: 'mobile',
    deviceInfo: 'Android/Opera'
  },
  {
    id: 'TXN-10010',
    amount: 110.00,
    product: 'W',
    paymentType: 'Credit',
    emailDomain: 'gmail.com',
    riskScore: 0.18,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 18:32',
    cardType: 'Discover',
    cardCategory: 'Standard',
    receiverEmail: 'gmail.com',
    deviceType: 'desktop',
    deviceInfo: 'Linux/Firefox'
  },
  {
    id: 'TXN-10011',
    amount: 450.00,
    product: 'C',
    paymentType: 'Debit',
    emailDomain: 'outlook.com',
    riskScore: 0.22,
    prediction: 'Fraud', // Threshold 0.20
    status: 'Blocked',
    date: '2026-08-17 18:20',
    cardType: 'Visa',
    cardCategory: 'Gold',
    receiverEmail: 'outlook.com',
    deviceType: 'mobile',
    deviceInfo: 'iOS/Chrome'
  },
  {
    id: 'TXN-10012',
    amount: 1250.00,
    product: 'H',
    paymentType: 'Credit',
    emailDomain: 'hotmail.com',
    riskScore: 0.58,
    prediction: 'Fraud',
    status: 'Blocked',
    date: '2026-08-17 18:10',
    cardType: 'Amex',
    cardCategory: 'Centurion',
    receiverEmail: 'live.com',
    deviceType: 'desktop',
    deviceInfo: 'Windows/Chrome'
  },
  {
    id: 'TXN-10013',
    amount: 85.00,
    product: 'W',
    paymentType: 'Debit',
    emailDomain: 'gmail.com',
    riskScore: 0.08,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 17:55',
    cardType: 'Visa',
    cardCategory: 'Classic',
    receiverEmail: 'gmail.com',
    deviceType: 'desktop',
    deviceInfo: 'macOS/Safari'
  },
  {
    id: 'TXN-10014',
    amount: 3200.00,
    product: 'R',
    paymentType: 'Credit',
    emailDomain: 'anonymous.net',
    riskScore: 0.99,
    prediction: 'Fraud',
    status: 'Blocked',
    date: '2026-08-17 17:40',
    cardType: 'Mastercard',
    cardCategory: 'Platinum',
    receiverEmail: 'darkweb.org',
    deviceType: 'mobile',
    deviceInfo: 'TOr Browser/Linux'
  },
  {
    id: 'TXN-10015',
    amount: 45.25,
    product: 'W',
    paymentType: 'Debit',
    emailDomain: 'gmail.com',
    riskScore: 0.02,
    prediction: 'Legitimate',
    status: 'Safe',
    date: '2026-08-17 17:30',
    cardType: 'Visa',
    cardCategory: 'Standard',
    receiverEmail: 'yahoo.com',
    deviceType: 'mobile',
    deviceInfo: 'Android/Chrome'
  }
];
