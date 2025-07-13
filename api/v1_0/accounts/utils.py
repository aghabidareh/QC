from datetime import datetime, timedelta

import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.v1_0.accounts.configs import AUTHORIZE_URL, TOKEN_URL
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.routes import VALIDATE_URL

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZE_URL,
    tokenUrl=TOKEN_URL,
)


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                VALIDATE_URL,
                headers={"Authorization": f"Bearer {token}"},
            )
            if response.status_code != 200:
                raise HTTPException(status_code=401, detail="Invalid token")

            token_data = response.json()
            user_id = token_data.get("user_id")
            scopes = token_data.get("scope", "").split()

            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token: No user_id")

            result = await db.execute(select(Accounts).where(Accounts.user_id == user_id))
            user = result.scalars().first()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")

            return {
                "user_id": user_id,
                "scopes": scopes,
                "client_id": token_data.get("client_id"),
                "access_token": token,
            }
    except httpx.HTTPError:
        raise HTTPException(status_code=500, detail="Failed to validate token")


async def store_tokens(db: AsyncSession, user_id: str, access_token: str, refresh_token: str | None):
    result = await db.execute(select(Accounts).where(Accounts.user_id == user_id))
    user = result.scalars().first()
    if user:
        user.access_token = access_token
        user.refresh_token = refresh_token
        await db.commit()
    else:
        new_user = Accounts(user_id=user_id, access_token=access_token, refresh_token=refresh_token)
        db.add(new_user)
        await db.commit()
