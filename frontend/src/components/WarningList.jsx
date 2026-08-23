export default function WarningList({ warnings }) {
  if (!warnings || warnings.length === 0) {
    return <p className="no-warnings">🟢 No warning signals detected.</p>
  }

  return (
    <ul className="warning-list">
      {warnings.map((w) => (
        <li key={w.code}>
          <span>⚠️ <strong>{w.label}</strong></span>
          <span style={{ marginLeft: 'auto', fontWeight: 'bold' }}>+{w.points} pts</span>
        </li>
      ))}
    </ul>
  )
}
