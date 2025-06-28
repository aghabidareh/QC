from fastapi import APIRouter, Query, HTTPException
import logging
from typing import List, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.database.database import get_db
from api.v1_0.UI.vendors.models import VendorInformation, Vendors, Enumerations


profile_main_router = APIRouter(prefix="/main/profiles", tags=["Profiles Main"])
logger = logging.getLogger(__name__)


