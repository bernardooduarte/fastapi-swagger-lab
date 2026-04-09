from typing import Literal, Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class Item(BaseModel):
    name: str = Field(..., description="Nome do item", example="Mouse Gamer")
    price: float = Field(..., gt=0, description="Preço do item (maior que zero)", example=199.9)
    description: Optional[str] = Field(
        default=None,
        description="Descrição opcional do item",
        example="Um mouse gamer com 6 botões e iluminação RGB",
    )
    in_stock: bool = Field(default=True, description="Se o item está em estoque", example=True)


class ItemResponse(BaseModel):
    id: int = Field(..., description="Identificador único do item", example=1)
    name: str = Field(..., description="Nome do item", example="Mouse Gamer")
    price: float = Field(..., description="Preço do item", example=199.9)
    in_stock: bool = Field(..., description="Se o item está em estoque", example=True)


class AccountCreate(BaseModel):
    owner: str = Field(..., description="Nome do titular da conta", example="Bernardo")
    type: Literal["checking", "savings"] = Field(
        ...,
        description="Tipo da conta: checking (corrente) ou savings (poupança)",
        example="checking",
    )


class Account(BaseModel):
    id: int = Field(..., description="Identificador único da conta", example=1)
    owner: str = Field(..., description="Nome do titular da conta", example="Bernardo")
    type: str = Field(..., description="Tipo da conta", example="checking")
    balance: float = Field(..., description="Saldo atual da conta", example=250.75)


class Amount(BaseModel):
    amount: float = Field(
        ...,
        description="Valor da movimentação",
        example=100.0,
    )


class AccountDB(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    owner: str
    type: str
    balance: float = 0.0


class UserDB(SQLModel, table=True):
    id: int | None = SQLField(default=None, primary_key=True)
    username: str
    password_hash: str