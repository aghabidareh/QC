import logging
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
from api.v1_0.accounts.utils import create_access_token

logger = logging.getLogger(__name__)

account_router = APIRouter(prefix="/accounts", tags=["Accounts"])

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=AUTHORIZE_URL,
    tokenUrl=TOKEN_URL,
)

VALIDATE_URL = "https://auth.basalam.com/validate"


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


@account_router.get("/login")
async def login():
    scopes = ["vendor.profile.read", "customer.profile.read", "vendor.product.read"]
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": "&".join(scopes),
        "state": 1
    }
    auth_url = f"{AUTHORIZE_URL}?client_id={params['client_id']}&scope={params['scope']}&redirect_uri={params['redirect_uri']}&state={params['state']}"
    print(auth_url)
    logger.info(f"Redirecting user to {auth_url}")
    return RedirectResponse(url=auth_url)


@account_router.get("/callback")
async def callback(code: str, db: AsyncSession = Depends(get_db)):
    print(f'code: {code}')
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "redirect_uri": REDIRECT_URI,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                },
                headers={
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                },
            )
            if response.status_code != 200:
                logger.error(f"Token exchange failed: {response.text}")
                raise HTTPException(status_code=400, detail="Failed to obtain access token")

            token_data = response.json()

            print(f'token data :{token_data}')

            access_token = token_data.get("access_token")
            refresh_token = token_data.get("refresh_token")
            user_id = token_data.get("user_id")

            if not access_token or not user_id:
                raise HTTPException(status_code=400, detail="Invalid token response")

            await store_tokens(db, user_id, access_token, refresh_token)
            logger.info(f"Tokens stored for user {user_id}")

            local_token = create_access_token(data={"sub": user_id})
            return {"access_token": local_token, "token_type": "bearer"}
    except httpx.HTTPError:
        logger.error("HTTP error during token exchange")
        raise HTTPException(status_code=500, detail="Failed to communicate with auth server")


@account_router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "refresh_token",
                    "refresh_token": refresh_token,
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                },
            )
            if response.status_code != 200:
                logger.error(f"Token refresh failed: {response.text}")
                raise HTTPException(status_code=400, detail="Failed to refresh token")

            token_data = response.json()
            access_token = token_data.get("access_token")
            new_refresh_token = token_data.get("refresh_token")
            user_id = token_data.get("user_id")

            if not access_token or not user_id:
                raise HTTPException(status_code=400, detail="Invalid token response")

            await store_tokens(db, user_id, access_token, new_refresh_token)
            logger.info(f"Tokens refreshed for user {user_id}")

            local_token = create_access_token(data={"sub": user_id})
            return {"access_token": local_token, "token_type": "bearer"}
    except httpx.HTTPError:
        logger.error("HTTP error during token refresh")
        raise HTTPException(status_code=500, detail="Failed to communicate with auth server")


@account_router.get("/client-token")
async def get_client_token():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                TOKEN_URL,
                data={
                    "grant_type": "client_credentials",
                    "client_id": CLIENT_ID,
                    "client_secret": CLIENT_SECRET,
                    "scope": "customer.wallet:spend.write",
                },
            )
            if response.status_code != 200:
                logger.error(f"Client token request failed: {response.text}")
                raise HTTPException(status_code=400, detail="Failed to obtain client token")

            token_data = response.json()
            access_token = token_data.get("access_token")
            logger.info("Client token obtained")
            return {"access_token": access_token, "token_type": "bearer"}
    except httpx.HTTPError:
        logger.error("HTTP error during client token request")
        raise HTTPException(status_code=500, detail="Failed to communicate with auth server")
