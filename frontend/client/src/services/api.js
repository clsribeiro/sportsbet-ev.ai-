import axios from 'axios';

// Cria uma instância do axios com configurações base.
const api = axios.create({
  baseURL: 'http://192.168.100.169:8000/api/v1', // Use o IP do seu servidor Debian
});

// --- Funções de Autenticação e Utilizador ---

export const login = async (email, password) => {
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);
  const response = await api.post('/auth/login', params, {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  });
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/users/', userData);
  return response.data;
};

export const getMe = async (token) => {
  const response = await api.get('/users/me', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const updateMe = async (token, userData) => {
  const response = await api.put('/users/me', userData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const updatePassword = async (token, passwordData) => {
  await api.post('/users/me/password', passwordData, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

// --- Funções de Dados (Jogos e Previsões) ---

export const getGames = async (token, timeFilter = 'upcoming') => {
  const response = await api.get('/games/', {
    headers: { Authorization: `Bearer ${token}` },
    params: { time_filter: timeFilter }
  });
  return response.data;
};

export const getGameDetails = async (token, gameId) => {
  const response = await api.get(`/games/${gameId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const generatePrediction = async (token, gameId) => {
  const response = await api.post(`/games/${gameId}/predict`, {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const getPredictions = async (token) => {
  const response = await api.get('/predictions/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

// --- Funções do Bet Tracker ---

export const getUserBets = async (token) => {
  const response = await api.get('/bets/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const createBet = async (token, betData) => {
  const response = await api.post('/bets/', betData, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const updateBet = async (token, betId, status) => {
  const response = await api.put(`/bets/${betId}`, 
    { status: status },
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
  return response.data;
};

export const deleteBet = async (token, betId) => {
  await api.delete(`/bets/${betId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};


// --- Funções de ADMINISTRAÇÃO ---

export const runPreAnalysisTask = async (token) => {
  const response = await api.post('/admin/tasks/run-pre-analysis', {}, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const sendBroadcastTest = async (token, message) => {
  const response = await api.post('/admin/tasks/broadcast-test', 
    { message: message },
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
  return response.data;
};

export const getRoles = async (token) => {
  const response = await api.get('/admin/roles/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const createRole = async (token, roleData) => {
  const response = await api.post('/admin/roles/', roleData, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

export const getRoleDetails = async (token, roleId) => {
  const response = await api.get(`/admin/roles/${roleId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const updateRole = async (token, roleId, roleData) => {
  const response = await api.put(`/admin/roles/${roleId}`, roleData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const deleteRole = async (token, roleId) => {
  await api.delete(`/admin/roles/${roleId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
};

export const getPermissions = async (token) => {
  const response = await api.get('/admin/permissions/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const updateRolePermissions = async (token, roleId, permissionIds) => {
  const response = await api.put(`/admin/roles/${roleId}/permissions`, 
    { permission_ids: permissionIds },
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
  return response.data;
};

export const getUsers = async (token) => {
  const response = await api.get('/admin/users/', {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const getAdminUserDetails = async (token, userId) => {
  const response = await api.get(`/admin/users/${userId}`, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const updateUserRoles = async (token, userId, roleIds) => {
  const response = await api.put(`/admin/users/${userId}/roles`,
    { role_ids: roleIds },
    {
      headers: { Authorization: `Bearer ${token}` },
    }
  );
  return response.data;
};

export const updateUserByAdmin = async (token, userId, userData) => {
  const response = await api.put(`/admin/users/${userId}`, userData, {
    headers: { Authorization: `Bearer ${token}` },
  });
  return response.data;
};

export const resetPasswordByAdmin = async (token, userId, newPassword) => {
  await api.post(`/admin/users/${userId}/password-reset`, { new_password: newPassword }, {
    headers: { Authorization: `Bearer ${token}` },
  });
};


export default api;
