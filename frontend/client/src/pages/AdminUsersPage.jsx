import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getUsers } from '../services/api';
import { Link } from 'react-router-dom';
import './Admin.css'; // Usa o mesmo ficheiro de estilos

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
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="admin-page-container">
      <h1>Gestão de Utilizadores</h1>
      
      <table className="admin-table">
        <thead>
          <tr>
            <th>Email</th>
            <th>Nome Completo</th>
            <th>Planos Atribuídos</th>
            <th style={{ textAlign: 'center' }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {users.map((user) => (
            <tr key={user.id}>
              <td>{user.email} {user.is_superuser && <span className="admin-badge">Admin</span>}</td>
              <td>{user.full_name || 'N/A'}</td>
              <td>
                {user.roles.length > 0 
                  ? user.roles.map(role => role.display_name).join(', ')
                  : 'Nenhum'
                }
                <span className="count-badge">{user.roles.length}</span>
              </td>
              <td style={{ textAlign: 'center' }}>
                <Link 
                  to={`/admin/users/${user.id}`}
                  state={{ user: user }}
                  className="action-link"
                >
                  Gerir
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
