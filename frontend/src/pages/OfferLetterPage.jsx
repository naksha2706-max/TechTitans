import { useState } from 'react'
import { apiRequest } from '../api/client.js'
import RiskScoreCard from '../components/RiskScoreCard.jsx'
import WarningList from '../components/WarningList.jsx'

export default function OfferLetterPage() {
  const [docText, setDocText] = useState('')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    if (!docText.trim()) return
    setLoading(true)
    setError(null)
    setResult(null)

    try {
      const data = await apiRequest('/analyze/document', {
        method: 'POST',
        body: { document_text: docText, filename: 'Offer_Letter.pdf' }
      })
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="offer-letter-page">
      <h1>📄 Offer Letter Document Analyzer</h1>
      <p>Paste the full text of an offer letter or internship contract to check for fake letterheads and security deposit clauses.</p>

      <form onSubmit={handleSubmit}>
        <label>
          Offer Letter Content <span className="required">*</span>
          <textarea
            rows={8}
            placeholder="Paste complete offer letter text, email body, or extracted document contents here..."
            value={docText}
            onChange={(e) => setDocText(e.target.value)}
            required
          />
        </label>

        <button type="submit" disabled={loading}>
          {loading ? 'Analyzing Document...' : 'Analyze Offer Letter'}
        </button>
      </form>

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="results-panel">
          <RiskScoreCard score={result.risk_score} band={result.risk_band} />
          <h2>Document Warning Indicators</h2>
          <WarningList warnings={result.warnings} />
          <h2>Recommendation</h2>
          <p>{result.recommendation}</p>
        </section>
      )}
    </div>
  )
}
