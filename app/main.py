from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

from app.routes import items, accounts, ai, auth
from app.database import init_db

app = FastAPI(
    title="FastAPI Swagger Lab",
    description="API de estudo para aprender FastAPI, Swagger (OpenAPI), modelos Pydantic e, depois, integração com IA.",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    init_db()

app.include_router(items.router)
app.include_router(accounts.router)
app.include_router(ai.router)
app.include_router(auth.router)


@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello, FastAPI with Swagger!"}

@app.get("/hello/{name}", tags=["greetings"])
def read_hello(name: str):
    return {"message": f"Hello, {name}!"}