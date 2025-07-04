import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useHasPermission } from '../hooks/useHasPermission'; // Importa o nosso novo hook de permissões

const Navbar = () => {
  const { isAuthenticated, user, logout } = useAuth();
  
  // Verifica se o utilizador tem a permissão para ver as dicas da IA
  const canSeeTips = useHasPermission('feature:access_advanced_analysis');

  const navLinkStyles = ({ isActive }) => ({
    fontWeight: isActive ? 'bold' : 'normal',
    textDecoration: 'none',
    color: isActive ? '#818cf8' : 'white',
    padding: '10px 15px',
    borderRadius: '4px',
  });

  const getFirstName = () => {
    if (!user) return '';
    return user.full_name ? user.full_name.split(' ')[0] : user.email.split('@')[0];
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
            
            {/* --- LINK CONDICIONAL --- */}
            {/* O link para "Dicas da IA" só aparece se o utilizador tiver a permissão */}
            {canSeeTips && (
              <NavLink to="/predictions" style={navLinkStyles}>Dicas da IA</NavLink>
            )}

            <NavLink to="/bets" style={navLinkStyles}>Bet Tracker</NavLink>
            
            {user && user.is_superuser && (
              <NavLink to="/admin/users" style={navLinkStyles}>Admin</NavLink>
            )}

            <span style={{ color: '#ccc', margin: '0 10px' }}>|</span>
            
            <div style={{ textAlign: 'right' }}>
              <span style={{ color: 'white', fontWeight: 'bold' }}>{getFirstName()}</span>
              <div>
                <Link to="/profile" style={{ fontSize: '0.8em', color: '#aaa', textDecoration: 'underline' }}>
                  editar perfil
                </Link>
              </div>
            </div>

            <button onClick={logout} style={{ 
              padding: '8px 15px', 
              background: 'transparent', 
              color: '#ff8a80', 
              border: '1px solid #ff8a80',
              borderRadius: '4px',
              cursor: 'pointer',
              marginLeft: '15px'
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
