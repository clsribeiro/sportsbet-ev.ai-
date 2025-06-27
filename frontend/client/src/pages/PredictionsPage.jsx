import React, { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import { getPredictions } from '../services/api';
import { Link } from 'react-router-dom';
import PredictionDisplay from '../components/PredictionDisplay'; // Reutilizamos o nosso componente

const PredictionsPage = () => {
  const { token } = useAuth();
  const [predictions, setPredictions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (token) {
      const fetchPredictions = async () => {
        try {
          setLoading(true);
          const data = await getPredictions(token);
          setPredictions(data);
        } catch (err) {
          console.error("Erro ao buscar previsões:", err);
          setError("Não foi possível carregar as dicas de IA no momento.");
        } finally {
          setLoading(false);
        }
      };
      fetchPredictions();
    }
  }, [token]);

  return (
    <div style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <h1>Pré-Análises e Dicas da IA</h1>
      <p>Aqui estão as últimas análises de valor geradas pela nossa inteligência artificial.</p>

      <hr style={{ margin: '20px 0', borderColor: '#444' }} />

      {loading ? (
        <p>A carregar as últimas dicas...</p>
      ) : error ? (
        <p style={{ color: 'red' }}>{error}</p>
      ) : (
        <div>
          {predictions.length > 0 ? (
            predictions.map(prediction => (
              <div key={prediction.id} style={{ border: '1px solid #333', padding: '15px', marginBottom: '20px', borderRadius: '8px' }}>
                <Link to={`/games/${prediction.game.id}`} style={{ textDecoration: 'none', color: 'inherit' }}>
                  <h2 style={{ marginTop: 0 }}>{prediction.game.home_team.name} vs {prediction.game.away_team.name}</h2>
                  <p><strong>Data:</strong> {new Date(prediction.game.game_time).toLocaleString('pt-PT')}</p>
                </Link>
                <PredictionDisplay prediction={prediction} />
              </div>
            ))
          ) : (
            <p>Nenhuma previsão disponível no momento. O nosso sistema está a trabalhar para gerar novas análises.</p>
          )}
        </div>
      )}
    </div>
  );
};

export default PredictionsPage;
