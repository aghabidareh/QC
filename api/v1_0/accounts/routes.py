from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.serializers import Account
from api.v1_0.accounts.utils import create_access_token


account_router = APIRouter(prefix="/accounts", tags=["Accounts"])

