import React, { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [connectionStatus, setConnectionStatus] = useState('Checking backend connection...')

  useEffect(() => {
    fetch('http://127.0.0.1:5000/api/health')
      .then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        return response.json()
      })
      .then((data) => {
        if (data.status === 'ok') {
          setConnectionStatus('Backend connection: Connected')
        } else {
          setConnectionStatus('Backend connection: Failed')
        }
      })
      .catch((error) => {
        console.error('Error fetching backend health:', error)
        setConnectionStatus('Backend connection: Failed')
      })
  }, [])

  const getStatusClass = (status) => {
    if (status.includes('Connected')) return 'status-connected'
    if (status.includes('Failed')) return 'status-failed'
    return 'status-checking'
  }

  return (
    <div className="app-container">
      <main className="card">
        <div className="status-pill">Phase 1 Foundation</div>
        <h1 className="title">Online Payment Fraud Detection System</h1>
        <p className="subtitle">
          Machine Learning Framework for Financial Risk Analysis & Fraud Detection
        </p>
        
        <div className="connection-box">
          <span className="connection-label">Status</span>
          <span className={`connection-status ${getStatusClass(connectionStatus)}`}>
            {connectionStatus}
          </span>
        </div>
      </main>
    </div>
  )
}

export default App
