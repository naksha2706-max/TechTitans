// Mirrors docs/FEATURE_SPECIFICATION.md — keep in sync with the backend.
// The backend is the source of truth for scoring; this is only used to
// pick a color/icon on the frontend from the band the API already returns.

export const RISK_BAND_META = {
  low: { color: '#1a7f37', icon: '🟢', label: 'Low Risk' },
  medium: { color: '#b8860b', icon: '🟠', label: 'Medium Risk' },
  high: { color: '#c0392b', icon: '🔴', label: 'High Risk' }
}

export function bandMeta(band) {
  return RISK_BAND_META[band] || RISK_BAND_META.medium
}
