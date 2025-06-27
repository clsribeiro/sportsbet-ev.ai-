import React from 'react';
// Importe o Outlet e o Link do react-router-dom
import { Link, Outlet } from 'react-router-dom';

const AdminLayout = () => {
  return (
    <div style={{ display: 'flex' }}>
      {/* Menu de Navegação Lateral */}
      <nav style={{ width: '220px', background: '#1a1a1a', padding: '20px', minHeight: '100vh', borderRight: '1px solid #333' }}>
        <h2 style={{ color: 'white' }}>Painel Admin</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/admin/users" style={{ color: '#646cff', textDecoration: 'none', fontSize: '1.1em' }}>Gestão de Utilizadores</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/admin/plans" style={{ color: '#646cff', textDecoration: 'none', fontSize: '1.1em' }}>Gestão de Planos</Link>
          </li>
          <li style={{ marginBottom: '10px' }}>
            <Link to="/admin/tasks" style={{ color: '#646cff', textDecoration: 'none', fontSize: '1.1em' }}>Tarefas</Link>
          </li>
          {/* Adicionar mais links de admin aqui no futuro */}

        </ul>
        <hr style={{ borderColor: '#444', margin: '20px 0' }} />
        <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>
          &larr; Voltar ao Site Principal
        </Link>
      </nav>

      {/* Área de Conteúdo Principal */}
      <main style={{ flex: 1, padding: '20px', overflowY: 'auto' }}>
        {/* O Outlet é crucial! É aqui que o conteúdo da rota filha 
            (AdminUsersPage, AdminPlansPage, etc.) será renderizado. */}
        <Outlet /> 
      </main>
    </div>
  );
};

export default AdminLayout;
