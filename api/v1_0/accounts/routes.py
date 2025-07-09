from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.accounts.models import Accounts
from api.v1_0.accounts.serializers import Account
from api.v1_0.accounts.utils import create_access_token


account_router = APIRouter(prefix="/accounts", tags=["Accounts"])

@account_router.post("/signup", response_description="the information of the new user",
                            status_code=201)
async def signup(account: Account, db: AsyncSession = Depends(get_db)):
    stmt = select(Accounts).where(Accounts.phone_number == account.phone_number)
    result = await db.execute(stmt)
    existing_owner = result.scalar()

    if existing_owner:
        raise HTTPException(status_code=400, detail="شماره تلفن وارد شده به صورت پیش فرض وجود دارد.")

    new_account = Accounts(
        phone_number=account.phone_number,
        password=account.password
    )
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)

    return new_account


@account_router.post('/login', response_description="the token for the user",
                            status_code=200)
async def login(account: Account, db: AsyncSession = Depends(get_db)):
    stmt = select(Accounts).where(Accounts.phone_number == account.phone_number)
    result = await db.execute(stmt)
    existing_owner = result.scalar()

    if not existing_owner:
        raise HTTPException(status_code=401, detail="شماره تلفن و یا رمز عبور نادرست میباشد.")

    access_token = create_access_token(data={
        "sub": existing_owner.phone_number,
    })

    return {"access_token": access_token, "token_type": "bearer"}
