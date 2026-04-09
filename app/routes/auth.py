from fastapi import APIRouter, Depends, HTTPException

from app.auth import create_access_token, hash_password, verify_password
from app.models import UserDB
from app.repositories.user import UserRepository, get_user_repository
from app.schemas.auth_schemas import LoginRequest, TokenResponse

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, repository: UserRepository = Depends(get_user_repository)):
    try:
        user = repository.get_user_by_username(data.username)
    except ValueError:
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=TokenResponse)
def register(data: LoginRequest, repository: UserRepository = Depends(get_user_repository)):
    try:
        repository.get_user_by_username(data.username)
        raise HTTPException(
            status_code=400,
            detail="Username already registered",
        )
    except ValueError:
        pass

    hashed_password = hash_password(data.password)
    new_user = UserDB(username=data.username, password_hash=hashed_password)
    user = repository.create_user(new_user)
        
    access_token = create_access_token(data={"sub": user.username})
    return TokenResponse(access_token=access_token, token_type="bearer")