import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getGames } from '../services/api';
import { Link } from 'react-router-dom';
import './Dashboard.css'; // Importa o nosso novo ficheiro de estilos

// Componente para um único jogo
const GameCard = ({ game }) => (
  <Link to={`/games/${game.id}`} className="game-card-link">
    <div className="game-card">
      <div className="game-card-teams">
        <img src={game.home_team.logo_url} alt={game.home_team.name} className="team-logo" />
        <span>{game.home_team.name}</span>
        <span className="vs-separator">vs</span>
        <span>{game.away_team.name}</span>
        <img src={game.away_team.logo_url} alt={game.away_team.name} className="team-logo" />
      </div>
      <div className="game-card-info">
        <span>{game.home_team.league}</span>
        <span>{new Date(game.game_time).toLocaleString('pt-PT', { day: '2-digit', month: '2-digit', hour: '2-digit', minute: '2-digit' })}</span>
      </div>
    </div>
  </Link>
);

// Componente para uma secção de jogos (ex: Hoje, Ao Vivo)
const GameSection = ({ title, games, loading, error }) => (
  <section className="game-section">
    <h2>{title}</h2>
    {loading && <p>A carregar jogos...</p>}
    {error && <p className="error-message">{error}</p>}
    {!loading && !error && (
      <div className="games-grid">
        {games.length > 0 ? (
          games.map(game => <GameCard key={game.id} game={game} />)
        ) : (
          <p>Nenhum jogo encontrado para esta categoria.</p>
        )}
      </div>
    )}
  </section>
);


const DashboardPage = () => {
  const { user } = useAuth(); // Já não precisamos do logout/token aqui diretamente
  
  // Estados para cada categoria de jogos
  const [liveGames, setLiveGames] = useState({ data: [], loading: true, error: '' });
  const [todayGames, setTodayGames] = useState({ data: [], loading: true, error: '' });
  const [upcomingGames, setUpcomingGames] = useState({ data: [], loading: true, error: '' });

  const { token } = useAuth();

  useEffect(() => {
    const fetchGamesData = async (filter, setter) => {
      if (token) {
        try {
          setter(prev => ({ ...prev, loading: true, error: '' }));
          const gamesData = await getGames(token, filter);
          setter({ data: gamesData, loading: false, error: '' });
        } catch (err) {
          console.error(`Erro ao buscar jogos (${filter}):`, err);
          setter({ data: [], loading: false, error: `Não foi possível carregar os jogos (${filter}).` });
        }
      }
    };
    
    // Busca os dados para todas as secções
    fetchGamesData('live', setLiveGames);
    fetchGamesData('today', setTodayGames);
    fetchGamesData('upcoming', setUpcomingGames);

  }, [token]);

  return (
    <div className="dashboard-container">
      <h1>Dashboard Principal</h1>
      <p>Bem-vindo de volta, <strong>{user?.full_name || user?.email}</strong>! Veja os jogos em destaque.</p>
      
      <GameSection title="Ao Vivo" games={liveGames.data} loading={liveGames.loading} error={liveGames.error} />
      <GameSection title="Jogos de Hoje" games={todayGames.data} loading={todayGames.loading} error={todayGames.error} />
      <GameSection title="Próximos na Semana" games={upcomingGames.data} loading={upcomingGames.loading} error={upcomingGames.error} />
    </div>
  );
};

export default DashboardPage;
