import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Importação dos Hooks e Componentes de Autenticação/Layout
import { useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';
import MainLayout from './components/MainLayout';
import AdminLayout from './components/AdminLayout';
import NotificationContainer from './components/NotificationContainer';

// Importação de Todas as Páginas
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import GameDetailPage from './pages/GameDetailPage';
import PredictionsPage from './pages/PredictionsPage';
import ProfilePage from './pages/ProfilePage';
import BetTrackerPage from './pages/BetTrackerPage';
import AdminPlansPage from './pages/AdminPlansPage';
import AdminUserDetailPage from './pages/AdminUserDetailPage';
import AdminUsersPage from './pages/AdminUsersPage';
import AdminTasksPage from './pages/AdminTasksPage';
import AdminPlanDetailPage from './pages/AdminPlanDetailPage';

// Importação do CSS
import './App.css';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      {/* O NotificationContainer fica fora do Routes para ser exibido em todas as páginas */}
      <NotificationContainer />
      
      <Routes>
        <Route 
          path="/login" 
          element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} 
        />
        
        <Route 
          path="/" 
          element={<ProtectedRoute><MainLayout /></ProtectedRoute>}
        >
          <Route index element={<DashboardPage />} />
          <Route path="games/:gameId" element={<GameDetailPage />} />
          <Route path="predictions" element={<PredictionsPage />} />
          <Route path="profile" element={<ProfilePage />} />
          <Route path="bets" element={<BetTrackerPage />} />
        </Route>

        <Route 
          path="/admin" 
          element={<AdminRoute><AdminLayout /></AdminRoute>}
        >
          <Route index element={<Navigate to="users" replace />} />
          <Route path="users" element={<AdminUsersPage />} />
          <Route path="users/:userId" element={<AdminUserDetailPage />} />
          <Route path="plans" element={<AdminPlansPage />} />
          <Route path="plans/:roleId" element={<AdminPlanDetailPage />} />
          <Route path="tasks" element={<AdminTasksPage />} />
        </Route>
      </Routes>
    </Router>
  );
}

export default App;
