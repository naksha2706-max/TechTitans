import { apiRequest } from './client.js'

// Matches the contract in docs/API_SPECIFICATION.md POST /api/analyze
export function analyzeOpportunity(payload) {
  return apiRequest('/analyze', { method: 'POST', body: payload, auth: true })
}

export function getCheckHistory() {
  return apiRequest('/checks', { auth: true })
}
