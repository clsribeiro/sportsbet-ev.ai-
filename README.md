# SportsBet +EV AI

**Plataforma de Análise Esportiva com Foco em Apostas de Valor Esperado Positivo (+EV)**

## 🎯 Objetivo Principal

Desenvolver uma plataforma web que integra APIs esportivas para realizar análises preditivas e fornecer recomendações de apostas com odds superiores a 1.5. O foco inicial são as ligas NBA, NFL e futebol (com ênfase em ligas brasileiras e principais torneios mundiais).

## 🚧 Status Atual do Projeto

O projeto encontra-se na fase inicial de desenvolvimento. A estrutura base do backend (API) e do frontend (interface do usuário) foi estabelecida, e a comunicação entre eles está funcional. As próximas fases envolverão a integração com APIs esportivas, desenvolvimento de modelos de machine learning e a implementação das funcionalidades principais.

## ✨ Funcionalidades (Planejadas)

* **Módulo 1: Destaques Diários:** Seleção inteligente de 3-5 jogos/dia por esporte.
* **Módulo 2: Análise Preditiva:** Modelos de machine learning com histórico de 5 temporadas.
* **Módulo 3: Apostas Ao Vivo:** Atualizações em tempo real (via WebSockets).
* **Interface Clara:** Separação entre Análise Técnica (estatísticas, heatmaps) e Recomendações de Apostas (odds, EV, gestão de banca).
* **Sistema de Ranking:** Classificação automática de jogos por potencial de lucro, confiabilidade e relevância.
* **Filtros Customizáveis:** Por tipo de aposta e nível de risco.
* **Alertas:** Notificações de oportunidades de apostas via Email/Telegram.
* **Sistema de Aprendizagem:** O sistema aprenderá com os resultados para refinar métodos e ranquear os mais lucrativos.

## 💻 Tecnologias Utilizadas (Stack)

* **Backend:** Python com FastAPI
* **Frontend:** React com Vite (JavaScript/JSX)
* **Banco de Dados:** PostgreSQL (planejado)
* **Controle de Versão:** Git e GitHub
* **Ambiente de Desenvolvimento:** Docker (planejado para facilitar a configuração e implantação)
* **Servidor de Implantação:** Debian (planejado)

## 🚀 Configuração e Execução do Ambiente de Desenvolvimento Local

### Pré-requisitos

* [Git](https://git-scm.com/)
* [Python 3.10+](https://www.python.org/) (com pip e venv)
* [Node.js](https://nodejs.org/) (com npm, via NVM recomendado)
* [Docker](https://www.docker.com/) e Docker Compose (quando implementado)

### Passos para Configuração

1.  **Clonar o repositório:**
    ```bash
    git clone [https://github.com/clsribeiro/sportsbet-ev.ai-.git](https://github.com/clsribeiro/sportsbet-ev.ai-.git)
    cd sportsbet-ev.ai-
    ```

2.  **Configurar o Backend:**
    ```bash
    cd backend
    python3 -m venv venv      # Criar ambiente virtual
    source venv/bin/activate  # Ativar ambiente virtual (Linux/macOS)
    # venv\Scripts\activate   # Ativar ambiente virtual (Windows)
    pip install -r requirements.txt # Instalar dependências (criar requirements.txt depois)
    # Por enquanto, instalamos manualmente: pip install fastapi "uvicorn[standard]"
    ```

3.  **Configurar o Frontend:**
    ```bash
    cd ../frontend/client
    npm install
    ```

### Executando a Aplicação

1.  **Iniciar o Backend:**
    No diretório `backend/` com o `venv` ativo:
    ```bash
    uvicorn main:app --reload --host 0.0.0.0 --port 8000
    ```
    A API estará acessível em `http://localhost:8000` e `http://SEU_IP_LOCAL:8000`.

2.  **Iniciar o Frontend:**
    No diretório `frontend/client/` (em um novo terminal):
    ```bash
    npm run dev -- --host
    ```
    A interface estará acessível em `http://localhost:5173` e `http://SEU_IP_LOCAL:5173` (ou a porta indicada pelo Vite).

## 📂 Estrutura de Diretórios (Simplificada)
