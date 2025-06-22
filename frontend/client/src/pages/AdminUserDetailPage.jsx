import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getRoles, updateUserRoles } from '../services/api';

const AdminUserDetailPage = () => {
  const { userId } = useParams();
  // Usamos useLocation para receber os dados do utilizador passados pela página anterior
  const location = useLocation();
  const { user: initialUserData } = location.state || {};

  const { token } = useAuth();
  const [user, setUser] = useState(initialUserData);
  const [allRoles, setAllRoles] = useState([]);
  const [selectedRoles, setSelectedRoles] = useState(new Set());

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const fetchData = useCallback(async () => {
    if (token && user) {
      try {
        setLoading(true);
        const rolesData = await getRoles(token);
        setAllRoles(rolesData);
        // Inicializa as checkboxes com os planos que o utilizador já possui
        setSelectedRoles(new Set(user.roles.map(r => r.id)));
      } catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError("Não foi possível carregar os planos.");
      } finally {
        setLoading(false);
      }
    } else if (!user) {
        setError("Dados do utilizador não encontrados. Por favor, volte à lista.");
        setLoading(false);
    }
  }, [token, user]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleRoleChange = (roleId) => {
    setSelectedRoles(prevSelected => {
      const newSelected = new Set(prevSelected);
      if (newSelected.has(roleId)) {
        newSelected.delete(roleId);
      } else {
        newSelected.add(roleId);
      }
      return newSelected;
    });
  };

  const handleSaveChanges = async () => {
    try {
      const roleIds = Array.from(selectedRoles);
      const updatedUser = await updateUserRoles(token, userId, roleIds);
      setUser(updatedUser); // Atualiza os dados do utilizador na página
      alert('Planos do utilizador atualizados com sucesso!');
    } catch (err) {
      console.error("Erro ao atualizar planos:", err);
      setError("Não foi possível guardar as alterações.");
    }
  };

  if (loading) return <div>A carregar detalhes do utilizador...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div>
      <Link to="/admin/users">&larr; Voltar para a Lista de Utilizadores</Link>

      <h1 style={{ marginTop: '20px' }}>Gerir Planos para: {user?.email}</h1>
      <p>Selecione os planos (roles) que este utilizador deve possuir.</p>

      <div style={{ marginTop: '30px' }}>
        {allRoles.map(role => (
          <div key={role.id} style={{ marginBottom: '10px', padding: '5px' }}>
            <label>
              <input
                type="checkbox"
                checked={selectedRoles.has(role.id)}
                onChange={() => handleRoleChange(role.id)}
                style={{ marginRight: '10px' }}
                // Não permite que o admin remova a si mesmo do plano de admin
                disabled={user?.is_superuser && role.name === 'admin_full'}
              />
              <strong>{role.display_name}</strong> (<code>{role.name}</code>)
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

export default AdminUserDetailPage;
