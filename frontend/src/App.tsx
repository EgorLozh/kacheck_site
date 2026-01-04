import { Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider } from './contexts/AuthContext'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import TrainingsPage from './pages/TrainingsPage'
import TemplatesPage from './pages/TemplatesPage'
import ExercisesPage from './pages/ExercisesPage'
import AnalyticsPage from './pages/AnalyticsPage'
import ActiveTrainingPage from './pages/ActiveTrainingPage'
import CompletedTrainingPage from './pages/CompletedTrainingPage'
import SharedTrainingPage from './pages/SharedTrainingPage'
import FollowersPage from './pages/FollowersPage'
import FollowingPage from './pages/FollowingPage'
import UserProfilePage from './pages/UserProfilePage'
import Layout from './components/layout/Layout'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/trainings/active/:id" element={<ActiveTrainingPage />} />
        <Route path="/trainings/completed/:id" element={<CompletedTrainingPage />} />
        <Route path="/trainings/shared/:token" element={<SharedTrainingPage />} />
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<DashboardPage />} />
          <Route path="trainings" element={<TrainingsPage />} />
          <Route path="templates" element={<TemplatesPage />} />
          <Route path="exercises" element={<ExercisesPage />} />
          <Route path="analytics" element={<AnalyticsPage />} />
          <Route path="followers" element={<FollowersPage />} />
          <Route path="following" element={<FollowingPage />} />
          <Route path="users/:id" element={<UserProfilePage />} />
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App

