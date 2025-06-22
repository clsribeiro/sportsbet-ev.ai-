import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const AdminRoute = ({ children }) => {
  const { isAuthenticated, user, loading } = useAuth();

  // Enquanto o estado de autenticação está a ser verificado, mostra uma mensagem
  if (loading) {
    return <div>A verificar permissões de administrador...</div>;
  }

  // Se o utilizador estiver autenticado E for um superutilizador, renderiza a página de admin
  if (isAuthenticated && user?.is_superuser) {
    return children;
  }

  // Caso contrário, redireciona para a página inicial (Dashboard) ou para a página de login
  // Redirecionar para a raiz é uma boa prática para evitar mostrar páginas de "acesso negado".
  return <Navigate to="/" replace />;
};

export default AdminRoute;
