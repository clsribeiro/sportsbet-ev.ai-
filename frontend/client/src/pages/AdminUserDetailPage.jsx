import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getRoles, updateUserRoles, updateUserByAdmin, resetPasswordByAdmin, getAdminUserDetails } from '../services/api';
import './Admin.css';

const AdminUserDetailPage = () => {
  const { userId } = useParams();
  const { token } = useAuth();
  
  const [user, setUser] = useState(null);
  const [allRoles, setAllRoles] = useState([]);
  const [selectedRoleIds, setSelectedRoleIds] = useState(new Set());
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [message, setMessage] = useState('');

  // Estados para os formulários
  const [fullName, setFullName] = useState('');
  const [isActive, setIsActive] = useState(true);
  const [newPassword, setNewPassword] = useState('');

  // Função robusta para buscar todos os dados necessários para a página
  const fetchData = useCallback(async () => {
    if (token && userId) {
      try {
        setLoading(true);
        // Busca os detalhes do utilizador e a lista de todos os planos em paralelo
        const [userData, rolesData] = await Promise.all([
          getAdminUserDetails(token, userId),
          getRoles(token)
        ]);

        // Define os estados com os dados recebidos
        setUser(userData);
        setAllRoles(rolesData);
        setFullName(userData.full_name || '');
        setIsActive(userData.is_active);
        setSelectedRoleIds(new Set(userData.roles.map(r => r.id)));

      } catch (err) {
        console.error("Erro ao buscar dados:", err);
        setError("Não foi possível carregar os dados do utilizador.");
      } finally {
        setLoading(false);
      }
    }
  }, [token, userId]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);
  
  const handleRoleChange = (roleId) => {
    setSelectedRoleIds(prevSelected => {
      const newSelected = new Set(prevSelected);
      newSelected.has(roleId) ? newSelected.delete(roleId) : newSelected.add(roleId);
      return newSelected;
    });
  };

  const handleUpdateDetails = async (e) => {
    e.preventDefault();
    setMessage('');
    try {
      const updatedUser = await updateUserByAdmin(token, userId, { full_name: fullName, is_active: isActive });
      setUser(updatedUser); // Atualiza os dados do utilizador na página
      setMessage('Detalhes do utilizador atualizados com sucesso!');
      setTimeout(() => setMessage(''), 4000);
    } catch (err) {
      setError('Não foi possível atualizar os detalhes do utilizador.');
    }
  };

  const handleUpdateRoles = async () => {
    setMessage('');
    try {
      const roleIds = Array.from(selectedRoleIds);
      const updatedUser = await updateUserRoles(token, userId, roleIds);
      setUser(updatedUser);
      setMessage('Planos do utilizador atualizados com sucesso!');
      setTimeout(() => setMessage(''), 4000);
    } catch (err) {
      setError("Não foi possível guardar as alterações nos planos.");
    }
  };

  const handleResetPassword = async (e) => {
    e.preventDefault();
    if (!newPassword) return;
    if (window.confirm(`Tem a certeza de que quer redefinir a senha para "${user.email}"?`)) {
      try {
        await resetPasswordByAdmin(token, userId, newPassword);
        setMessage('Senha do utilizador redefinida com sucesso!');
        setNewPassword('');
        setTimeout(() => setMessage(''), 4000);
      } catch (err) {
        setError('Não foi possível redefinir a senha.');
      }
    }
  };

  if (loading) return <div>A carregar detalhes do utilizador...</div>;
  if (error) return <div className="error-message">{error}</div>;
  if (!user) return <div>Utilizador não encontrado. <Link to="/admin/users">Voltar</Link></div>;

  return (
    <div className="admin-page-container">
      <Link to="/admin/users">&larr; Voltar para a Lista de Utilizadores</Link>
      
      <h1 style={{ marginTop: '20px' }}>Gerir Utilizador: {user.email}</h1>
      {message && <p className="success-message">{message}</p>}

      <div className="admin-grid">
        <form onSubmit={handleUpdateDetails} className="admin-form">
          <h3>Detalhes do Utilizador</h3>
          <div className="form-group">
            <label>Nome Completo</label>
            <input type="text" value={fullName} onChange={(e) => setFullName(e.target.value)} />
          </div>
          <div className="form-group checkbox-group">
            <label>
              <input type="checkbox" checked={isActive} onChange={(e) => setIsActive(e.target.checked)} />
              Conta Ativa
            </label>
          </div>
          <button type="submit">Guardar Detalhes</button>
        </form>

        <div className="admin-form">
          <h3>Planos (Roles)</h3>
          <div className="permissions-container">
            {allRoles.map(role => (
              <div key={role.id} className="permission-item">
                <label>
                  <input
                    type="checkbox"
                    checked={selectedRoleIds.has(role.id)}
                    onChange={() => handleRoleChange(role.id)}
                    // Impede que um admin remova o seu próprio plano de admin
                    disabled={user.is_superuser && role.name === 'admin_full'}
                  />
                  <span>{role.display_name}</span>
                </label>
              </div>
            ))}
          </div>
          <button type="button" onClick={handleUpdateRoles} className="save-button">Guardar Planos</button>
        </div>

        <form onSubmit={handleResetPassword} className="admin-form">
          <h3>Redefinir Senha</h3>
          <div className="form-group">
            <label>Nova Senha</label>
            <input type="text" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} placeholder="Digite a nova senha aqui" />
          </div>
          <button type="submit" disabled={!newPassword}>Redefinir Senha</button>
        </form>
      </div>
    </div>
  );
};

export default AdminUserDetailPage;
