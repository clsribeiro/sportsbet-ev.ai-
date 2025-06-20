import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom'; // useParams para ler o ID da URL
import { useAuth } from '../context/AuthContext';
import { getGameDetails } from '../services/api';

const GameDetailPage = () => {
  const { gameId } = useParams(); // Obtém o 'gameId' da URL (ex: /games/1)
  const { token } = useAuth();
  const [game, setGame] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (token && gameId) {
      const fetchGameDetails = async () => {
        try {
          setLoading(true);
          const gameData = await getGameDetails(token, gameId);
          setGame(gameData);
        } catch (err) {
          console.error("Erro ao buscar detalhes do jogo:", err);
          setError("Não foi possível carregar os detalhes do jogo.");
        } finally {
          setLoading(false);
        }
      };
      fetchGameDetails();
    }
  }, [token, gameId]);

  if (loading) return <div>A carregar detalhes do jogo...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;
  if (!game) return <div>Jogo não encontrado.</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <Link to="/">&larr; Voltar ao Dashboard</Link>

      <h1 style={{ marginTop: '20px' }}>{game.home_team.name} vs {game.away_team.name}</h1>
      <p><strong>Liga:</strong> {game.home_team.league}</p>
      <p><strong>Data:</strong> {new Date(game.game_time).toLocaleString('pt-PT')}</p>
      <p><strong>Status:</strong> {game.status}</p>

      <div style={{ marginTop: '30px', padding: '15px', background: '#2a2a2a', borderRadius: '8px' }}>
        <h3>Análise da Partida</h3>
        <p>{game.analysis || "Análise não disponível."}</p>
      </div>

      <div style={{ marginTop: '20px', padding: '15px', background: '#004d40', borderRadius: '8px' }}>
        <h3>Dica de Aposta de Valor (+EV)</h3>
        <p>{game.value_bet_tip || "Nenhuma dica de valor identificada para esta partida."}</p>
      </div>
    </div>
  );
};

export default GameDetailPage;
