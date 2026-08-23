import { useState } from 'react'
import { useNavigate, Link } from 'react-router-dom'
import { login, signup } from '../api/auth.js'

export default function LoginPage({ mode = 'login' }) {
  const [isLogin, setIsLogin] = useState(mode === 'login')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      if (isLogin) {
        await login(email, password)
      } else {
        await signup(email, password)
      }
      navigate('/')
      window.location.reload()
    } catch (err) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  async function handleDemoLogin() {
    setLoading(true)
    setError(null)
    const demoEmail = `student_${Math.floor(Math.random() * 10000)}@college.edu`
    const demoPassword = 'securepassword123'
    try {
      await signup(demoEmail, demoPassword)
      navigate('/')
      window.location.reload()
    } catch (err) {
      // If duplicate, try login
      try {
        await login(demoEmail, demoPassword)
        navigate('/')
        window.location.reload()
      } catch (lErr) {
        setError(lErr.message)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="auth-page" style={{ maxWidth: '480px', margin: '3rem auto' }}>
      <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
        <div style={{ fontSize: '3rem', marginBottom: '0.5rem' }}>🛡️</div>
        <h1 style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>Welcome to ScamCheck</h1>
        <p style={{ color: '#94a3b8', fontSize: '0.95rem' }}>
          Please log in or create an account to access the ScamCheck AI detection suite.
        </p>
      </div>

      <div className="glass-card">
        {/* Auth Mode Selector Tabs */}
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.75rem', background: 'rgba(15, 21, 35, 0.8)', padding: '0.35rem', borderRadius: '10px' }}>
          <button
            type="button"
            onClick={() => { setIsLogin(true); setError(null) }}
            style={{
              flex: 1,
              background: isLogin ? '#6366f1' : 'transparent',
              color: isLogin ? 'white' : '#94a3b8',
              boxShadow: isLogin ? '0 4px 12px rgba(99, 102, 241, 0.4)' : 'none',
              padding: '0.6rem 1rem',
              fontSize: '0.9rem'
            }}
          >
            Log In
          </button>
          <button
            type="button"
            onClick={() => { setIsLogin(false); setError(null) }}
            style={{
              flex: 1,
              background: !isLogin ? '#6366f1' : 'transparent',
              color: !isLogin ? 'white' : '#94a3b8',
              boxShadow: !isLogin ? '0 4px 12px rgba(99, 102, 241, 0.4)' : 'none',
              padding: '0.6rem 1rem',
              fontSize: '0.9rem'
            }}
          >
            Create Account
          </button>
        </div>

        <form onSubmit={handleSubmit} style={{ background: 'transparent', border: 'none', padding: 0, boxShadow: 'none', marginBottom: '1.25rem' }}>
          <label>
            Student Email Address
            <input
              type="email"
              placeholder="student@college.edu"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </label>

          <label>
            Password
            <input
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              minLength={6}
            />
          </label>

          {error && <p className="error">{error}</p>}

          <button type="submit" disabled={loading} style={{ marginTop: '0.5rem' }}>
            {loading ? 'Authenticating...' : isLogin ? 'Log In to ScamCheck' : 'Create Student Account'}
          </button>
        </form>

        <div style={{ textAlign: 'center', marginTop: '1.25rem', paddingTop: '1.25rem', borderTop: '1px solid rgba(255, 255, 255, 0.1)' }}>
          <button
            type="button"
            onClick={handleDemoLogin}
            disabled={loading}
            style={{
              background: 'rgba(16, 185, 129, 0.15)',
              border: '1px solid #10b981',
              color: '#6ee7b7',
              fontSize: '0.9rem'
            }}
          >
            ⚡ Continue with 1-Click Demo Account
          </button>
        </div>
      </div>
    </div>
  )
}
