import React, { createContext, useState, useContext, useEffect, useCallback, useRef } from 'react';
import { getMe, login as apiLogin } from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem('authToken'));
  const [user, setUser] = useState(null);
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

  useEffect(() => {
    if (isAuthenticated && token) {
      if (websocket.current?.readyState === WebSocket.OPEN) return;

      const wsUrl = `ws://192.168.100.169:8000/ws`;
      websocket.current = new WebSocket(wsUrl);

      websocket.current.onopen = () => {
        console.log("Conexão WebSocket aberta. A enviar token para autenticação...");
        const authMessage = { type: "auth", token: token };
        websocket.current.send(JSON.stringify(authMessage));
      };

      websocket.current.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("Mensagem recebida do WebSocket:", data);
          const message = data.message || 'Mensagem desconhecida';
          const type = data.type || 'info'; // Obtém o tipo da mensagem
          addNotification(message, type);
        } catch (e) {
          addNotification(event.data, 'info');
        }
      };

      websocket.current.onclose = (event) => console.log(`Conexão WebSocket fechada: Code ${event.code}`);
      websocket.current.onerror = (error) => console.error("Erro no WebSocket:", error);

    } else if (websocket.current) {
      websocket.current.close();
      websocket.current = null;
    }
    return () => {
      if (websocket.current) websocket.current.close();
    };
  }, [isAuthenticated, token]);

  const loadUserFromToken = useCallback(async () => {
    if (token) {
      try {
        const userData = await getMe(token);
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        localStorage.removeItem('authToken');
        setToken(null); setUser(null); setIsAuthenticated(false);
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
    }
  };

  const logout = () => {
    if (websocket.current) websocket.current.close();
    localStorage.removeItem('authToken');
    setToken(null); setUser(null); setIsAuthenticated(false);
  };
  
  const refreshUser = useCallback(async () => {
    setLoading(true);
    await loadUserFromToken();
  }, [loadUserFromToken]);

  const value = {
    token, user, isAuthenticated, loading, login, logout, refreshUser, notifications,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth deve ser usado dentro de um AuthProvider');
  return context;
};
