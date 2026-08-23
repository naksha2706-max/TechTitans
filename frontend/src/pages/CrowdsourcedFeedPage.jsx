import { useState, useEffect } from 'react'
import { apiRequest } from '../api/client.js'

export default function CrowdsourcedFeedPage() {
  const [feed, setFeed] = useState([])
  const [loading, setLoading] = useState(true)

  async function loadFeed() {
    try {
      const data = await apiRequest('/reports/feed')
      setFeed(data.reports)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadFeed()
  }, [])

  async function handleConfirm(id) {
    try {
      const res = await apiRequest(`/reports/${id}/confirm`, { method: 'POST' })
      setFeed((prev) =>
        prev.map((item) => (item.id === id ? { ...item, confirm_count: res.confirm_count } : item))
      )
    } catch (err) {
      console.error(err)
    }
  }

  return (
    <div className="feed-page">
      <h1>🤝 Crowdsourced Scam Feed</h1>
      <p>Browse verified scam reports submitted by students to build collective intelligence.</p>

      {loading ? (
        <p>Loading community reports...</p>
      ) : feed.length === 0 ? (
        <p>No community scam reports submitted yet.</p>
      ) : (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem', marginTop: '1.5rem' }}>
          {feed.map((report) => (
            <div key={report.id} className="glass-card" style={{ padding: '1.5rem', marginBottom: 0 }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.75rem' }}>
                <h3 style={{ color: '#ffffff', margin: 0 }}>
                  🏢 {report.company_name || 'Unspecified Company'}
                </h3>
                <span style={{ fontSize: '0.85rem', color: '#94a3b8' }}>
                  {new Date(report.created_at).toLocaleDateString()}
                </span>
              </div>
              <p style={{ fontSize: '0.95rem', color: '#cbd5e1', marginBottom: '1rem' }}>
                {report.description}
              </p>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <span style={{ color: '#ef4444', fontWeight: 600, fontSize: '0.9rem' }}>
                  ⚠️ Flagged Scam Report
                </span>
                <button
                  type="button"
                  onClick={() => handleConfirm(report.id)}
                  style={{
                    width: 'auto',
                    padding: '0.45rem 1rem',
                    fontSize: '0.85rem',
                    background: 'rgba(99, 102, 241, 0.2)',
                    border: '1px solid #6366f1',
                    color: '#a5b4fc'
                  }}
                >
                  👍 I received this offer too ({report.confirm_count || 1})
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
