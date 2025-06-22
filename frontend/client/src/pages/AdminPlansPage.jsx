import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getRoles } from '../services/api'; // Importa a nossa nova função
import { Link } from 'react-router-dom';

const AdminPlansPage = () => {
  const { token } = useAuth();
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) {
      const fetchRoles = async () => {
        try {
          setLoading(true);
          const rolesData = await getRoles(token);
          setRoles(rolesData);
        } catch (err) {
          console.error("Erro ao buscar planos:", err);
          setError("Não foi possível carregar os planos. Verifique se tem permissões de administrador.");
        } finally {
          setLoading(false);
        }
      };
      fetchRoles();
    }
  }, [token]);

  if (loading) return <div>A carregar planos...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <Link to="/">&larr; Voltar ao Dashboard</Link>
      <h1 style={{ marginTop: '20px' }}>Gestão de Planos (Roles)</h1>
      <p>Esta página lista todos os planos de assinatura disponíveis no sistema.</p>

      <table style={{ width: '100%', marginTop: '20px', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #444' }}>
            <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Nome de Exibição</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Nome Técnico</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Status</th>
          </tr>
        </thead>
        <tbody>
          {roles.map((role) => (
            <tr key={role.id} style={{ borderBottom: '1px solid #333' }}>
              <td style={{ padding: '8px' }}>{role.id}</td>
              <td style={{ padding: '8px' }}>{role.display_name}</td>
              <td style={{ padding: '8px' }}><code>{role.name}</code></td>
              <td style={{ padding: '8px' }}>{role.is_active ? 'Ativo' : 'Inativo'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPlansPage;
