import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { runPreAnalysisTask } from '../services/api';

const AdminTasksPage = () => {
  const { token } = useAuth();
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const handleRunTask = async () => {
    setLoading(true);
    setMessage('A iniciar a tarefa de pré-análise. Isto pode demorar alguns minutos...');
    try {
      const result = await runPreAnalysisTask(token);
      setMessage(`Tarefa concluída! Resultado: ${result.message}`);
    } catch (err) {
      console.error("Erro ao executar a tarefa:", err);
      setMessage(`Erro ao executar a tarefa: ${err.response?.data?.detail || 'Erro desconhecido'}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <h1>Tarefas de Administração</h1>
      <p>Aqui pode acionar tarefas de fundo manuais para a plataforma.</p>
      <div style={{ padding: '20px', border: '1px solid #444', borderRadius: '8px', marginTop: '20px' }}>
        <h2>Serviço de Pré-Análise de Jogos</h2>
        <p>
          Clique no botão abaixo para que a IA analise os próximos jogos agendados
          que ainda não têm uma previsão.
        </p>
        <button onClick={handleRunTask} disabled={loading} style={{ padding: '10px 15px' }}>
          {loading ? 'A Executar...' : 'Executar Pré-Análise Agora'}
        </button>
        {message && <p style={{ marginTop: '15px', background: '#2a2a2a', padding: '10px', borderRadius: '4px' }}>{message}</p>}
      </div>
    </div>
  );
};

export default AdminTasksPage;
