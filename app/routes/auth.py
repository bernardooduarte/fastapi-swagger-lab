from fastapi import APIRouter
from pydantic import BaseModel

from app.auth import FAKE_API_TOKEN

router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


@router.post("/fake-login", response_model=TokenResponse)
def fake_login(data: LoginRequest):
    return TokenResponse(access_token=FAKE_API_TOKEN)