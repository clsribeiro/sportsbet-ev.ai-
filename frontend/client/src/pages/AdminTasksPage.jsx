import React, { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { runPreAnalysisTask, sendBroadcastTest } from '../services/api'; // Importa a nova função
import './Admin.css';

const AdminTasksPage = () => {
  const { token } = useAuth();
  
  // Estado para a tarefa de pré-análise
  const [analysisLoading, setAnalysisLoading] = useState(false);
  const [analysisMessage, setAnalysisMessage] = useState('');

  // Estado para a tarefa de broadcast
  const [broadcastLoading, setBroadcastLoading] = useState(false);
  const [broadcastMessage, setBroadcastMessage] = useState('');
  const [broadcastInput, setBroadcastInput] = useState('Golo! O Flamengo marcou!');

  const handleRunTask = async () => {
    setAnalysisLoading(true);
    setAnalysisMessage('A iniciar a tarefa de pré-análise...');
    try {
      const result = await runPreAnalysisTask(token);
      setAnalysisMessage(`Tarefa concluída! Resultado: ${result.message}`);
    } catch (err) {
      setAnalysisMessage(`Erro ao executar a tarefa: ${err.response?.data?.detail || 'Erro desconhecido'}`);
    } finally {
      setAnalysisLoading(false);
    }
  };

  const handleSendBroadcast = async (e) => {
    e.preventDefault();
    setBroadcastLoading(true);
    setBroadcastMessage('A enviar mensagem...');
    try {
      const result = await sendBroadcastTest(token, broadcastInput);
      setBroadcastMessage(`Sucesso: ${result.detail}`);
    } catch (err) {
      setBroadcastMessage(`Erro ao enviar mensagem: ${err.response?.data?.detail || 'Erro desconhecido'}`);
    } finally {
      setBroadcastLoading(false);
    }
  };

  return (
    <div className="admin-page-container">
      <h1>Tarefas de Administração</h1>
      <p>Aqui pode acionar tarefas de fundo manuais para a plataforma.</p>
      
      <div className="admin-task-card">
        <h2>Serviço de Pré-Análise de Jogos</h2>
        <p>Aciona a IA para analisar os próximos jogos que ainda não têm uma previsão.</p>
        <button onClick={handleRunTask} disabled={analysisLoading}>
          {analysisLoading ? 'A Executar...' : 'Executar Pré-Análise Agora'}
        </button>
        {analysisMessage && <p className="message-feedback">{analysisMessage}</p>}
      </div>

      <div className="admin-task-card">
        <h2>Enviar Notificação de Teste (Broadcast)</h2>
        <p>Envia uma mensagem em tempo real para todos os utilizadores atualmente conectados.</p>
        <form onSubmit={handleSendBroadcast}>
          <input 
            type="text" 
            value={broadcastInput}
            onChange={(e) => setBroadcastInput(e.target.value)}
            placeholder="Escreva a sua mensagem de teste"
            style={{width: '100%', padding: '8px', boxSizing: 'border-box', marginBottom: '10px'}}
          />
          <button type="submit" disabled={broadcastLoading}>
            {broadcastLoading ? 'A Enviar...' : 'Enviar Notificação Global'}
          </button>
        </form>
        {broadcastMessage && <p className="message-feedback">{broadcastMessage}</p>}
      </div>
    </div>
  );
};

export default AdminTasksPage;
