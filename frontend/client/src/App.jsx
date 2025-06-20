import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import DashboardPage from './pages/DashboardPage';
import GameDetailPage from './pages/GameDetailPage'; // Importa a nova página
import ProtectedRoute from './components/ProtectedRoute';
import { useAuth } from './context/AuthContext';
import './App.css';

function App() {
  const { isAuthenticated } = useAuth();

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/login" element={isAuthenticated ? <Navigate to="/" /> : <LoginPage />} />

          {/* Rota Raiz ('/'): Protegida, leva ao Dashboard */}
          <Route
            path="/"
            element={
              <ProtectedRoute>
                <DashboardPage />
              </ProtectedRoute>
            }
          />

          {/* NOVA ROTA para Detalhes do Jogo */}
          <Route
            path="/games/:gameId" // O :gameId é um parâmetro dinâmico
            element={
              <ProtectedRoute>
                <GameDetailPage />
              </ProtectedRoute>
            }
          />

        </Routes>
      </div>
    </Router>
  );
}

export default App;
