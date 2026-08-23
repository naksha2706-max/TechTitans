import { useState } from 'react'
import OpportunityForm from '../components/OpportunityForm.jsx'
import RiskScoreCard from '../components/RiskScoreCard.jsx'
import WarningList from '../components/WarningList.jsx'
import { analyzeOpportunity } from '../api/analyze.js'

export default function CheckPage() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(form) {
    setLoading(true)
    setError(null)
    try {
      const data = await analyzeOpportunity(form)
      setResult(data)
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="check-page">
      <h1>Check an internship or job opportunity</h1>
      <p>Paste the message you received and get an instant risk assessment.</p>

      <OpportunityForm onSubmit={handleSubmit} loading={loading} />

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="results-panel">
          <RiskScoreCard score={result.risk_score} band={result.risk_band} />
          <h2>Warning Indicators</h2>
          <WarningList warnings={result.warnings} />
          <h2>Recommendation</h2>
          <p>{result.recommendation}</p>
        </section>
      )}
    </div>
  )
}
