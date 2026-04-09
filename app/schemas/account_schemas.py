from typing import Literal, Optional
from pydantic import BaseModel, Field
from sqlmodel import SQLModel, Field as SQLField


class AccountCreate(BaseModel):
       owner: str = Field(
              ...,
              description="Nome do titular da conta",
              example="Bernardo",
       )
       type: Literal["checking", "savings"] = Field(
              ...,
              description="Tipo da conta: checking (corrente) ou savings (poupança)",
              example="checking",
       )


class AccountResponse(BaseModel):
       id: int = Field(..., description="Identificador único da conta", example=1)
       owner: str = Field(..., description="Nome do titular da conta", example="Bernardo")
       type: str = Field(..., description="Tipo da conta", example="checking")
       balance: float = Field(..., description="Saldo atual da conta", example=250.75)
