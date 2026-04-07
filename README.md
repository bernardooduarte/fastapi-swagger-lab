# FastAPI Swagger Lab

API de estudo com FastAPI, documentação Swagger (OpenAPI), autenticação Bearer, persistência em PostgreSQL e integração com Gemini.

## Visão Geral

O projeto foi estruturado com separação de responsabilidades usando padrões na camada de rotas e na camada de acesso a dados.

Principais grupos de endpoint:

- items: exemplo simples em memória para leitura e criação de itens.
- accounts: criação e movimentação de contas com persistência em PostgreSQL.
- auth: login fake para obter token Bearer e testar endpoints protegidos.
- ai: chat com Gemini usando chave de API via .env.

## Arquitetura e Patterns

### 1) Router Pattern (camada HTTP)

As rotas ficam em `app/routes` e concentram apenas responsabilidades de API:

- receber e validar entrada HTTP;
- aplicar autenticação/autorização via `Depends`;
- delegar regras de negócio/acesso a dados para componentes específicos;
- traduzir exceções em respostas HTTP (`400`, `401`, `404`, `429`, `502`, etc).

Com isso, a camada de rota fica fina, previsível e fácil de manter.

### 2) Repository Pattern (camada de dados)

Os repositórios ficam em `app/repositories` e abstraem o acesso ao banco com SQLModel/Session:

- `Repository` base define contrato comum;
- `AccountRepository` implementa operações de conta (`create`, `get`, `deposit`, `withdraw`, etc);
- regras de persistência e consistência de dados ficam centralizadas nessa camada.

Isso reduz acoplamento entre HTTP e banco de dados, facilitando evolução e testes.

### 3) Dependency Injection Pattern (FastAPI Depends)

A ligação entre camadas é feita com injeção de dependência:

- rota injeta `AccountRepository` usando `Depends(get_account_repository)`;
- repositório injeta sessão do banco via `Depends(get_session)`.

Esse padrão permite trocar implementações com menor impacto no restante do código.

### Fluxo de uma requisição de conta

1. Request chega em `app/routes/accounts.py`.
2. Rota valida entrada e autenticação.
3. Rota delega operação para `AccountRepository`.
4. Repositório executa query/update no PostgreSQL.
5. Resultado volta para rota, que responde em formato HTTP.

## Requisitos

- Python 3.12+
- PostgreSQL local ativo em localhost:5432
- Credenciais padrão definidas no código:
  - usuário: postgres
  - senha: postgres
  - banco de administração: postgres
  - banco de aplicação: accounts

## Configuração

1. Crie e ative o ambiente virtual.

```bash
python -m venv .venv
.\.venv\Scripts\activate
```

2. Instale as dependências.

```bash
pip install -r requirements.txt
```

3. Configure o arquivo .env.

```env
GEMINI_API_KEY=seu_token_aqui
GEMINI_MODEL=gemini-2.5-flash
```

## Como Executar

```bash
uvicorn app.main:app --reload
```

Aplicação disponível em:

- API root: http://127.0.0.1:8000/
- Swagger: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

## Banco de Dados

Na inicialização do app:

- o banco accounts é criado automaticamente caso não exista;
- a tabela de contas é criada via SQLModel metadata.create_all.

A configuração e bootstrap do banco estão em app/database.py.

## Autenticação no Swagger

As rotas de accounts exigem token Bearer.

Fluxo recomendado:

1. Chame POST /auth/fake-login com:

```json
{
  "username": "qualquer_valor",
  "password": "qualquer_valor"
}
```

2. Copie o campo access_token.
3. Clique em Authorize no Swagger.
4. Informe o token de uma destas formas:
   - meu-token-secreto
   - Bearer meu-token-secreto
5. Acesse as rotas de accounts.

Se token ausente ou inválido, a API retorna 401.

## Endpoints Principais

### Root e exemplo

- GET /
- GET /hello/{name}

### Items

- GET /items?skip=0&limit=10
- POST /items

### Auth

- POST /auth/fake-login

### Accounts (protegidos)

- POST /accounts
- GET /accounts/{account_id}
- POST /accounts/{account_id}/deposit
- POST /accounts/{account_id}/withdraw

Payload de movimentação:

```json
{
  "amount": 100
}
```

Regras atuais de movimentação:

- amount deve ser maior que zero;
- saque com valor maior que o saldo retorna 400 com detail `Insufficient funds`;
- conta inexistente retorna 404 Account not found.

## Comportamento da Rota de IA

A rota POST /ai/chat recebe:

```json
{
  "prompt": "Sua pergunta aqui"
}
```

Respostas de erro esperadas:

- 500 quando GEMINI_API_KEY não está configurada;
- 429 quando a quota do Gemini foi excedida;
- 502 para falha na chamada ao provedor ou resposta vazia/inesperada.

## Dependências Relevantes

Além do stack FastAPI, esta API depende diretamente de:

- sqlmodel
- psycopg2-binary
- google-generativeai

Todas estão fixadas em requirements/base.txt e instaladas via requirements.txt.

## Estrutura de Pastas

```text
app/
  main.py
  config.py
  auth.py
  database.py
  db.py
  models.py
  repositories/
    base.py
    accounts.py
  routes/
    items.py
    accounts.py
    auth.py
    ai.py
main.py
requirements.txt
requirements/
  base.txt
```

## Observações

- O endpoint de autenticação fake-login é apenas para estudo.
- Em produção, substitua por autenticação real com usuários persistidos e JWT.
- A camada `routes` e a camada `repositories` seguem padrões para manter baixo acoplamento e alta coesão.
