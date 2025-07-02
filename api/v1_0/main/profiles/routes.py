import logging

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.UI.vendors.models import Enumerations
from api.v1_0.main.profiles.serializers import Profile, Profiles

profile_main_router = APIRouter(prefix="/v1/main/profiles", tags=["Profiles Main"])
logger = logging.getLogger(__name__)

@profile_main_router.get('/profiles', response_model=Profiles,
                        description='Get the profiles',
                        status_code=200)
async def get_profiles(
        db: AsyncSession = Depends(get_db),
):
    query = select(Enumerations).filter(Enumerations.parent_id==5).filter(Enumerations.status==True)
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
