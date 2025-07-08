import logging

from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from api.database.database import get_db
from api.v1_0.profiles.base_profile import BaseProfile
from api.v1_0.profiles.profile_utils import get_profiles_handler
from api.v1_0.vendors.models import Enumerations
from api.v1_0.profiles.serializers import Profile, Profiles

profile_main_router = APIRouter(prefix="/v1/main/profiles", tags=["Profiles Main"])
logger = logging.getLogger(__name__)


@profile_main_router.get('/profiles', response_model=Profiles,
                         description='Get the profiles',
                         status_code=200)
async def get_profiles(
        db: AsyncSession = Depends(get_db),
):
    profile_handler = BaseProfile(db)
    return await get_profiles_handler(profile_handler)
