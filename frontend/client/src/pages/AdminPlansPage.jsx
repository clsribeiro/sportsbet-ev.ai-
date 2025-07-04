import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { getRoles, createRole, deleteRole } from '../services/api';
import { Link } from 'react-router-dom';
import './Admin.css';

const AdminPlansPage = () => {
  const { token } = useAuth();
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [newRoleName, setNewRoleName] = useState('');
  const [newRoleDisplayName, setNewRoleDisplayName] = useState('');
  const [formError, setFormError] = useState('');

  const fetchRoles = useCallback(async () => {
    if (token) {
      try {
        setLoading(true);
        const rolesData = await getRoles(token);
        setRoles(rolesData);
      } catch (err) {
        setError("Não foi possível carregar os planos.");
      } finally {
        setLoading(false);
      }
    }
  }, [token]);

  useEffect(() => {
    fetchRoles();
  }, [fetchRoles]);

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
        description: "Plano criado via painel de admin.",
      };
      await createRole(token, roleData);
      setNewRoleName('');
      setNewRoleDisplayName('');
      fetchRoles(); 
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Ocorreu um erro ao criar o plano.');
    }
  };

  const handleDeleteRole = async (roleId, roleName) => {
    if (window.confirm(`Tem a certeza de que quer apagar o plano "${roleName}"? Esta ação não pode ser desfeita.`)) {
      try {
        await deleteRole(token, roleId);
        fetchRoles(); // Atualiza a lista após apagar
      } catch (err) {
        console.error("Erro ao apagar o plano:", err);
        alert("Não foi possível apagar o plano.");
      }
    }
  };

  if (loading) return <div>A carregar planos...</div>;
  if (error) return <div className="error-message">{error}</div>;

  return (
    <div className="admin-page-container">
      <h1>Gestão de Planos (Roles)</h1>
      
      <div className="admin-form">
        <h2>Criar Novo Plano</h2>
        <form onSubmit={handleCreateRole}>
          <div className="form-group">
            <label htmlFor="newRoleDisplayName">Nome de Exibição (ex: +EV Starter)</label>
            <input
              type="text"
              id="newRoleDisplayName"
              value={newRoleDisplayName}
              onChange={(e) => setNewRoleDisplayName(e.target.value)}
            />
          </div>
          <div className="form-group">
            <label htmlFor="newRoleName">Nome Técnico (ex: plan_starter)</label>
            <input
              type="text"
              id="newRoleName"
              value={newRoleName}
              onChange={(e) => setNewRoleName(e.target.value)}
            />
          </div>
          {formError && <p className="error-message">{formError}</p>}
          <button type="submit">Criar Plano</button>
        </form>
      </div>

      <h2>Planos Existentes</h2>
      <table className="admin-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Nome de Exibição</th>
            <th>Nome Técnico</th>
            <th>Status</th>
            <th style={{ textAlign: 'center' }}>Ações</th>
          </tr>
        </thead>
        <tbody>
          {roles.map((role) => (
            <tr key={role.id}>
              <td>{role.id}</td>
              <td>{role.display_name}</td>
              <td><code>{role.name}</code></td>
              <td>{role.is_active ? 'Ativo' : 'Inativo'}</td>
              <td className="actions-cell">
                <Link to={`/admin/plans/${role.id}`} className="action-link edit">Editar / Gerir</Link>
                {role.name !== 'admin_full' && (
                  <button onClick={() => handleDeleteRole(role.id, role.display_name)} className="action-button delete">Apagar</button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AdminPlansPage;
