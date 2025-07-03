import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../context/AuthContext';
import { getUserBets, createBet, updateBet, deleteBet } from '../services/api';
import './BetTracker.css';

const BetTrackerPage = () => {
  const { token } = useAuth();
  const [bets, setBets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [market, setMarket] = useState('');
  const [selection, setSelection] = useState('');
  const [odds, setOdds] = useState('');
  const [stake, setStake] = useState('');
  const [formError, setFormError] = useState('');

  const fetchBets = useCallback(async () => {
    if (token) {
      try {
        setLoading(true);
        const betsData = await getUserBets(token);
        setBets(betsData);
      } catch (err) {
        setError("Não foi possível carregar as suas apostas.");
      } finally {
        setLoading(false);
      }
    }
  }, [token]);

  useEffect(() => { fetchBets(); }, [fetchBets]);

  const handleAddBet = async (e) => {
    e.preventDefault();
    setFormError('');
    if (!market || !selection || !odds || !stake) {
      setFormError('Todos os campos são obrigatórios.');
      return;
    }
    try {
      const betData = { market_name: market, selection: selection, odds: parseFloat(odds), stake: parseFloat(stake) };
      await createBet(token, betData);
      setMarket(''); setSelection(''); setOdds(''); setStake('');
      fetchBets(); 
    } catch (err) {
      setFormError(err.response?.data?.detail || 'Ocorreu um erro ao adicionar a aposta.');
    }
  };

  const handleUpdateStatus = async (betId, newStatus) => {
    try {
      await updateBet(token, betId, newStatus);
      fetchBets(); // Busca a lista completa para garantir consistência
    } catch (err) {
      alert("Não foi possível atualizar o status da aposta.");
    }
  };

  const handleDeleteBet = async (betId) => {
    // Usamos um prompt de confirmação simples do navegador
    if (window.confirm("Tem a certeza de que quer apagar esta aposta? Esta ação não pode ser desfeita.")) {
      try {
        await deleteBet(token, betId);
        fetchBets();
      } catch (err) {
        alert("Não foi possível apagar a aposta.");
      }
    }
  };

  const getStatusClass = (status) => {
    switch (status) {
      case 'won': return 'status-won';
      case 'lost': return 'status-lost';
      case 'void': return 'status-void';
      default: return 'status-pending';
    }
  };

  return (
    <div className="bet-tracker-container">
      <h1>O Meu Registo de Apostas (Bet Tracker)</h1>
      <div className="form-container">
        <h2>Adicionar Nova Aposta</h2>
        <form onSubmit={handleAddBet} className="bet-form">
          <input type="text" placeholder="Mercado (ex: Vencedor do Jogo)" value={market} onChange={(e) => setMarket(e.target.value)} />
          <input type="text" placeholder="Seleção (ex: Flamengo)" value={selection} onChange={(e) => setSelection(e.target.value)} />
          <input type="number" step="0.01" placeholder="Odds (ex: 1.85)" value={odds} onChange={(e) => setOdds(e.target.value)} />
          <input type="number" step="0.01" placeholder="Valor (Stake)" value={stake} onChange={(e) => setStake(e.target.value)} />
          <button type="submit">Adicionar Aposta</button>
        </form>
        {formError && <p className="error-message">{formError}</p>}
      </div>

      <div className="bets-list-container">
        <h2>As Minhas Apostas</h2>
        {loading && <p>A carregar apostas...</p>}
        {error && <p className="error-message">{error}</p>}
        {!loading && bets.length === 0 && <p>Ainda não tem nenhuma aposta registada.</p>}
        <div className="bets-list">
          {bets.map(bet => (
            <div key={bet.id} className="bet-card">
              <div className="bet-card-header">
                <h3>{bet.market_name}</h3>
                <span className={`bet-status ${getStatusClass(bet.status)}`}>{bet.status}</span>
              </div>
              <p className="bet-selection">{bet.selection}</p>
              <div className="bet-card-footer">
                <span><strong>Odds:</strong> {bet.odds.toFixed(2)}</span>
                <span><strong>Stake:</strong> {bet.stake.toFixed(2)}</span>
                <span><strong>Data:</strong> {new Date(bet.placed_at).toLocaleDateString('pt-PT')}</span>
              </div>
              <div className="bet-card-actions">
                {bet.status === 'pending' && (
                  <>
                    <button onClick={() => handleUpdateStatus(bet.id, 'won')} className="action-button won">Ganha</button>
                    <button onClick={() => handleUpdateStatus(bet.id, 'lost')} className="action-button lost">Perdida</button>
                    <button onClick={() => handleUpdateStatus(bet.id, 'void')} className="action-button void">Anulada</button>
                  </>
                )}
                <button onClick={() => handleDeleteBet(bet.id)} className="action-button delete">Apagar</button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default BetTrackerPage;
