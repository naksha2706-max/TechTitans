import { useState } from 'react'
import { submitScamReport } from '../api/reports.js'

const initialState = {
  company_name: '',
  description: '',
  contact_email: '',
  contact_phone: ''
}

export default function ReportPage() {
  const [form, setForm] = useState(initialState)
  const [submitted, setSubmitted] = useState(false)
  const [error, setError] = useState(null)

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setError(null)
    try {
      await submitScamReport(form)
      setSubmitted(true)
    } catch (err) {
      setError(err.message)
    }
  }

  if (submitted) {
    return (
      <div className="report-page">
        <h1>Thanks for reporting</h1>
        <p>This helps warn other students. It doesn't guarantee an investigation outcome or timeline.</p>
      </div>
    )
  }

  return (
    <div className="report-page">
      <h1>Report a scam</h1>
      <form onSubmit={handleSubmit}>
        <label>
          Company name
          <input value={form.company_name} onChange={update('company_name')} />
        </label>
        <label>
          What happened? <span className="required">*</span>
          <textarea value={form.description} onChange={update('description')} rows={5} required />
        </label>
        <label>
          Recruiter contact email
          <input value={form.contact_email} onChange={update('contact_email')} />
        </label>
        <label>
          Recruiter contact phone
          <input value={form.contact_phone} onChange={update('contact_phone')} />
        </label>
        {error && <p className="error">{error}</p>}
        <button type="submit">Submit report</button>
      </form>
    </div>
  )
}
