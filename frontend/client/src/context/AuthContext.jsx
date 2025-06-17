import React, { createContext, useState, useContext, useEffect } from 'react';
import { login as apiLogin, getMe } from '../services/api'; // Importa as nossas funções da API

// 1. Criar o Contexto
const AuthContext = createContext(null);

// 2. Criar o Provedor do Contexto (o componente que vai gerir o estado)
export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken')); // Lê o token do localStorage ao iniciar
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [loading, setLoading] = useState(true);

  // Efeito para carregar os dados do utilizador se um token existir no início
  useEffect(() => {
    const loadUserFromToken = async () => {
      if (token) {
        try {
          const userData = await getMe(token);
          setUser(userData);
          setIsAuthenticated(true);
        } catch (error) {
          console.error("Falha ao carregar utilizador a partir do token", error);
          // Limpa o token se for inválido
          localStorage.removeItem('authToken');
          setToken(null);
          setIsAuthenticated(false);
        }
      }
      setLoading(false);
    };
    loadUserFromToken();
  }, [token]); // Executa sempre que o token mudar

  // Função de login que será usada pelos componentes
  const login = async (email, password) => {
    const data = await apiLogin(email, password);
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token); // Guarda o token no localStorage
      setToken(data.access_token);
      setIsAuthenticated(true);
      return data;
    }
  };

  // Função de logout
  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  // Valor que será fornecido a todos os componentes filhos
  const value = {
    token,
    user,
    isAuthenticated,
    loading,
    login,
    logout,
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// 3. Criar um Hook customizado para usar o contexto mais facilmente
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};
