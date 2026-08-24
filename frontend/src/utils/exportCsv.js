export function exportTransactionsToCsv(transactions, filename = "fraud_detection_results.csv") {
  if (!transactions || transactions.length === 0) return;

  // Determine all unique column keys from raw_features plus model prediction outputs
  const baseHeaders = ["transaction_id", "amount", "fraud_probability", "risk_level", "prediction"];
  
  // Collect extra raw feature keys
  const extraKeys = new Set();
  transactions.forEach(t => {
    if (t.raw_features) {
      Object.keys(t.raw_features).forEach(k => {
        if (!baseHeaders.includes(k) && k !== "TransactionID" && k !== "TransactionAmt") {
          extraKeys.add(k);
        }
      });
    }
  });

  const allHeaders = [...baseHeaders, ...Array.from(extraKeys)];

  // Escape helper for CSV cells
  const escapeCsv = (val) => {
    if (val === null || val === undefined) return '""';
    const str = String(val).replace(/"/g, '""');
    return `"${str}"`;
  };

  const csvRows = [];
  // Add Header Row
  csvRows.push(allHeaders.map(escapeCsv).join(","));

  // Add Data Rows
  transactions.forEach(t => {
    const rowValues = allHeaders.map(header => {
      if (header === "transaction_id") return t.transaction_id;
      if (header === "amount") return t.amount !== null ? t.amount : "";
      if (header === "fraud_probability") return t.fraud_probability;
      if (header === "risk_level") return t.risk_level;
      if (header === "prediction") return t.prediction === 1 ? "Fraud" : "Legitimate";

      // Raw features fallback
      if (t.raw_features && t.raw_features.hasOwnProperty(header)) {
        return t.raw_features[header];
      }
      return "";
    });

    csvRows.push(rowValues.map(escapeCsv).join(","));
  });

  const csvString = csvRows.join("\n");
  const blob = new Blob([csvString], { type: "text/csv;charset=utf-8;" });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement("a");
  link.setAttribute("href", url);
  link.setAttribute("download", filename);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
