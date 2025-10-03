from fastapi import Security, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.core.config import settings

bearer_scheme = HTTPBearer(auto_error=False)

TOKEN_SCOPES = {
    settings.API_ADMIN_KEY: ["admin", "user"],
    settings.API_SECRET_KEY: ["user"]
}


async def get_current_user(
        token: HTTPAuthorizationCredentials = Security(bearer_scheme)
) -> dict:
    credentials = token.credentials

    if credentials == settings.API_ADMIN_KEY:
        username = "admin_user"
        scopes = TOKEN_SCOPES[credentials]
    elif credentials == settings.API_SECRET_KEY:
        username = "normal_user"
        scopes = TOKEN_SCOPES[credentials]
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"username": username, "scopes": scopes}


def require_scope(required_scopes: list[str]):
    async def scope_checker(
        current_user: dict = Depends(get_current_user)
    ):
        user_scopes = current_user.get("scopes", [])
        for scope in required_scopes:
            if scope not in user_scopes:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Not enough permissions. Requires scope: '{scope}'"
                )
        return current_user

    return scope_checker