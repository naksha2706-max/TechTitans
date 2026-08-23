import { useState } from 'react'
import { apiRequest } from '../api/client.js'

export default function WhatsAppBotPage() {
  const [messages, setMessages] = useState([
    { sender: 'bot', text: '👋 Hi there! Send or forward any suspicious internship message, job offer, or UPI handle here to get an instant AI risk report.' }
  ])
  const [inputText, setInputText] = useState('')
  const [loading, setLoading] = useState(false)

  async function handleSend(e) {
    e.preventDefault()
    if (!inputText.trim() || loading) return

    const userMsg = inputText.trim()
    setMessages((prev) => [...prev, { sender: 'user', text: userMsg }])
    setInputText('')
    setLoading(true)

    try {
      const res = await apiRequest('/whatsapp/message', {
        method: 'POST',
        body: { message_text: userMsg }
      })
      setMessages((prev) => [...prev, { sender: 'bot', text: res.reply }])
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { sender: 'bot', text: `⚠️ Error analyzing message: ${err.message}` }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="whatsapp-page">
      <h1>🤖 WhatsApp Scam Bot Simulator</h1>
      <p>Simulate forwarding a message to the ScamCheck WhatsApp Bot to see automated AI detection replies.</p>

      <div className="whatsapp-chat-container">
        <div className="whatsapp-header">
          <div className="whatsapp-avatar">🤖</div>
          <div>
            <h3 style={{ color: 'white', margin: 0, fontSize: '1.05rem' }}>ScamCheck WhatsApp Bot</h3>
            <span style={{ color: '#25d366', fontSize: '0.8rem', fontWeight: 500 }}>● Online | AI Risk Detector</span>
          </div>
        </div>

        <div className="whatsapp-chat-body">
          {messages.map((m, idx) => (
            <div key={idx} className={`chat-bubble ${m.sender}`}>
              {m.text}
            </div>
          ))}
          {loading && <div className="chat-bubble bot">Analyzing message for risk signals...</div>}
        </div>

        <form className="whatsapp-input-bar" onSubmit={handleSend}>
          <input
            type="text"
            placeholder="Paste suspicious offer or message..."
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
          />
          <button type="submit" disabled={loading}>Send</button>
        </form>
      </div>
    </div>
  )
}
