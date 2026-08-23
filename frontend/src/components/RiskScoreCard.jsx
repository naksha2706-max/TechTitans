import { bandMeta } from '../utils/riskBand.js'

export default function RiskScoreCard({ score, band }) {
  const meta = bandMeta(band)

  return (
    <div className="risk-score-card" style={{ borderColor: meta.color }}>
      <div className="risk-score-number">{score}/100</div>
      <div className="risk-score-band" style={{ color: meta.color }}>
        {meta.icon} {meta.label}
      </div>
    </div>
  )
}
