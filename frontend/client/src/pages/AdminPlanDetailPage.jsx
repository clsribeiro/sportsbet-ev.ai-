import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getRoleDetails, getPermissions, updateRolePermissions, updateRole } from '../services/api';
import './Admin.css';

const AdminPlanDetailPage = () => {
  const { roleId } = useParams();
  const { token } = useAuth();
  
  const [role, setRole] = useState(null);
  const [displayName, setDisplayName] = useState('');
  const [description, setDescription] = useState('');
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
        setDisplayName(roleData.display_name);
        setDescription(roleData.description || '');
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
      // Atualiza tanto os detalhes do plano como as permissões
      await updateRole(token, roleId, { display_name: displayName, description: description });
      const permissionIds = Array.from(selectedPermissions);
      await updateRolePermissions(token, roleId, permissionIds);
      
      setSaveMessage('Alterações guardadas com sucesso!');
      setTimeout(() => setSaveMessage(''), 4000);
      fetchData(); // Recarrega os dados para garantir consistência
    } catch (err) {
      console.error("Erro ao guardar alterações:", err);
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
      
      <div className="admin-grid">
        <form onSubmit={(e) => e.preventDefault()} className="admin-form">
          <h3>Detalhes do Plano</h3>
          <div className="form-group">
            <label htmlFor="displayName">Nome de Exibição</label>
            <input
              id="displayName"
              type="text"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              disabled={role.name === 'admin_full'}
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Descrição</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={role.name === 'admin_full'}
              rows={4}
            />
          </div>
        </form>

        <div className="admin-form">
          <h3>Permissões do Plano</h3>
          <div className="permissions-container">
            {Object.entries(groupedPermissions).map(([groupName, permissions]) => (
              <div key={groupName} className="permission-group">
                <h4>{groupName}</h4>
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
        </div>
      </div>

      <div style={{marginTop: '2rem', textAlign: 'right'}}>
        <button 
          onClick={handleSaveChanges} 
          disabled={role.name === 'admin_full'}
          className="save-button"
        >
          Guardar Todas as Alterações
        </button>
        {saveMessage && <p className="success-message">{saveMessage}</p>}
        {role.name === 'admin_full' && <p className="info-message">O plano de Administrador não pode ser alterado.</p>}
      </div>
    </div>
  );
};

export default AdminPlanDetailPage;
