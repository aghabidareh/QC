from fastapi import APIRouter, Query, HTTPException
import logging
from typing import List, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.database.database import get_db
from api.v1_0.UI.vendors.models import VendorInformation, Vendors, Enumerations

from api.v1_0.main.vendors.serializers import VendorIdSerializer, VendorIdSingle, ActiveVendors, ActiveVendor, Profiles, \
    Profile

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
        VendorIdSingle(
            vendor_id=row
        )
        for row in rows
    ]

    return VendorIdSerializer(vendors=vendor_identifier, count=total_count)


@vendor_main_router.get('/city/{city_id}', response_model=VendorIdSerializer,
                        description='Get the identifier of vendor by city identifier',
                        status_code=200)
async def get_single_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    query = (
        select(VendorInformation.vendor_id)
        .distinct(VendorInformation.vendor_id)
        .filter(VendorInformation.city_id == city_id)
    )
    result = await db.execute(query)
    rows = result.scalars().all()

    vendor_identifier = [
        VendorIdSingle(
            vendor_id=row
        )
        for row in rows
    ]

    return VendorIdSerializer(vendors=vendor_identifier, count=len(vendor_identifier))


@vendor_main_router.get('/active/{id}', response_model=ActiveVendors,
                        description='Get the active vendor by id',
                        status_code=200)
async def get_active_by_id(
        id: int,
        db: AsyncSession = Depends(get_db),
        source: Optional[str] = Query(None, enum=["vendor", "profile"])
):
    query = select(Vendors, Enumerations).join(
        Enumerations, Vendors.profile_id == Enumerations.id, isouter=True
    ).filter(Vendors.status == 2)
    if source == "vendor":
        query = query.filter(Vendors.vendor_id == id)
    elif source == "profile":
        query = query.filter(Vendors.profile_id == id)
    else:
        raise HTTPException(status_code=400, detail="Source must be 'vendor' or 'profile'")

    result = await db.execute(query)
    rows = result.all()

    if not rows:
        raise HTTPException(status_code=404, detail="Vendor not found")

    vendors = [
        ActiveVendor(
            vendor_id=row[0].vendor_id,
            profile_id=row[0].profile_id,
            profile_name=row[1].title,
            working_time=row[0].working_times if hasattr(row[0], 'working_times') else None,
            extra=row[0].extra
        )
        for row in rows
    ]

    return ActiveVendors(vendors=vendors, count=len(vendors))


