import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { signup } from '../api/auth.js'

export default function SignupPage() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    try {
      await signup(email, password)
      navigate('/history')
    } catch (err) {
      setError(err.message)
    }
  }

  return (
    <div className="auth-page">
      <h1>Sign up</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Email
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
        </label>
        <label>
          Password
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required minLength={8} />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit">Sign up</button>
      </form>
    </div>
  )
}
