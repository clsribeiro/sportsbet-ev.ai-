import React from 'react';
import { Navigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useHasPermission } from '../hooks/useHasPermission'; // Importa o nosso novo hook

const PermissionProtectedRoute = ({ children, permission }) => {
  const { isAuthenticated, loading } = useAuth();
  const hasPermission = useHasPermission(permission);

  // Enquanto o estado de autenticação está a ser verificado, mostra uma mensagem
  if (loading) {
    return <div>A verificar permissões...</div>;
  }

  // Se não estiver autenticado, redireciona para a página de login
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Se estiver autenticado, mas não tiver a permissão necessária,
  // redireciona para o Dashboard. Poderíamos também mostrar uma página "Acesso Negado".
  if (!hasPermission) {
    console.warn(`Acesso negado à rota. Permissão necessária: ${permission}`);
    // Opcional: Mostrar um alerta ao utilizador
    // alert("Você não tem permissão para aceder a esta página. Considere fazer um upgrade do seu plano.");
    return <Navigate to="/" replace />;
  }

  // Se estiver autenticado e tiver a permissão, renderiza o componente filho
  return children;
};

export default PermissionProtectedRoute;
