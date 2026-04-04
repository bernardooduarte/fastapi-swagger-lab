from fastapi import Depends, Header, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

FAKE_API_TOKEN = "meu-token-secreto"
bearer_scheme = HTTPBearer(auto_error=False)


def _extract_token_from_header(authorization: str | None) -> str | None:
    if not authorization:
        return None

    parts = authorization.split()
    if len(parts) == 1:
        if parts[0].lower() == "bearer":
            return None
        return parts[0]
    if len(parts) == 2 and parts[0].lower() == "bearer":
        return parts[1]
    return None


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    authorization: str | None = Header(default=None),
):
    token = None

    if credentials and credentials.scheme.lower() == "bearer":
        token = credentials.credentials
    else:
        token = _extract_token_from_header(authorization)

    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authorization token ausente",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if token != FAKE_API_TOKEN:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"username": "fake-user"}