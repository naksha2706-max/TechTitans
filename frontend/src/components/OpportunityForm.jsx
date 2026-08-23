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

  function handleSubmit(e) {
    e.preventDefault()
    if (!form.message_text.trim()) return
    onSubmit(form)
  }

  return (
    <form onSubmit={handleSubmit} className="opportunity-form">
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
        {loading ? 'Checking...' : 'Check Now'}
      </button>
    </form>
  )
}
