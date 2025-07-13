from urllib.parse import urlencode

import httpx
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.testing.plugin.plugin_base import logging

from api.database.database import get_db
from api.v1_0.accounts.configs import AUTHORIZE_URL, CLIENT_ID, REDIRECT_URI, TOKEN_URL, CLIENT_SECRET
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.serializers import Account

account_router = APIRouter(prefix="/accounts", tags=["Accounts"])

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

VALIDATE_URL = "https://auth.basalam.com/validate"
KONG_GATEWAY_URL = "https://api.basalam.com"


@account_router.get("/login")
async def login():
    scopes = ["customer.wallet.read", "customer.wallet.write"]  # Adjust based on your needs
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": " ".join(scopes),
    }
    auth_url = f"{AUTHORIZE_URL}?{urlencode(params)}"
    logger.info(f"Redirecting user to {auth_url}")
    return RedirectResponse(url=auth_url)


