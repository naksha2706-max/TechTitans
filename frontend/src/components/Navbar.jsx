import { Link } from 'react-router-dom'
import { useAuth } from '../hooks/useAuth.js'
import { logout } from '../api/auth.js'

export default function Navbar() {
  const { loggedIn, refresh } = useAuth()

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-brand">ScamCheck</Link>
      <div className="navbar-links">
        <Link to="/">Check an opportunity</Link>
        <Link to="/report">Report a scam</Link>
        {loggedIn ? (
          <>
            <Link to="/history">My history</Link>
            <button onClick={() => { logout(); refresh() }}>Log out</button>
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
