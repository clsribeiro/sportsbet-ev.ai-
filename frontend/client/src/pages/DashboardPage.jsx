import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getGames } from '../services/api';
import { Link } from 'react-router-dom'; // Importe o componente Link

const DashboardPage = () => {
  const { user, logout, token } = useAuth();
  const [games, setGames] = useState([]);
  const [loadingGames, setLoadingGames] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) {
      const fetchGames = async () => {
        try {
          setLoadingGames(true);
          const gamesData = await getGames(token);
          setGames(gamesData);
        } catch (err) {
          console.error("Erro ao buscar jogos:", err);
          setError("Não foi possível carregar os jogos.");
        } finally {
          setLoadingGames(false);
        }
      };
      fetchGames();
    }
  }, [token]);

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <h1>Dashboard</h1>
        {/* LINK DE ADMIN CONDICIONAL */}
        {user && user.is_superuser && (
          <Link to="/admin/users" // Aponta para a nova página de utilizadores
            style={{ padding: '10px', background: '#e53935', color: 'white', textDecoration: 'none', borderRadius: '4px' }}
          >
            Painel de Admin
          </Link>
        )}
        <button onClick={logout} style={{ padding: '10px' }}>
          Sair (Logout)
        </button>
      </div>
      {user ? (
        <p>Bem-vindo, <strong>{user.full_name || user.email}</strong>!</p>
      ) : (
        <p>A carregar dados do utilizador...</p>
      )}

      <hr style={{ margin: '20px 0' }} />

      <h2>Próximos Jogos</h2>
      {loadingGames ? (
        <p>A carregar jogos...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {games.map((game) => (
            // Envolva o item da lista com um Link
            <Link to={`/games/${game.id}`} key={game.id} style={{ textDecoration: 'none', color: 'inherit' }}>
              <li style={{ border: '1px solid #333', padding: '15px', marginBottom: '10px', borderRadius: '8px', cursor: 'pointer' }}>
                <div style={{ fontWeight: 'bold', fontSize: '1.2em' }}>
                  <span>{game.home_team.name}</span> vs <span>{game.away_team.name}</span>
                </div>
                <div>Liga: {game.home_team.league}</div>
                <div>Data: {new Date(game.game_time).toLocaleString('pt-PT')}</div>
              </li>
            </Link>
          ))}
        </ul>
      )}
    </div>
  );
};

export default DashboardPage;
