from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer
from jose import JWTError, jwt


security = HTTPBearer()

SECRET_KEY = "Sahel-Is-Here"
ACCESS_TOKEN_EXPIRE_MINUTES = 365 * 24 * 360 * 360


def create_access_token(data: dict, expires_delta: timedelta = None):
    pass


