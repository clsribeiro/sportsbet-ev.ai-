import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { updateMe, updatePassword } from '../services/api';
import './ProfilePage.css'; // Vamos criar este ficheiro de estilos

const ProfilePage = () => {
  const { user, token, refreshUser } = useAuth();
  
  // Estado para o formulário de perfil
  const [fullName, setFullName] = useState(user?.full_name || '');
  const [profileMessage, setProfileMessage] = useState({ type: '', text: '' });

  // Estado para o formulário de senha
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [passwordMessage, setPasswordMessage] = useState({ type: '', text: '' });

  const handleUpdateProfile = async (e) => {
    e.preventDefault();
    setProfileMessage({ type: '', text: '' });
    try {
      await updateMe(token, { full_name: fullName });
      setProfileMessage({ type: 'success', text: 'Perfil atualizado com sucesso!' });
      if (refreshUser) await refreshUser(); // Atualiza o nome na Navbar
      setTimeout(() => setProfileMessage({ type: '', text: '' }), 4000);
    } catch (error) {
      setProfileMessage({ type: 'error', text: 'Falha ao atualizar o perfil.' });
    }
  };
  
  const handleUpdatePassword = async (e) => {
    e.preventDefault();
    if (newPassword !== confirmPassword) {
      setPasswordMessage({ type: 'error', text: 'As novas senhas não coincidem.' });
      return;
    }
    try {
      await updatePassword(token, { current_password: currentPassword, new_password: newPassword });
      setPasswordMessage({ type: 'success', text: 'Senha alterada com sucesso!' });
      // Limpa os campos após o sucesso
      setCurrentPassword('');
      setNewPassword('');
      setConfirmPassword('');
      setTimeout(() => setPasswordMessage({ type: '', text: '' }), 4000);
    } catch (error) {
      setPasswordMessage({ type: 'error', text: error.response?.data?.detail || 'Falha ao alterar a senha.' });
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
        <button type="submit">Guardar Detalhes</button>
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
        <button type="submit">Alterar Senha</button>
        {passwordMessage.text && <p className={`message ${passwordMessage.type}`}>{passwordMessage.text}</p>}
      </form>
    </div>
  );
};

export default ProfilePage;
