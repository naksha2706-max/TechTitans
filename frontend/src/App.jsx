import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar.jsx'
import CheckPage from './pages/CheckPage.jsx'
import HistoryPage from './pages/HistoryPage.jsx'
import ReportPage from './pages/ReportPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import SignupPage from './pages/SignupPage.jsx'

export default function App() {
  return (
    <>
      <Navbar />
      <main>
        <Routes>
          {/* Phase 2 — core scanner, no login required */}
          <Route path="/" element={<CheckPage />} />

          {/* Phase 3 — reporting */}
          <Route path="/report" element={<ReportPage />} />

          {/* Phase 1 — auth */}
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />

          {/* Phase 2 — history, requires login (guarded inside the page) */}
          <Route path="/history" element={<HistoryPage />} />
        </Routes>
      </main>
    </>
  )
}
