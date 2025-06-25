import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
// Importa ambas as funções da API
import { getGameDetails, generatePrediction } from '../services/api'; 
// Importa o novo componente de exibição
import PredictionDisplay from '../components/PredictionDisplay';

const GameDetailPage = () => {
  const { gameId } = useParams();
  const { token } = useAuth();
  const [game, setGame] = useState(null);
  const [prediction, setPrediction] = useState(null); // Novo estado para a previsão
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [predictionLoading, setPredictionLoading] = useState(false); // Loading para o botão

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

  // Função para ser chamada pelo botão
  const handleGeneratePrediction = async () => {
    if (token && gameId) {
      try {
        setPredictionLoading(true);
        setError('');
        const predictionData = await generatePrediction(token, gameId);
        setPrediction(predictionData);
      } catch (err) {
        console.error("Erro ao gerar previsão:", err);
        setError("Não foi possível obter a análise da IA. Tente novamente.");
      } finally {
        setPredictionLoading(false);
      }
    }
  };

  if (loading) return <div>A carregar detalhes do jogo...</div>;
  if (!game && !error) return <div>Jogo não encontrado.</div>;

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <Link to="/">&larr; Voltar ao Dashboard</Link>

      {game && (
        <>
          <h1 style={{ marginTop: '20px' }}>{game.home_team.name} vs {game.away_team.name}</h1>
          <p><strong>Liga:</strong> {game.home_team.league}</p>
          <p><strong>Data:</strong> {new Date(game.game_time).toLocaleString('pt-PT')}</p>
          <p><strong>Status:</strong> {game.status}</p>
        </>
      )}

      <hr style={{ margin: '30px 0' }} />

      {/* Secção de Análise de IA */}
      {prediction ? (
        // Se já tivermos uma previsão, exibe o componente
        <PredictionDisplay prediction={prediction} />
      ) : (
        // Caso contrário, mostra o botão para gerar uma
        <div style={{ textAlign: 'center' }}>
          <button 
            onClick={handleGeneratePrediction} 
            disabled={predictionLoading}
            style={{ padding: '15px 30px', fontSize: '1.2em', cursor: 'pointer' }}
          >
            {predictionLoading ? 'A gerar análise...' : 'Gerar Análise de IA'}
          </button>
        </div>
      )}

      {error && <p style={{ color: 'red', marginTop: '20px' }}>{error}</p>}
    </div>
  );
};

export default GameDetailPage;
