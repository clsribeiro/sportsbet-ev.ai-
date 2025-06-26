import React, { useState, useEffect, useCallback } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { getGameDetails, generatePrediction } from '../services/api';
import PredictionDisplay from '../components/PredictionDisplay';

const GameDetailPage = () => {
  const { gameId } = useParams();
  const { token } = useAuth();
  
  // Estados separados para cada parte da página
  const [game, setGame] = useState(null);
  const [prediction, setPrediction] = useState(null);
  
  const [gameLoading, setGameLoading] = useState(true);
  const [predictionLoading, setPredictionLoading] = useState(true);
  
  const [gameError, setGameError] = useState('');
  const [predictionError, setPredictionError] = useState('');

  // Função para buscar a previsão da IA. Pode ser chamada ao carregar ou ao clicar no botão.
  const fetchPrediction = useCallback(async () => {
    if (token && gameId) {
      try {
        setPredictionLoading(true);
        setPredictionError(''); // Limpa erros anteriores
        const predictionData = await generatePrediction(token, gameId);
        setPrediction(predictionData);
      } catch (err) {
        console.error("Erro ao buscar previsão da IA:", err);
        setPredictionError("Falha ao obter a análise da IA.");
      } finally {
        setPredictionLoading(false);
      }
    }
  }, [token, gameId]);

  // useEffect para buscar os dados essenciais do jogo
  useEffect(() => {
    const fetchGameData = async () => {
      if (token && gameId) {
        try {
          setGameLoading(true);
          const gameData = await getGameDetails(token, gameId);
          setGame(gameData);
        } catch (err) {
          console.error("Erro ao buscar detalhes do jogo:", err);
          setGameError("Não foi possível carregar os detalhes do jogo.");
        } finally {
          setGameLoading(false);
        }
      }
    };
    fetchGameData();
  }, [token, gameId]);
  
  // useEffect para buscar a previsão da IA automaticamente
  useEffect(() => {
    // Só busca a previsão se já tivermos os dados do jogo, para evitar condições de corrida
    if (game) {
      fetchPrediction();
    }
  }, [game, fetchPrediction]); // Depende do 'game' e da função `fetchPrediction`

  // Função para renderizar a secção de previsão
  const renderPredictionSection = () => {
    if (predictionLoading) {
      return <p>A gerar análise de IA...</p>;
    }
    if (predictionError) {
      return (
        <div>
          <p style={{ color: 'orange' }}>{predictionError}</p>
          <button onClick={fetchPrediction} style={{ marginTop: '10px' }}>Tentar Novamente</button>
        </div>
      );
    }
    if (prediction) {
      return <PredictionDisplay prediction={prediction} />;
    }
    // Não mostra nada se não houver previsão e não estiver a carregar nem com erro
    return null; 
  };

  if (gameLoading) {
    return <div style={{ textAlign: 'center', marginTop: '50px' }}><h2>A carregar dados do jogo...</h2></div>;
  }

  if (gameError) {
    return <div style={{ color: 'red', textAlign: 'center', marginTop: '50px' }}>{gameError}</div>;
  }
  
  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <Link to="/">&larr; Voltar ao Dashboard</Link>
      
      {game ? (
        <>
          <h1 style={{ marginTop: '20px' }}>{game.home_team.name} vs {game.away_team.name}</h1>
          <p><strong>Liga:</strong> {game.home_team.league}</p>
          <p><strong>Data:</strong> {new Date(game.game_time).toLocaleString('pt-PT')}</p>
          <p><strong>Status:</strong> {game.status}</p>
        </>
      ) : (
        <div style={{ textAlign: 'center', marginTop: '50px' }}>Jogo não encontrado.</div>
      )}

      <hr style={{ margin: '30px 0', borderColor: '#444' }} />

      {renderPredictionSection()}
    </div>
  );
};

export default GameDetailPage;
