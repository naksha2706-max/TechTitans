import { apiRequest } from './client.js'

// Matches docs/API_SPECIFICATION.md POST /api/reports
export function submitScamReport(payload) {
  return apiRequest('/reports', { method: 'POST', body: payload, auth: true })
}

// Matches docs/API_SPECIFICATION.md GET /api/reputation
export function lookupReputation(type, value) {
  const params = new URLSearchParams({ type, value })
  return apiRequest(`/reputation?${params.toString()}`)
}
