import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getUsers } from '../services/api';
import { Link } from 'react-router-dom';

const AdminUsersPage = () => {
  const { token } = useAuth();
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) {
      const fetchUsers = async () => {
        try {
          setLoading(true);
          const usersData = await getUsers(token);
          setUsers(usersData);
        } catch (err) {
          console.error("Erro ao buscar utilizadores:", err);
          setError("Não foi possível carregar os utilizadores.");
        } finally {
          setLoading(false);
        }
      };
      fetchUsers();
    }
  }, [token]);

  if (loading) return <div>A carregar utilizadores...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: 'auto' }}>
      <Link to="/">&larr; Voltar ao Dashboard</Link>
      <h1 style={{ marginTop: '20px' }}>Gestão de Utilizadores</h1>

      <table style={{ width: '100%', marginTop: '20px', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #444' }}>
            <th style={{ padding: '8px', textAlign: 'left' }}>Email</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Nome Completo</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Planos Atuais</th>
            <th style={{ padding: '8px', textAlign: 'center' }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id} style={{ borderBottom: '1px solid #333' }}>
              <td style={{ padding: '8px' }}>{user.email}</td>
              <td style={{ padding: '8px' }}>{user.full_name || 'N/A'}</td>
              <td style={{ padding: '8px' }}>
                {user.roles.map(role => role.display_name).join(', ') || 'Nenhum'}
              </td>
              <td style={{ padding: '8px', textAlign: 'center' }}>
              <Link 
                to={`/admin/users/${user.id}`}
                state={{ user: user }} // Passa o objeto completo do utilizador
                style={{ textDecoration: 'none', color: '#646cff', fontWeight: 'bold' }}
              >
                Gerir Planos
              </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminUsersPage;
