import React from 'react';
import { useAuth } from '../context/AuthContext'; // Importa o nosso hook de autenticação

const DashboardPage = () => {
  // Obtém os dados do utilizador e a função de logout do contexto
  const { user, logout } = useAuth();

  return (
    <div style={{ padding: '20px' }}>
      <h1>Dashboard - Bem-vindo à Plataforma!</h1>
      {user ? (
        <div>
          <p>Você está autenticado como: <strong>{user.email}</strong></p>
          <p>Nome Completo: {user.full_name || 'Não informado'}</p>
          <p>ID do Utilizador: {user.id}</p>
          <button onClick={logout} style={{ padding: '10px', marginTop: '20px' }}>
            Sair (Logout)
          </button>
        </div>
      ) : (
        <p>A carregar dados do utilizador...</p>
      )}
    </div>
  );
};

export default DashboardPage;
