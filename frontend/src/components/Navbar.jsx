import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { logout } from '../api/auth.js'

export default function Navbar() {
  const { loggedIn, refresh } = useAuth()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">
        🛡️ ScamCheck
        <span className="navbar-brand-badge">PRO AI</span>
      </Link>
      <div className="navbar-links">
        {loggedIn ? (
          <>
            <Link to="/">Dashboard</Link>
            <Link to="/offer-letter">📄 Offer Letter</Link>
            <Link to="/upi-check">💳 UPI Check</Link>
            <Link to="/fingerprints">🧬 Fingerprints</Link>
            <Link to="/community-feed">🤝 Feed</Link>
            <Link to="/whatsapp">🤖 WhatsApp Bot</Link>
            <Link to="/report">Report Scam</Link>
            <Link to="/history">My history</Link>
            <button onClick={() => { logout(); refresh(); window.location.reload() }}>Log out</button>
          </>
        ) : (
          <>
            <Link to="/login">Log in</Link>
            <Link to="/signup">Sign up</Link>
          </>
        )}
      </div>
    </nav>
  )
}
