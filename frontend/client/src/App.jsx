import { useState, useEffect } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  const [backendStatus, setBackendStatus] = useState('Carregando status do backend...')

  useEffect(() => {
    // URL do seu backend. Use o IP da VM para acesso via rede.
    // Certifique-se que o backend está rodando e acessível neste endereço.
    const backendUrl = 'http://192.168.100.169:8000/api/health';

    fetch(backendUrl)
      .then(response => {
        if (!response.ok) {
          throw new Error(`Erro HTTP! status: ${response.status}`);
        }
        return response.json();
      })
      .then(data => {
        setBackendStatus(data.status || 'Status não recebido ou em formato incorreto.');
      })
      .catch(error => {
        console.error("Erro ao buscar dados do backend:", error);
        setBackendStatus('Falha ao conectar com o backend.');
      });
  }, []); // Array de dependências vazio, roda apenas uma vez ao montar o componente

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank" rel="noreferrer">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank" rel="noreferrer">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edite <code>src/App.jsx</code> e salve para testar o HMR.
        </p>
      </div>
      <p className="read-the-docs">
        Clique nos logos do Vite e React para aprender mais.
      </p>
      <hr />
      <h2>Status do Backend:</h2>
      <p>{backendStatus}</p>
    </>
  )
}

export default App
