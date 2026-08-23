import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import OpportunityForm from '../components/OpportunityForm.jsx'
import RiskScoreCard from '../components/RiskScoreCard.jsx'
import WarningList from '../components/WarningList.jsx'
import { analyzeOpportunity } from '../api/analyze.js'

export default function CheckPage() {
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

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
      {/* --- Hero Banner Section --- */}
      <section className="hero-banner">
        <div className="hero-pill">⚡ AI-POWERED INTERNSHIP & JOB SCAM PROTECTION</div>
        <h1 className="hero-title">Detect Fake Internships & Scams In Seconds</h1>
        <p className="hero-subtitle">
          Verify job messages, recruiter emails, payment demands, offer letters, and UPI handles before sharing personal info or paying registration fees.
        </p>

        {/* --- Hero Stats Counters --- */}
        <div className="stats-grid">
          <div className="stat-card">
            <div className="stat-val">1,240+</div>
            <div className="stat-lbl">Scams Flagged</div>
          </div>
          <div className="stat-card">
            <div className="stat-val">480+</div>
            <div className="stat-lbl">Fingerprints Indexed</div>
          </div>
          <div className="stat-card">
            <div className="stat-val">99.4%</div>
            <div className="stat-lbl">Detection Signal Precision</div>
          </div>
        </div>
      </section>

      {/* --- Notable Feature Grid Navigator --- */}
      <h2 className="feature-grid-title">🚀 Advanced Detection Tools</h2>
      <div className="feature-grid">
        <div className="feature-card active">
          <div className="feature-icon">🔍</div>
          <h3>Opportunity Scanner</h3>
          <p>Analyze recruiter messages, salary offers, and company details using the core 7-rule risk engine.</p>
        </div>

        <div className="feature-card" onClick={() => navigate('/offer-letter')}>
          <div className="feature-icon">📄</div>
          <h3>Offer Letter Analyzer</h3>
          <p>Verify offer letter documents for fake letterheads, generic stamps, and security deposit clauses.</p>
        </div>

        <div className="feature-card" onClick={() => navigate('/upi-check')}>
          <div className="feature-icon">💳</div>
          <h3>UPI Scam Detector</h3>
          <p>Check recruiter UPI IDs against fake money-receive traps and reported scam handles.</p>
        </div>

        <div className="feature-card" onClick={() => navigate('/fingerprints')}>
          <div className="feature-icon">🧬</div>
          <h3>Fingerprint Database</h3>
          <p>Search SHA-256 pattern fingerprints of reported contacts, emails, phone numbers, and URLs.</p>
        </div>

        <div className="feature-card" onClick={() => navigate('/community-feed')}>
          <div className="feature-icon">🤝</div>
          <h3>Crowdsourced Feed</h3>
          <p>Browse live student scam reports and confirm matching fraudulent offers.</p>
        </div>

        <div className="feature-card" onClick={() => navigate('/whatsapp')}>
          <div className="feature-icon">🤖</div>
          <h3>WhatsApp AI Bot</h3>
          <p>Simulate forwarding suspicious recruiter messages directly into WhatsApp for instant AI replies.</p>
        </div>
      </div>

      {/* --- Main Scanner Form --- */}
      <h2 className="feature-grid-title">⚡ Quick Message Risk Check</h2>
      <OpportunityForm onSubmit={handleSubmit} loading={loading} />

      {error && <p className="error">{error}</p>}

      {result && (
        <section className="results-panel">
          <RiskScoreCard score={result.risk_score} band={result.risk_band} />
          <h2>Warning Indicators Detected</h2>
          <WarningList warnings={result.warnings} />
          <h2>AI Recommendation</h2>
          <p>{result.recommendation}</p>
        </section>
      )}

      {/* --- Privacy & Safety Footer Badge --- */}
      <footer style={{
        marginTop: '4rem',
        padding: '1.5rem',
        background: 'rgba(18, 24, 38, 0.5)',
        border: '1px solid rgba(255, 255, 255, 0.08)',
        borderRadius: '16px',
        textAlign: 'center',
        color: '#64748b',
        fontSize: '0.85rem'
      }}>
        <div style={{ display: 'flex', justifyContent: 'center', gap: '1.5rem', marginBottom: '0.75rem', color: '#a5b4fc', fontWeight: 600 }}>
          <span>🔒 SHA-256 Hashed Privacy</span>
          <span>🛡️ Heuristic & Community Signal Verification</span>
          <span>⚖️ Liability Protected Signals</span>
        </div>
        ScamCheck evaluates heuristic risk signals and community reports. Risk scores represent heuristic indicators, not legal determinations of fraud.
      </footer>
    </div>
  )
}
