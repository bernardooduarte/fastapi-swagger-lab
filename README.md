# FastAPI Swagger Lab

API de estudo com FastAPI, documentação Swagger (OpenAPI), autenticação Bearer e integração com Gemini.

## Visão Geral

Este projeto possui 4 grupos principais de endpoints:

- `items`: endpoints de exemplo para leitura/criação de itens (dados em memória).
- `accounts`: criação e movimentação de contas com persistência em PostgreSQL.
- `auth`: login fake para obter token Bearer e testar endpoints protegidos.
- `ai`: chat com Gemini usando chave de API via `.env`.

## Requisitos

- Python 3.12
- PostgreSQL local ativo em `localhost:5432`
- Usuário/senha padrão do banco no código atual:
  - usuário: `postgres`
  - senha: `postgres`

## Configuração

1. Crie e ative o ambiente virtual:

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Configure variáveis em `.env` (já existe no projeto):

```env
GEMINI_API_KEY=seu_token_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## Como Rodar

```bash
uvicorn app.main:app --reload
```

A aplicação ficará disponível em:

- API root: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Banco de Dados (PostgreSQL)

A inicialização do app executa:

- criação automática do banco `accounts` (se ainda não existir);
- criação das tabelas SQLModel (`AccountDB`) via `metadata.create_all`.

Essa lógica está em `app/database.py`.

## Autenticação no Swagger

As rotas de `accounts` exigem Bearer token.

Fluxo:

1. Execute `POST /auth/fake-login` com payload:

```json
{
  "username": "qualquer_valor",
  "password": "qualquer_valor"
}
```

2. Copie o `access_token` retornado.
3. Clique em **Authorize** no Swagger.
4. Cole o token de uma destas formas:
   - `meu-token-secreto`
   - `Bearer meu-token-secreto`
5. Chame os endpoints de `accounts`.

Se o token estiver ausente ou inválido, a API retorna `401 Unauthorized`.

## Endpoints Principais

### Root e exemplo

- `GET /`
- `GET /hello/{name}`

### Items

- `GET /items?skip=0&limit=10`
- `POST /items`

### Auth

- `POST /auth/fake-login`

### Accounts (protegidos)

- `POST /accounts`
- `GET /accounts/{account_id}`
- `POST /accounts/{account_id}/deposit`
- `POST /accounts/{account_id}/withdraw`

### AI

- `POST /ai/chat`

## Comportamento da Rota de IA

A rota `/ai/chat` usa `google.generativeai` e retorna:

- `429` quando a quota do Gemini foi excedida;
- `502` para falhas de upstream/chamada ao provedor;
- `500` se `GEMINI_API_KEY` não estiver configurada.

## Estrutura Atual

```text
app/
  main.py
  config.py
  auth.py
  database.py
  db.py
  models.py
  routes/
    items.py
    accounts.py
    auth.py
    ai.py
```

## Observações

- O endpoint de autenticação atual é propositalmente simples (`fake-login`) para fins de estudo.
- Para produção, substitua por autenticação real (usuário/senha persistidos + JWT).
