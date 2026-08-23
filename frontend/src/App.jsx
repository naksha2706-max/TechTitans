import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import CheckPage from './pages/CheckPage.jsx'
import HistoryPage from './pages/HistoryPage.jsx'
import ReportPage from './pages/ReportPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import SignupPage from './pages/SignupPage.jsx'
import WhatsAppBotPage from './pages/WhatsAppBotPage.jsx'
import UpiCheckerPage from './pages/UpiCheckerPage.jsx'

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          <Route path="/" element={<CheckPage />} />
          <Route path="/upi-check" element={<UpiCheckerPage />} />
          <Route path="/whatsapp" element={<WhatsAppBotPage />} />
          <Route path="/report" element={<ReportPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </main>
    </>
  )
}
