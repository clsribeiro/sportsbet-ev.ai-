import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getRoles, createRole } from '../services/api'; // Importa a nova função createRole
import { Link } from 'react-router-dom';

const AdminPlansPage = () => {
  const { token } = useAuth();
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Estado para o formulário de novo plano
  const [newRoleName, setNewRoleName] = useState('');
  const [newRoleDisplayName, setNewRoleDisplayName] = useState('');
  const [formError, setFormError] = useState('');

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

  useEffect(() => {
    if (token) {
      fetchRoles();
    }
  }, [token]);

  const handleCreateRole = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!newRoleName || !newRoleDisplayName) {
      setFormError('Ambos os nomes (técnico e de exibição) são obrigatórios.');
      return;
    }

    try {
      const roleData = {
        name: newRoleName,
        display_name: newRoleDisplayName,
        description: "Plano criado via painel de admin.", // Descrição padrão
      };
      await createRole(token, roleData);
      alert('Plano criado com sucesso!');
      // Limpa os campos e atualiza a lista
      setNewRoleName('');
      setNewRoleDisplayName('');
      fetchRoles(); 
    } catch (err) {
      console.error("Erro ao criar plano:", err);
      setFormError(err.response?.data?.detail || 'Ocorreu um erro ao criar o plano.');
    }
  };

  if (loading) return <div>A carregar planos...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '900px', margin: 'auto' }}>
      <Link to="/">&larr; Voltar ao Dashboard</Link>
      <h1 style={{ marginTop: '20px' }}>Gestão de Planos (Roles)</h1>

      {/* Formulário para Novo Plano */}
      <div style={{ padding: '15px', border: '1px solid #444', borderRadius: '8px', marginBottom: '30px' }}>
        <h2>Criar Novo Plano</h2>
        <form onSubmit={handleCreateRole}>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="displayName">Nome de Exibição (ex: +EV Starter):</label>
            <input
              type="text"
              id="displayName"
              value={newRoleDisplayName}
              onChange={(e) => setNewRoleDisplayName(e.target.value)}
              style={{ width: '100%', padding: '8px', background: '#333', border: '1px solid #555', color: 'white' }}
            />
          </div>
          <div style={{ marginBottom: '10px' }}>
            <label htmlFor="technicalName">Nome Técnico (ex: plan_starter):</label>
            <input
              type="text"
              id="technicalName"
              value={newRoleName}
              onChange={(e) => setNewRoleName(e.target.value)}
              style={{ width: '100%', padding: '8px', background: '#333', border: '1px solid #555', color: 'white' }}
            />
          </div>
          {formError && <p style={{ color: 'red' }}>{formError}</p>}
          <button type="submit" style={{ padding: '10px 15px' }}>Criar Plano</button>
        </form>
      </div>

      <h2>Planos Existentes</h2>
      <table style={{ width: '100%', marginTop: '20px', borderCollapse: 'collapse' }}>
        <thead>
          <tr style={{ borderBottom: '1px solid #444' }}>
            <th style={{ padding: '8px', textAlign: 'left' }}>ID</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Nome de Exibição</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Nome Técnico</th>
            <th style={{ padding: '8px', textAlign: 'left' }}>Status</th>
            {/* --- NOVA COLUNA --- */}
            <th style={{ padding: '8px', textAlign: 'center' }}>Ações</th> 
          </tr>
        </thead>
        <tbody>
          {roles.map((role) => (
            <tr key={role.id} style={{ borderBottom: '1px solid #333' }}>
              <td style={{ padding: '8px' }}>{role.id}</td>
              <td style={{ padding: '8px' }}>{role.display_name}</td>
              <td style={{ padding: '8px' }}><code>{role.name}</code></td>
              <td style={{ padding: '8px' }}>{role.is_active ? 'Ativo' : 'Inativo'}</td>
              {/* --- NOVA CÉLULA COM O LINK --- */}
              <td style={{ padding: '8px', textAlign: 'center' }}>
                <Link 
                  to={`/admin/plans/${role.id}`}
                  style={{ textDecoration: 'none', color: '#646cff', fontWeight: 'bold' }}
                >
                  Gerir Permissões
                </Link>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPlansPage;
