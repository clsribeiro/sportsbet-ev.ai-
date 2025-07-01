import React, { createContext, useState, useContext, useEffect, useCallback } from 'react';
import { getMe, login as apiLogin } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [loading, setLoading] = useState(true);

  const loadUserFromToken = useCallback(async () => {
    if (token) {
      try {
        const userData = await getMe(token);
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        console.error("Falha ao carregar utilizador a partir do token", error);
        localStorage.removeItem('authToken');
        setToken(null);
        setUser(null);
        setIsAuthenticated(false);
      }
    }
    setLoading(false);
  }, [token]);

  useEffect(() => {
    loadUserFromToken();
  }, [loadUserFromToken]);

  const login = async (email, password) => {
    const data = await apiLogin(email, password);
    if (data.access_token) {
      localStorage.setItem('authToken', data.access_token);
      setToken(data.access_token);
      setIsAuthenticated(true);
      return data;
    }
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    setToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };
  
  // --- FUNÇÃO MODIFICADA ---
  // Tornamos a função async e garantimos que ela espera pela conclusão
  const refreshUser = useCallback(async () => {
    setLoading(true);
    await loadUserFromToken();
  }, [loadUserFromToken]);

  const value = {
    token,
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    refreshUser, // Adiciona a função ao contexto
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  }
  return context;
};
