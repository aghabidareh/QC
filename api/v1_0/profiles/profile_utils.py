import logging
from typing import List, Optional
from fastapi import HTTPException, Query, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.v1_0.profiles.serializers import Profile, Profiles
from api.v1_0.vendors.models import VendorInformation, Enumerations, Vendors

logger = logging.getLogger(__name__)


async def get_profiles_handler(profile_handler: 'BaseProfile'):
    db = profile_handler.db
    query = select(Enumerations).filter(Enumerations.parent_id == 5).filter(Enumerations.status == True)
    result = await db.execute(query)
    rows = result.scalars().all()

    profiles = [
        Profile(
            id=row.id,
            title=row.title,
            extra=row.extra,
        )
        for row in rows
    ]
    return Profiles(profiles=profiles, count=len(profiles))
