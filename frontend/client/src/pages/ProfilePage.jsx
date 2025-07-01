import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { updateMe, updatePassword } from '../services/api';
import './ProfilePage.css';

const ProfilePage = () => {
  const { user, token, refreshUser } = useAuth();
  
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [profileLoading, setProfileLoading] = useState(false);
  const [profileMessage, setProfileMessage] = useState({ type: '', text: '' });

  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordLoading, setPasswordLoading] = useState(false);
  const [passwordMessage, setPasswordMessage] = useState({ type: '', text: '' });

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setProfileLoading(true);
    setProfileMessage({ type: '', text: '' });
    try {
      await updateMe(token, { full_name: fullName });
      setProfileMessage({ type: 'success', text: 'Dados do perfil atualizados com sucesso!' });
      
      // Espera que a atualização do utilizador no contexto termine
      if (refreshUser) {
        await refreshUser();
      }

      // Limpa a mensagem de sucesso após 4 segundos
      setTimeout(() => setProfileMessage({ type: '', text: '' }), 4000);
    } catch (error) {
      console.error("Erro ao atualizar perfil:", error);
      setProfileMessage({ type: 'error', text: 'Falha ao atualizar o perfil.' });
    } finally {
      setProfileLoading(false);
    }
  };
  
  const handleUpdatePassword = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setPasswordMessage({ type: 'error', text: 'As novas senhas não coincidem.' });
      return;
    }
    setPasswordLoading(true);
    setPasswordMessage({ type: '', text: '' });
    try {
      await updatePassword(token, { current_password: currentPassword, new_password: newPassword });
      setPasswordMessage({ type: 'success', text: 'Senha alterada com sucesso!' });
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setPasswordMessage({ type: '', text: '' }), 4000);
    } catch (error) {
      console.error("Erro ao alterar senha:", error);
      setPasswordMessage({ type: 'error', text: error.response?.data?.detail || 'Falha ao alterar a senha.' });
    } finally {
      setPasswordLoading(false);
    }
  };

  return (
    <div className="profile-container">
      <h1>O Meu Perfil</h1>
      
      <form onSubmit={handleUpdateProfile} className="profile-form">
        <h2>Detalhes Pessoais</h2>
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input type="email" id="email" value={user?.email || ''} disabled />
        </div>
        <div className="form-group">
          <label htmlFor="fullName">Nome Completo</label>
          <input type="text" id="fullName" value={fullName} onChange={(e) => setFullName(e.target.value)} />
        </div>
        <button type="submit" disabled={profileLoading}>
          {profileLoading ? 'A guardar...' : 'Guardar Detalhes'}
        </button>
        {profileMessage.text && <p className={`message ${profileMessage.type}`}>{profileMessage.text}</p>}
      </form>

      <form onSubmit={handleUpdatePassword} className="profile-form">
        <h2>Alterar Senha</h2>
        <div className="form-group">
          <label htmlFor="currentPassword">Senha Atual</label>
          <input type="password" id="currentPassword" value={currentPassword} onChange={(e) => setCurrentPassword(e.target.value)} required />
        </div>
        <div className="form-group">
          <label htmlFor="newPassword">Nova Senha</label>
          <input type="password" id="newPassword" value={newPassword} onChange={(e) => setNewPassword(e.target.value)} required />
        </div>
        <div className="form-group">
          <label htmlFor="confirmPassword">Confirmar Nova Senha</label>
          <input type="password" id="confirmPassword" value={confirmPassword} onChange={(e) => setConfirmPassword(e.target.value)} required />
        </div>
        <button type="submit" disabled={passwordLoading}>
          {passwordLoading ? 'A alterar...' : 'Alterar Senha'}
        </button>
        {passwordMessage.text && <p className={`message ${passwordMessage.type}`}>{passwordMessage.text}</p>}
      </form>
    </div>
  );
};

export default ProfilePage;
