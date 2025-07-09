from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt

security = HTTPBearer()

SECRET_KEY = "IT-IS-QC"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 365 * 24 * 360 * 360


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: str = Depends(security)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        if "sub" not in payload:
            raise credentials_exception
        return {"user_id": payload["sub"], "id": payload.get("id", None)}
    except JWTError:
        raise credentials_exception
