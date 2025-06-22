import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getRoleDetails, getPermissions, updateRolePermissions } from '../services/api';

const AdminPlanDetailPage = () => {
  const { roleId } = useParams();
  const { token } = useAuth();

  const [role, setRole] = useState(null);
  const [allPermissions, setAllPermissions] = useState([]);
  const [selectedPermissions, setSelectedPermissions] = useState(new Set());

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    if (token && roleId) {
      try {
        setLoading(true);
        // Busca os detalhes do plano e todas as permissões disponíveis em paralelo
        const [roleData, permissionsData] = await Promise.all([
          getRoleDetails(token, roleId),
          getPermissions(token) // Precisamos da função que busca todas as permissões
        ]);

        setRole(roleData);
        setAllPermissions(permissionsData);
        // Inicializa as checkboxes com as permissões que o plano já possui
        setSelectedPermissions(new Set(roleData.permissions.map(p => p.id)));

      } catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError("Não foi possível carregar os dados. Verifique as suas permissões.");
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
      // Converte o Set de volta para uma lista de IDs e envia para a API
      const permissionIds = Array.from(selectedPermissions);
      await updateRolePermissions(token, roleId, permissionIds);
      alert('Permissões atualizadas com sucesso!');
      // Recarrega os dados para garantir que a UI está sincronizada
      fetchData();
    } catch (err) {
      console.error("Erro ao atualizar permissões:", err);
      setError("Não foi possível guardar as alterações.");
    }
  };

  if (loading) return <div>A carregar detalhes do plano...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!role) return <div>Plano não encontrado.</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <Link to="/admin/plans">&larr; Voltar para a Lista de Planos</Link>

      <h1 style={{ marginTop: '20px' }}>Gerir Plano: {role.display_name}</h1>
      <p>Selecione as permissões que este plano deve conceder aos seus utilizadores.</p>

      <div style={{ marginTop: '30px' }}>
        {allPermissions.map(permission => (
          <div key={permission.id} style={{ marginBottom: '10px', padding: '5px' }}>
            <label>
              <input
                type="checkbox"
                checked={selectedPermissions.has(permission.id)}
                onChange={() => handlePermissionChange(permission.id)}
                style={{ marginRight: '10px' }}
              />
              <strong>{permission.name}</strong> - <span>{permission.description}</span>
            </label>
          </div>
        ))}
      </div>

      <button 
        onClick={handleSaveChanges} 
        style={{ marginTop: '20px', padding: '10px 20px', fontSize: '1em' }}
      >
        Guardar Alterações
      </button>
    </div>
  );
};

export default AdminPlanDetailPage;