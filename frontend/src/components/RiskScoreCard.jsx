import { bandMeta } from '../utils/riskBand.js'

export default function RiskScoreCard({ score, band }) {
  const meta = bandMeta(band)
  const clampedScore = Math.min(Math.max(score, 0), 100)

  return (
    <div className="risk-score-card" style={{ borderColor: meta.color }}>
      <div className="risk-score-number" style={{ color: meta.color }}>
        {clampedScore}<span style={{ fontSize: '1.8rem', color: '#94a3b8' }}>/100</span>
      </div>
      
      {/* Animated Risk Meter Bar */}
      <div style={{
        height: '10px',
        width: '100%',
        background: 'rgba(255, 255, 255, 0.1)',
        borderRadius: '20px',
        overflow: 'hidden',
        margin: '1rem 0 1.25rem 0'
      }}>
        <div style={{
          height: '100%',
          width: `${clampedScore}%`,
          background: meta.color,
          boxShadow: `0 0 12px ${meta.color}`,
          transition: 'width 1s cubic-bezier(0.16, 1, 0.3, 1)'
        }} />
      </div>

      <div className="risk-score-band" style={{ color: meta.color }}>
        {meta.icon} {meta.label}
      </div>
    </div>
  )
}
