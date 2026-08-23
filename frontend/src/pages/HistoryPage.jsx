import { useEffect, useState } from 'react'
import { Navigate } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { getCheckHistory } from '../api/analyze.js'
import { bandMeta } from '../utils/riskBand.js'

export default function HistoryPage() {
  const { loggedIn } = useAuth()
  const [checks, setChecks] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!loggedIn) return
    getCheckHistory()
      .then((data) => setChecks(data.checks))
      .finally(() => setLoading(false))
  }, [loggedIn])

  if (!loggedIn) return <Navigate to="/login" replace />
  if (loading) return <p>Loading...</p>

  return (
    <div className="history-page">
      <h1>My Checks</h1>
      {checks.length === 0 ? (
        <p>You haven't checked any opportunities yet.</p>
      ) : (
        <ul className="history-list">
          {checks.map((c) => {
            const meta = bandMeta(c.risk_band)
            return (
              <li key={c.id}>
                <span>{c.company_name || 'Unnamed opportunity'}</span>
                <span style={{ color: meta.color }}>{meta.icon} {c.risk_score}/100</span>
                <span>{new Date(c.created_at).toLocaleDateString()}</span>
              </li>
            )
          })}
        </ul>
      )}
    </div>
  )
}
