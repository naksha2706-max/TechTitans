import { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { isLoggedIn } from '../api/auth.js'

export function useAuth() {
  const [loggedIn, setLoggedIn] = useState(isLoggedIn())
  const location = useLocation()

  useEffect(() => {
    setLoggedIn(isLoggedIn())
  }, [location])

  useEffect(() => {
    // Re-check on storage changes (e.g. login/logout in another tab)
    const handler = () => setLoggedIn(isLoggedIn())
    window.addEventListener('storage', handler)
    return () => window.removeEventListener('storage', handler)
  }, [])

  return { loggedIn, refresh: () => setLoggedIn(isLoggedIn()) }
}
