import { useState, useEffect } from 'react'
import { apiRequest } from '../api/client.js'

export default function FingerprintsPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  async function handleSearch(e) {
    if (e) e.preventDefault()
    setLoading(true)
    try {
      const data = await apiRequest(`/fingerprints/search?query=${encodeURIComponent(query)}`)
      setResults(data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    handleSearch()
  }, [])

  return (
    <div className="fingerprint-page">
      <h1>🧬 Scam Fingerprint Database</h1>
      <p>Search reported contact handles, UPI IDs, emails, and scam pattern fingerprints.</p>

      <form onSubmit={handleSearch}>
        <label>
          Search Fingerprint Database
          <input
            type="text"
            placeholder="Search email, phone, UPI handle, or company name..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <button type="submit" disabled={loading}>
          {loading ? 'Searching Database...' : 'Search Fingerprints'}
        </button>
      </form>

      {results && (
        <section className="results-panel">
          <h2>Fingerprint Matches ({results.matches_found})</h2>
          {results.fingerprints.length === 0 ? (
            <p>No scam fingerprints found matching this query in the database.</p>
          ) : (
            <ul className="history-list">
              {results.fingerprints.map((fp, idx) => (
                <li key={idx}>
                  <div>
                    <span style={{ display: 'block', fontSize: '0.95rem' }}>
                      {fp.company_name || fp.contact_hash || 'Scam Contact Fingerprint'}
                    </span>
                    <small style={{ color: '#94a3b8' }}>
                      {fp.description || (fp.type ? `Type: ${fp.type.toUpperCase()}` : 'Reported Scam Fingerprint')}
                    </small>
                  </div>
                  <span style={{ color: '#ef4444' }}>
                    {fp.report_count ? `⚠️ ${fp.report_count} Reports` : '🔴 Flagged'}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </section>
      )}
    </div>
  )
}
