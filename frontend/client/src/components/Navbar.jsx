import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();

  const navLinkStyles = ({ isActive }) => {
    return {
      fontWeight: isActive ? 'bold' : 'normal',
      textDecoration: 'none',
      color: isActive ? '#818cf8' : 'white',
      padding: '10px 15px',
      borderRadius: '4px',
      transition: 'background-color 0.2s',
    };
  };

  return (
    <header style={{ 
      display: 'flex', 
      justifyContent: 'space-between', 
      alignItems: 'center', 
      padding: '1rem 2rem', 
      backgroundColor: '#1a1a1a',
      borderBottom: '1px solid #333'
    }}>
      <Link to="/" style={{ textDecoration: 'none', color: 'white', fontSize: '1.5rem', fontWeight: 'bold' }}>
        SportsBet <span style={{ color: '#818cf8' }}>+EV AI</span>
      </Link>
      <nav style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
        {isAuthenticated ? (
          <>
            <NavLink to="/" style={navLinkStyles}>Dashboard</NavLink>
            <NavLink to="/predictions" style={navLinkStyles}>Dicas da IA</NavLink>
            
            {user && user.is_superuser && (
              <NavLink to="/admin/users" style={navLinkStyles}>Admin</NavLink>
            )}

            <span style={{ color: '#ccc', margin: '0 10px' }}>|</span>
            
            <span style={{ color: 'white', marginRight: '15px' }}>
              Olá, {user ? (user.full_name || user.email) : ''}
            </span>

            <button onClick={logout} style={{ 
              padding: '8px 15px', 
              background: 'transparent', 
              color: '#ff8a80', 
              border: '1px solid #ff8a80',
              borderRadius: '4px',
              cursor: 'pointer'
            }}>
              Sair
            </button>
          </>
        ) : (
          <NavLink to="/login" style={navLinkStyles}>Login</NavLink>
        )}
      </nav>
    </header>
  );
};

export default Navbar;
