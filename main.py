from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Literal

app = FastAPI(
    title="FastAPI Swagger Lab",
    description="API de estudo para aprender FastAPI, Swagger (OpenAPI), modelos Pydantic e, depois, integração com IA.",
    version="0.1.0",
)

class Item(BaseModel):
    name: str = Field(..., description="Nome do item")
    price: float = Field(..., gt=0, description="Preço do item (maior que zero)")
    description: str | None = Field(
        default=None,
        description="Descrição opcional do item",
        example="Um mouse gamer com 6 botões e iluminação RGB",
    )
    in_stock: bool = Field(default=True, description="Se o item está em estoque")

class ItemResponse(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

class AccountCreate(BaseModel):
    owner: str = Field(..., description="Nome do titular da conta")
    type: Literal["checking", "savings"] = Field(..., description="Tipo da conta: checking (corrente) ou savings (poupança)")

class Account(BaseModel):
    id: int
    owner: str
    type: str
    balance: float

accounts_db: list[Account] = []
next_account_id = 1

@app.get("/", tags=["root"])
def read_root():
    return {"message": "Hello, FastAPI with Swagger!"}

@app.get("/hello/{name}", tags=["greetings"])
def read_hello(name: str):
    return {"message": f"Hello, {name}!"}

@app.get("/items", tags=["items"])
def read_items(skip: int = 0, limit: int = 10):
    ...

@app.post("/items", response_model=ItemResponse, tags=["items"])
def create_item(item: Item):
    ...

@app.post("/accounts", response_model=Account, tags=["accounts"])
def create_account(account_data: AccountCreate):
    global next_account_id

    account = Account(
        id=next_account_id,
        owner=account_data.owner,
        type=account_data.type,
        balance=0.0,
    )
    accounts_db.append(account)
    next_account_id += 1

    return account

@app.get("/accounts/{account_id}", response_model=Account, tags=["accounts"])
def get_account(account_id: int):
    for acc in accounts_db:
        if acc.id == account_id:
            return acc
    raise HTTPException(status_code=404, detail="Account not found")