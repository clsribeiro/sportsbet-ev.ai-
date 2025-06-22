import axios from 'axios';

// Cria uma instância do axios com configurações base.
// Isso nos permite definir a URL base da nossa API em um único lugar.
const api = axios.create({
  baseURL: 'http://192.168.100.169:8000/api/v1', // Use o IP do seu servidor Debian
});

/**
 * Função para realizar o login do usuário.
 * @param {string} email - O email do usuário (enviado como username).
 * @param {string} password - A senha do usuário.
 * @returns {Promise<object>} - A resposta da API com o token.
 */
export const login = async (email, password) => {
  // O endpoint de login espera dados de formulário (x-www-form-urlencoded).
  // Criamos um objeto URLSearchParams para formatar os dados corretamente.
  const params = new URLSearchParams();
  params.append('username', email);
  params.append('password', password);

  // Faz a requisição POST para o endpoint de login.
  const response = await api.post('/auth/login', params, {
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
  });
  return response.data; // Retorna os dados da resposta (ex: { access_token, token_type })
};

/**
 * Função para registrar um novo usuário.
 * @param {object} userData - Objeto com email, password, full_name.
 * @returns {Promise<object>} - A resposta da API com os dados do usuário criado.
 */
export const register = async (userData) => {
  // O endpoint de registro espera um corpo JSON.
  const response = await api.post('/users/', userData);
  return response.data;
};

/**
 * Função para buscar os dados do usuário logado.
 * @param {string} token - O token JWT de acesso.
 * @returns {Promise<object>} - A resposta da API com os dados do usuário.
 */
export const getMe = async (token) => {
  const response = await api.get('/users/me', {
    headers: {
      Authorization: `Bearer ${token}`, // Envia o token no cabeçalho de autorização
    },
  });
  return response.data;
};

/**
 * Busca a lista de jogos do dia.
 * @param {string} token - O token JWT de acesso.
 * @returns {Promise<Array>} - Uma lista de jogos.
 */
export const getGames = async (token) => {
  const response = await api.get('/games/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

/**
 * Busca os detalhes de um jogo específico.
 * @param {string} token - O token JWT de acesso.
 * @param {number} gameId - O ID do jogo.
 * @returns {Promise<object>} - Os detalhes do jogo.
 */
export const getGameDetails = async (token, gameId) => {
  const response = await api.get(`/games/${gameId}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

/**
 * Busca a lista de todos os Planos (Roles). Requer privilégios de admin.
 * @param {string} token - O token JWT de acesso.
 * @returns {Promise<Array>} - Uma lista de planos (roles).
 */
export const getRoles = async (token) => {
  const response = await api.get('/admin/roles/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

/**
 * Busca a lista de todas as Permissões. Requer privilégios de admin.
 * @param {string} token - O token JWT de acesso.
 * @returns {Promise<Array>} - Uma lista de permissões.
 */
export const getPermissions = async (token) => {
  const response = await api.get('/admin/permissions/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  return response.data;
};

// Podemos adicionar outras funções de API aqui no futuro...
export default api;
