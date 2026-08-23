import { useState } from 'react'

const initialState = {
  company_name: '',
  message_text: '',
  salary: '',
  website: '',
  contact_email: ''
}

export default function OpportunityForm({ onSubmit, loading }) {
  const [form, setForm] = useState(initialState)

  function update(field) {
    return (e) => setForm((f) => ({ ...f, [field]: e.target.value }))
  }

  function handleScamPreset() {
    setForm({
      company_name: 'Fast Track Global Tech',
      message_text: 'Congratulations! You are selected for Python Internship. Pay ₹2,500 registration fee immediately within 1 hour to lock your seat. OTP required for processing stipend credit.',
      salary: '250000',
      website: 'https://fasttracktech.weebly.com',
      contact_email: 'hr.recruiter@gmail.com'
    })
  }

  function handleCleanPreset() {
    setForm({
      company_name: 'Acme Software Solutions',
      message_text: 'Thank you for interviewing with Acme Software. We are pleased to offer you the Software Developer Internship role starting next month.',
      salary: '25000',
      website: 'https://acmesoftware.com',
      contact_email: 'careers@acmesoftware.com'
    })
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (!form.message_text.trim()) return
    onSubmit(form)
  }

  return (
    <form onSubmit={handleSubmit} className="opportunity-form">
      <div style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem', flexWrap: 'wrap' }}>
        <button
          type="button"
          onClick={handleScamPreset}
          style={{
            width: 'auto',
            background: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid #ef4444',
            color: '#fca5a5',
            fontSize: '0.85rem',
            padding: '0.4rem 0.9rem'
          }}
        >
          🚨 Load Sample High-Risk Scam
        </button>
        <button
          type="button"
          onClick={handleCleanPreset}
          style={{
            width: 'auto',
            background: 'rgba(16, 185, 129, 0.15)',
            border: '1px solid #10b981',
            color: '#6ee7b7',
            fontSize: '0.85rem',
            padding: '0.4rem 0.9rem'
          }}
        >
          ✅ Load Sample Genuine Offer
        </button>
      </div>

      <label>
        Company name
        <input value={form.company_name} onChange={update('company_name')} placeholder="ABC Technologies" />
      </label>

      <label>
        Job / internship message <span className="required">*</span>
        <textarea
          value={form.message_text}
          onChange={update('message_text')}
          placeholder="Paste the message here..."
          rows={6}
          required
        />
      </label>

      <label>
        Salary offered
        <input value={form.salary} onChange={update('salary')} placeholder="e.g. 40000" />
      </label>

      <label>
        Website
        <input value={form.website} onChange={update('website')} placeholder="https://example.com" />
      </label>

      <label>
        Recruiter / contact email
        <input value={form.contact_email} onChange={update('contact_email')} placeholder="hr@example.com" />
      </label>

      <button type="submit" disabled={loading}>
        {loading ? 'Analyzing Signals...' : 'Run Risk Analysis'}
      </button>
    </form>
  )
}
