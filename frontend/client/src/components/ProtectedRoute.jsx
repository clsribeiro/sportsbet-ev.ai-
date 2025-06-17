import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();

  // Enquanto o estado de autenticação está a ser verificado, não renderiza nada
  if (loading) {
    return <div>A verificar autenticação...</div>;
  }

  // Se não estiver autenticado, redireciona para a página de login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Se estiver autenticado, renderiza o componente filho (a página protegida)
  return children;
};

export default ProtectedRoute;
