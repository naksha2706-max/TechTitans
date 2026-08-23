const BASE_URL = import.meta.env.VITE_API_BASE_URL || ''

function getToken() {
  const token = localStorage.getItem('scamcheck_token')
  if (!token || token === 'null' || token === 'undefined') return null
  return token
}

export async function apiRequest(path, { method = 'GET', body, auth = false } = {}) {
  const headers = { 'Content-Type': 'application/json' }
  if (auth) {
    const token = getToken()
    if (token) headers.Authorization = `Bearer ${token}`
  }

  const res = await fetch(`${BASE_URL}/api${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  })

  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || `Request failed: ${res.status}`)
  }

  return res.json()
}
