# FastAPI Swagger Lab

API de estudo com FastAPI, Swagger/OpenAPI, autenticação JWT com hash de senha, persistência em PostgreSQL e integração com Gemini.

## Visão Geral

O projeto foi organizado para separar responsabilidades entre rotas, controle de regras e acesso a dados. A aplicação expõe exemplos de leitura e criação de itens, criação e movimentação de contas, autenticação real com JWT e um endpoint de IA.

## Funcionalidades

- `items`: exemplo simples em memória para leitura e criação de itens.
- `accounts`: criação, consulta, depósito e saque com persistência em PostgreSQL.
- `auth`: registro e login real com hash de senha e JWT.
- `ai`: chat com Gemini usando a API `google-genai`.

## Arquitetura

### 1) Router Pattern

As rotas ficam em `app/routes` e concentram a camada HTTP:

- recebem e validam entrada;
- aplicam autenticação e autorização com `Depends`;
- delegam regras de negócio para controllers/repositórios;
- traduzem erros para respostas HTTP.

### 2) Controller Pattern

Os controllers ficam em `app/controllers` e servem como camada intermediária entre HTTP e repositório:

- encapsulam regras de operação;
- mantêm a rota fina;
- evitam que a rota fale direto com o banco quando não precisa.

### 3) Repository Pattern

Os repositórios ficam em `app/repositories` e concentram o acesso ao banco com SQLModel/Session:

- `AccountRepository` executa operações de conta;
- `UserRepository` executa consultas e persistência de usuários;
- o contrato base está em `app/repositories/base.py`.

### 4) Dependency Injection

FastAPI injeta dependências para conectar as camadas:

- rota injeta controller ou repositório com `Depends(...)`;
- repositório injeta sessão do banco com `Depends(get_session)`;
- autenticação injeta o usuário atual via `get_current_user`.

## Fluxo de Requisição

### Contas

1. A requisição chega em `app/routes/accounts.py`.
2. A rota exige JWT válido.
3. A rota delega a operação para `AccountController`.
4. O controller chama `AccountRepository`.
5. O repositório lê ou atualiza o PostgreSQL.
6. A resposta volta em formato HTTP.

### Autenticação

1. O usuário faz `POST /auth/register` ou `POST /auth/login`.
2. A senha é armazenada com hash usando `passlib[bcrypt]`.
3. O login compara a senha enviada com o hash salvo.
4. Se válido, a API gera um JWT real com `sub` e `exp`.
5. As rotas protegidas validam esse token em cada requisição.

## Requisitos

- Python 3.12+
- PostgreSQL local ativo em `localhost:5432`
- Credenciais padrão definidas no código:
  - usuário: `postgres`
  - senha: `postgres`
  - banco de administração: `postgres`
  - banco da aplicação: `accounts`

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

3. Configure o arquivo `.env`.

```env
SECRET_KEY=sua_chave_secreta_aqui
ACCESS_TOKEN_EXPIRE_MINUTES=30
GEMINI_API_KEY=seu_token_aqui
GEMINI_MODEL=gemini-2.5-flash
```

Para gerar a `SECRET_KEY`, use:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
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

- o banco `accounts` é criado automaticamente caso não exista;
- as tabelas de `AccountDB` e `UserDB` são criadas via `SQLModel.metadata.create_all`.

A configuração e o bootstrap do banco estão em `app/database.py`.

## Autenticação JWT

As rotas de `accounts` exigem token Bearer JWT.

Fluxo recomendado:

1. Faça `POST /auth/register` ou `POST /auth/login` com credenciais válidas.
2. Copie o campo `access_token` retornado.
3. Clique em `Authorize` no Swagger.
4. Informe o token como:
   - `meu-token-jwt`
   - `Bearer meu-token-jwt`
5. Acesse as rotas protegidas de `accounts`.

Se o token estiver ausente, inválido ou expirado, a API retorna `401`.

## Endpoints

### Root e exemplo

- `GET /`
- `GET /hello/{name}`

### Items

- `GET /items?skip=0&limit=10`
- `POST /items`

### Auth

- `POST /auth/register`
- `POST /auth/login`

### Accounts protegidos

- `POST /accounts`
- `GET /accounts/{account_id}`
- `POST /accounts/{account_id}/deposit`
- `POST /accounts/{account_id}/withdraw`

### AI

- `POST /ai/chat`

Payload esperado:

```json
{
  "prompt": "Sua pergunta aqui"
}
```

## Modelos e Swagger

Os schemas usam `Field()` com `description` e `example`, então o Swagger exibe documentação enriquecida nos campos principais.

Exemplos usados no projeto:

- `amount`: valor da movimentação;
- `username` e `password`: login e registro;
- `prompt`: entrada para o Gemini;
- `name`, `price` e `in_stock`: item de exemplo.

## Dependências Relevantes

Além do stack FastAPI, esta API depende diretamente de:

- `sqlmodel`
- `psycopg2-binary`
- `google-genai`
- `passlib[bcrypt]`
- `python-jose[cryptography]`

As versões estão fixadas em `requirements/base.txt`.

## Comportamento Esperado

### Items

- endpoint de leitura retorna uma lista em memória;
- endpoint de criação devolve um item de resposta formatado.

### Auth

- `POST /auth/register` cria usuário com hash de senha;
- `POST /auth/login` valida senha salva e retorna JWT;
- o fluxo não usa mais fake login.

### Accounts

- `amount` precisa ser maior que zero;
- saque acima do saldo retorna `400` com `Insufficient funds`;
- conta inexistente retorna `404`.

### AI

- `500` quando `GEMINI_API_KEY` não está configurada;
- `429` quando a quota do Gemini é excedida;
- `502` quando a chamada ao provedor falha ou a resposta vem vazia/inesperada.

## Estrutura de Pastas

```text
app/
  main.py
  config.py
  auth.py
  database.py
  db.py
  models.py
  controllers/
    base.py
    accounts.py
  repositories/
    base.py
    accounts.py
    user.py
  routes/
    items.py
    accounts.py
    auth.py
    ai.py
  schemas/
    account_schemas.py
    auth_schemas.py
main.py
requirements.txt
requirements/
  base.txt
```

## Observações

- A autenticação JWT usa `SECRET_KEY` definida em `.env` para assinar tokens.
- Os tokens carregam expiração e o usuário em `sub`.
- Os campos do Swagger foram enriquecidos com `description` e `example` nos schemas Pydantic.
- O endpoint de Gemini foi ajustado para a API atual do pacote `google-genai`.