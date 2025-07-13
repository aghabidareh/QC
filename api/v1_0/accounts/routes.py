from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.accounts.configs import AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI, TOKEN_URL, CLIENT_SECRET
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.serializers import Account
from api.v1_0.accounts.utils import create_access_token


account_router = APIRouter(prefix="/accounts", tags=["Accounts"])


@account_router.get("/login")
async def login():
    scopes = ['vendor.profile.read', 'vendor.profile.write', 'customer.profile.write', 'customer.profile.read', 'vendor.product.read']
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scopes),
    }

    auth_url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    return RedirectResponse(url=auth_url)


@account_router.get("/callback")
async def callback(code: str):
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
        )
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail="Failed to obtain access token")

        token_data = response.json()
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")

        return {"access_token": access_token, "refresh_token": refresh_token}
