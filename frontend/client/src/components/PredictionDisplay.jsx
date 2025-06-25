import React from 'react';

const PredictionDisplay = ({ prediction }) => {
  if (!prediction) {
    return null;
  }

  const cardStyle = {
    padding: '20px',
    borderRadius: '8px',
    marginBottom: '20px',
    color: 'white',
  };

  const summaryCardStyle = {
    ...cardStyle,
    background: '#2a2a2a',
    borderLeft: '5px solid #007bff',
  };

  const tipCardStyle = {
    ...cardStyle,
    background: '#004d40',
    borderLeft: '5px solid #4caf50',
  };

  const confidenceStyle = {
      fontWeight: 'bold',
      fontSize: '1.2em',
      color: prediction.confidence_level > 0.7 ? '#4caf50' : '#ffc107',
  };

  return (
    <div style={{ marginTop: '30px' }}>
      <h2>Análise de IA</h2>
      <div style={summaryCardStyle}>
        <h3>Resumo da Previsão</h3>
        <p>{prediction.prediction_summary}</p>
        <p><strong>Vencedor Previsto:</strong> {prediction.predicted_winner}</p>
        <p><strong>Nível de Confiança:</strong> <span style={confidenceStyle}>{(prediction.confidence_level * 100).toFixed(0)}%</span></p>
      </div>
      <div style={tipCardStyle}>
        <h3>Dica de Aposta de Valor (+EV)</h3>
        <p>{prediction.value_bet_suggestion}</p>
      </div>
    </div>
  );
};

export default PredictionDisplay;
