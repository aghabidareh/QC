from typing import Optional
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession


class BaseVendor:
    def __init__(self, db: AsyncSession, current_user: Optional[dict] = None):
        self.db = db
        self.current_user = current_user
