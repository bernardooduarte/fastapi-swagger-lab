from fastapi import FastAPI
from pydantic import BaseModel, Field

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