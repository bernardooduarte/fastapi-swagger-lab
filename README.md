# FastAPI Swagger Lab

Projeto de estudo com FastAPI e Swagger (OpenAPI), criado do zero.

## Requisitos

- Python 3.12
- pip

## Como rodar

```bash
python -m venv .venv
.\.venv\Scripts\activate  # Windows

pip install -r requirements.txt

uvicorn main:app --reload
```
# Endpoints
```bash
read_root()

read_hello()

read_items()

create_item()
```

Acesse:

- API root: http://127.0.0.1:8000/
- Documentação Swagger: http://127.0.0.1:8000/docs
- Documentação alternativa: http://127.0.0.1:8000/redoc