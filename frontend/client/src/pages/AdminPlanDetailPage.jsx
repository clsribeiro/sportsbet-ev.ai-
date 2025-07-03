import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getRoleDetails, getPermissions, updateRolePermissions } from '../services/api';
import './Admin.css'; // Importa um CSS partilhado para as páginas de admin

const AdminPlanDetailPage = () => {
  const { roleId } = useParams();
  const { token } = useAuth();
  
  const [role, setRole] = useState(null);
  const [allPermissions, setAllPermissions] = useState([]);
  const [selectedPermissions, setSelectedPermissions] = useState(new Set());
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [saveMessage, setSaveMessage] = useState('');

  // Agrupa as permissões por 'module_group' para uma melhor UI
  const groupedPermissions = useMemo(() => {
    return allPermissions.reduce((acc, permission) => {
      const group = permission.module_group || 'Geral';
      if (!acc[group]) {
        acc[group] = [];
      }
      acc[group].push(permission);
      return acc;
    }, {});
  }, [allPermissions]);

  const fetchData = useCallback(async () => {
    if (token && roleId) {
      try {
        setLoading(true);
        const [roleData, permissionsData] = await Promise.all([
          getRoleDetails(token, roleId),
          getPermissions(token)
        ]);
        setRole(roleData);
        setAllPermissions(permissionsData);
        setSelectedPermissions(new Set(roleData.permissions.map(p => p.id)));
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError("Não foi possível carregar os dados.");
      } finally {
        setLoading(false);
      }
    }
  }, [token, roleId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handlePermissionChange = (permissionId) => {
    setSelectedPermissions(prevSelected => {
      const newSelected = new Set(prevSelected);
      if (newSelected.has(permissionId)) {
        newSelected.delete(permissionId);
      } else {
        newSelected.add(permissionId);
      }
      return newSelected;
    });
  };

  const handleSaveChanges = async () => {
    try {
      setSaveMessage('');
      const permissionIds = Array.from(selectedPermissions);
      await updateRolePermissions(token, roleId, permissionIds);
      setSaveMessage('Permissões atualizadas com sucesso!');
      setTimeout(() => setSaveMessage(''), 4000);
    } catch (err) {
      console.error("Erro ao atualizar permissões:", err);
      setError("Não foi possível guardar as alterações.");
    }
  };

  if (loading) return <div>A carregar detalhes do plano...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!role) return <div>Plano não encontrado.</div>;

  return (
    <div className="admin-page-container">
      <Link to="/admin/plans">&larr; Voltar para a Lista de Planos</Link>
      
      <h1 style={{ marginTop: '20px' }}>Gerir Plano: {role.display_name}</h1>
      <p>Selecione as permissões que este plano deve conceder aos seus utilizadores.</p>

      <div className="permissions-grid">
        {Object.entries(groupedPermissions).map(([groupName, permissions]) => (
          <div key={groupName} className="permission-group">
            <h3>{groupName}</h3>
            {permissions.map(permission => (
              <div key={permission.id} className="permission-item">
                <label>
                  <input
                    type="checkbox"
                    checked={selectedPermissions.has(permission.id)}
                    onChange={() => handlePermissionChange(permission.id)}
                    disabled={role.name === 'admin_full'}
                  />
                  <span>{permission.description} (<code>{permission.name}</code>)</span>
                </label>
              </div>
            ))}
          </div>
        ))}
      </div>

      <button 
        onClick={handleSaveChanges} 
        disabled={role.name === 'admin_full'}
        className="save-button"
      >
        Guardar Alterações
      </button>
      {saveMessage && <p className="success-message">{saveMessage}</p>}
      {role.name === 'admin_full' && <p className="info-message">O plano de Administrador não pode ser alterado.</p>}
    </div>
  );
};

export default AdminPlanDetailPage;
