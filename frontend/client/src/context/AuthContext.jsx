import React, { createContext, useState, useContext, useEffect, useCallback, useRef } from 'react';
import { getMe, login as apiLogin } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);
  // --- NOVA LÓGICA DE PERMISSÕES ---
  const [permissions, setPermissions] = useState(new Set());
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [loading, setLoading] = useState(true);
  
  const [notifications, setNotifications] = useState([]);
  const websocket = useRef(null);

  const addNotification = (message, type = 'info') => {
    const newNotification = { id: Date.now(), message, type };
    setNotifications(prev => [...prev, newNotification]);
    setTimeout(() => {
      setNotifications(prev => prev.filter(n => n.id !== newNotification.id));
    }, 7000);
  };

  const processUserData = (userData) => {
    setUser(userData);
    if (userData && userData.roles) {
      // Extrai todas as permissões de todos os planos (roles) e armazena num Set para verificação rápida
      const userPermissions = new Set(
        userData.roles.flatMap(role => role.permissions.map(p => p.name))
      );
      setPermissions(userPermissions);
    } else {
      setPermissions(new Set());
    }
  };

  const loadUserFromToken = useCallback(async () => {
    if (token) {
      try {
        const userData = await getMe(token);
        processUserData(userData);
        setIsAuthenticated(true);
      } catch (error) {
        console.error("Falha ao carregar utilizador a partir do token", error);
        localStorage.removeItem('authToken');
        setToken(null); setUser(null); setPermissions(new Set()); setIsAuthenticated(false);
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
      setIsAuthenticated(true); // O useEffect irá tratar de carregar o utilizador e as permissões
    }
  };

  const logout = () => {
    if (websocket.current) websocket.current.close();
    localStorage.removeItem('authToken');
    setToken(null); setUser(null); setPermissions(new Set()); setIsAuthenticated(false);
  };
  
  const refreshUser = useCallback(async () => {
    setLoading(true);
    await loadUserFromToken();
  }, [loadUserFromToken]);

  const value = {
    token, user, isAuthenticated, loading, login, logout, refreshUser, notifications, permissions, // Adiciona permissões ao contexto
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  return context;
};
