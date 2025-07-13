from datetime import datetime, timedelta

import jwt
from fastapi.security import HTTPBearer
from jose import jwt

security = HTTPBearer()

SECRET_KEY = "IT-IS-QC"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 365 * 24 * 360 * 360


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
