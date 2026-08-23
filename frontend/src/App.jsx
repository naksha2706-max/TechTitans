import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth.js'
import Navbar from './components/Navbar.jsx'
import CheckPage from './pages/CheckPage.jsx'
import HistoryPage from './pages/HistoryPage.jsx'
import ReportPage from './pages/ReportPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import SignupPage from './pages/SignupPage.jsx'
import WhatsAppBotPage from './pages/WhatsAppBotPage.jsx'
import UpiCheckerPage from './pages/UpiCheckerPage.jsx'
import OfferLetterPage from './pages/OfferLetterPage.jsx'
import FingerprintsPage from './pages/FingerprintsPage.jsx'
import CrowdsourcedFeedPage from './pages/CrowdsourcedFeedPage.jsx'

export default function App() {
  const { loggedIn } = useAuth()

  return (
    <>
      <Navbar />
      <main>
        <Routes>
          {/* Public Auth Routes */}
          <Route path="/login" element={loggedIn ? <Navigate to="/" replace /> : <LoginPage mode="login" />} />
          <Route path="/signup" element={loggedIn ? <Navigate to="/" replace /> : <SignupPage />} />

          {/* Protected Feature Routes (Require Login First) */}
          <Route path="/" element={loggedIn ? <CheckPage /> : <LoginPage mode="login" />} />
          <Route path="/offer-letter" element={loggedIn ? <OfferLetterPage /> : <LoginPage mode="login" />} />
          <Route path="/upi-check" element={loggedIn ? <UpiCheckerPage /> : <LoginPage mode="login" />} />
          <Route path="/fingerprints" element={loggedIn ? <FingerprintsPage /> : <LoginPage mode="login" />} />
          <Route path="/community-feed" element={loggedIn ? <CrowdsourcedFeedPage /> : <LoginPage mode="login" />} />
          <Route path="/whatsapp" element={loggedIn ? <WhatsAppBotPage /> : <LoginPage mode="login" />} />
          <Route path="/report" element={loggedIn ? <ReportPage /> : <LoginPage mode="login" />} />
          <Route path="/history" element={loggedIn ? <HistoryPage /> : <LoginPage mode="login" />} />
        </Routes>
      </main>
    </>
  )
}
