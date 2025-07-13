from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.accounts.configs import AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI, TOKEN_URL, CLIENT_SECRET
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.serializers import Account
from api.v1_0.accounts.utils import create_access_token

account_router = APIRouter(prefix="/accounts", tags=["Accounts"])

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZE_URL,
    tokenUrl=TOKEN_URL,
)

VALIDATE_URL = "https://auth.basalam.com/validate"
KONG_GATEWAY_URL = "https://api.basalam.com"


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
