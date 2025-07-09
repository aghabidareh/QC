from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.serializers import Account
from api.v1_0.accounts.utils import create_access_token


accounts_router = APIRouter(prefix="/accounts", tags=["Accounts"])

@accounts_router.post("/signup", response_description="the information of the new user",
                            status_code=201)
async def signup(owner: Account, db: AsyncSession = Depends(get_db)):
    pass


@accounts_router.post('/login', response_description="the token for the user",
                            status_code=200)
async def login(owner: Account, db: AsyncSession = Depends(get_db)):
    pass
