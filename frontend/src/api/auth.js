import { apiRequest } from './client.js'

export async function login(email, password) {
  const data = await apiRequest('/auth/login', { method: 'POST', body: { email, password } })
  localStorage.setItem('scamcheck_token', data.access_token)
  return data
}

export async function signup(email, password) {
  const data = await apiRequest('/auth/register', { method: 'POST', body: { email, password } })
  localStorage.setItem('scamcheck_token', data.access_token)
  return data
}

export function logout() {
  localStorage.removeItem('scamcheck_token')
}

export function isLoggedIn() {
  return Boolean(localStorage.getItem('scamcheck_token'))
}
