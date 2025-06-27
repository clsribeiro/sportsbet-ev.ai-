import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';

// Importação dos Hooks e Componentes de Autenticação/Layout
import { useAuth } from './context/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import AdminRoute from './components/AdminRoute';
import AdminLayout from './components/AdminLayout';

// Importação das Páginas
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import GameDetailPage from './pages/GameDetailPage';
import PredictionsPage from './pages/PredictionsPage'; // Página de Dicas da IA
import AdminPlansPage from './pages/AdminPlansPage';
import AdminUsersPage from './pages/AdminUsersPage';
import AdminUserDetailPage from './pages/AdminUserDetailPage';
import AdminTasksPage from './pages/AdminTasksPage'; // Página de Tarefas do Admin

// Importação do CSS
import './App.css';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Rota de Login: se o utilizador já estiver autenticado, redireciona para o dashboard */}
          <Route 
            path="/login" 
            element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} 
          />
          
          {/* --- Rotas para Utilizadores Autenticados --- */}
          <Route path="/" element={<ProtectedRoute><DashboardPage /></ProtectedRoute>} />
          <Route path="/games/:gameId" element={<ProtectedRoute><GameDetailPage /></ProtectedRoute>} />
          <Route path="/predictions" element={<ProtectedRoute><PredictionsPage /></ProtectedRoute>} />


          {/* --- Rotas de Administração Agrupadas --- */}
          {/* A rota pai /admin é protegida pela AdminRoute e renderiza o AdminLayout */}
          <Route 
            path="/admin" 
            element={
              <AdminRoute>
                <AdminLayout />
              </AdminRoute>
            }
          >
            {/* As rotas filhas são renderizadas dentro do <Outlet /> do AdminLayout */}
            <Route path="users" element={<AdminUsersPage />} />
            <Route path="users/:userId" element={<AdminUserDetailPage />} />
            <Route path="plans" element={<AdminPlansPage />} />
            <Route path="tasks" element={<AdminTasksPage />} />
          </Route>
          
        </Routes>
      </div>
    </Router>
  );
}

export default App;
