# Guia de Instalacao e Execucao

Este guia contem os passos detalhados para configurar e executar os ambientes de desenvolvimento do backend e do frontend.

## Pre-requisitos

- Python 3.10 ou superior
- Node.js 18 ou superior (recomendado via NVM)
- Git

### Dependencias do Sistema (Ubuntu/Debian)
O projeto utiliza bibliotecas modernas que minimizam a necessidade de pacotes do sistema. No entanto, o `build-essential` e o `git` sao recomendados:
```bash
sudo apt update && sudo apt install -y build-essential git
```

## 1. Configuracao do Backend

Siga estes passos a partir da raiz do repositorio. O projeto utiliza o **uv** para gerenciamento ultra-rapido de pacotes e ambientes.

```bash
# 1. Instale o uv (caso nao possua)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 2. Sincronize o ambiente e dependencias
uv sync

# 3. Configure as variaveis de ambiente
cp .env.example .env

# Edite o arquivo .env com suas configuracoes
# Dica: Para desenvolvimento offline, use PACIENTE_PROVIDER_TYPE=CSV
nano .env
```

## 2. Configuracao do Frontend

Estes passos devem ser executados em um novo terminal.

```bash
# 1. Navegue ate a pasta do frontend
cd frontend

# 2. Instale as dependencias e execute
npm install
npm run dev
```

## 3. Executando a Aplicacao

### Servidor de Backend

Voce pode iniciar o servidor de tres formas:

**A. Usando o script automatizado (Recomendado):**
```bash
./start.sh
```

**B. Usando o uv run (Desenvolvimento):**
```bash
uv run uvicorn src.main:app --reload
```

**C. Executando como modulo:**
```bash
uv run python -m src.main
```

- O backend estara disponivel em `http://127.0.0.1:8000`.
- O Swagger UI estara em `http://127.0.0.1:8000/docs`.

### Servidor de Frontend

Na pasta `frontend/`, execute o servidor de desenvolvimento do Vite.

```bash
npm run dev
```

- O frontend estara disponivel em `http://127.0.0.1:5173` (ou outra porta indicada pelo Vite). O servidor de desenvolvimento do Vite ja vem configurado com um proxy para o backend, entao todas as chamadas de API para `/api` serao redirecionadas automaticamente para `http://127.0.0.1:8000`.

## 4. Build de Producao do Frontend

Para gerar a versao de producao do frontend, que e servida diretamente pelo FastAPI:

```bash
# Na pasta frontend/
npm run build
```

Os arquivos gerados em `frontend/dist/` serao servidos pela aplicacao FastAPI quando ela nao estiver em modo de desenvolvimento, na rota raiz (`/`).
