from fastapi import APIRouter, Query
import logging
from typing import List

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.database.database import get_db
from api.v1_0.UI.vendors.models import VendorInformation

from api.v1_0.main.vendors.serializers import VendorIdSerializer, VendorIdBase

vendor_main_router = APIRouter(prefix="/main/vendors", tags=["Vendors Main"])
logger = logging.getLogger(__name__)


@vendor_main_router.get('/', response_model=VendorIdSerializer,
                        description='Get the identifier of Vendors',
                        status_code=200)
async def get_all(
        db: AsyncSession = Depends(get_db)
):
    count_query = select(func.count(func.distinct(VendorInformation.id))).select_from(VendorInformation)
    count_result = await db.execute(count_query)
    total_count = count_result.scalar()

    query = (
        select(VendorInformation.vendor_id)
        .distinct(VendorInformation.vendor_id)
    )
    result = await db.execute(query)
    rows = result.scalars().all()

    vendor_identifier = [
        VendorIdBase(
            vendor_id=row
        )
        for row in rows
    ]

    return VendorIdSerializer(vendors=vendor_identifier, count=total_count)
