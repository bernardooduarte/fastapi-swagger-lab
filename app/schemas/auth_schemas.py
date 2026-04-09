from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., description="Nome de usuário para login", example="bernardo")
    password: str = Field(..., description="Senha do usuário", example="minhaSenha@123")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Token JWT de acesso", example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
    token_type: str = Field(..., description="Tipo do token", example="bearer")