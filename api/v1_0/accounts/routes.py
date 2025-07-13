from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.accounts.configs import AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI
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
async def callback():
    pass
