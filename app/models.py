from typing import Literal, Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField

class Item(BaseModel):
       name: str = Field(..., description="Nome do item")
       price: float = Field(..., gt=0, description="Preço do item (maior que zero)")
       description: Optional[str] = Field(
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
       type: Literal["checking", "savings"] = Field(
           ..., description="Tipo da conta: checking (corrente) ou savings (poupança)"
       )


class Account(BaseModel):
       id: int
       owner: str
       type: str
       balance: float


class Amount(BaseModel):
       amount: float = Field(
           ..., gt=0, description="Valor da movimentação (maior que zero)"
       )

class AccountDB(SQLModel, table=True):
       id: int | None = SQLField(default=None, primary_key=True)
       owner: str
       type: str
       balance: float = 0.0