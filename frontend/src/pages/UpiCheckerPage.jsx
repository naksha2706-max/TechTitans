import { useState } from 'react'
import { apiRequest } from '../api/client.js'
import RiskScoreCard from '../components/RiskScoreCard.jsx'
import WarningList from '../components/WarningList.jsx'

export default function UpiCheckerPage() {
  const [upiId, setUpiId] = useState('')
  const [messageText, setMessageText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await apiRequest('/upi/check', {
        method: 'POST',
        body: { upi_id: upiId, message_text: messageText }
      })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="upi-page">
      <h1>💳 UPI Fake Transaction & Scam Detector</h1>
      <p>Check if a recruiter's UPI handle or payment request is a known scam or fake money-receive trap.</p>

      <form onSubmit={handleSubmit}>
        <label>
          Recruiter / Company UPI ID <span className="required">*</span>
          <input
            type="text"
            placeholder="e.g. refund-hr@ybl, recruiter@okaxis"
            value={upiId}
            onChange={(e) => setUpiId(e.target.value)}
            required
          />
        </label>

        <label>
          Payment Request Message (Optional)
          <textarea
            placeholder="e.g. Enter your UPI PIN to claim ₹5,000 stipend refund..."
            rows={3}
            value={messageText}
            onChange={(e) => setMessageText(e.target.value)}
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing UPI Handle...' : 'Verify UPI Handle'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="results-panel">
          <RiskScoreCard score={result.risk_score} band={result.risk_band} />
          <h2>Warnings & Indicators</h2>
          <WarningList warnings={result.warnings} />
          <h2>Recommendation</h2>
          <p>{result.recommendation}</p>
        </section>
      )}
    </div>
  )
}
