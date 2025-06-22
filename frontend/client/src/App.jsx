import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import GameDetailPage from './pages/GameDetailPage';
import AdminPlansPage from './pages/AdminPlansPage';
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';
import { useAuth } from './context/AuthContext';
import AdminPlanDetailPage from './pages/AdminPlanDetailPage'; 
import './App.css';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Rota de Login: se já estiver autenticado, redireciona para o dashboard */}
          <Route 
            path="/login" 
            element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} 
          />

          {/* Rota Raiz ('/'): Protegida, leva ao Dashboard */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />

          {/* Rota para Detalhes do Jogo */}
          <Route
            path="/games/:gameId" // O :gameId é um parâmetro dinâmico
            element={
              <ProtectedRoute>
                <GameDetailPage />
              </ProtectedRoute>
            }
          />

          {/* ROTA DE ADMIN */}
          <Route
            path="/admin/plans"
            element={
              <AdminRoute>
                <AdminPlansPage />
              </AdminRoute>
            }
          />
          {/* --- NOVA ROTA DINÂMICA DE ADMIN --- */}
          <Route
            path="/admin/plans/:roleId" // :roleId é um parâmetro dinâmico
            element={
              <AdminRoute>
                <AdminPlanDetailPage />
              </AdminRoute>
            }
          />
        </Routes>
      </div>
    </Router>
  );
}

export default App;