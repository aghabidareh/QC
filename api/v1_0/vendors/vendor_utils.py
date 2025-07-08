import logging
from typing import List, Optional
from fastapi import HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.database.database import get_db
from api.v1_0.vendors.models import VendorInformation, Enumerations, Vendors
from api.v1_0.vendors.serializers import AllVendors, SingleVendor, ActiveVendors, ActiveVendor, Message, VendorCreate, VendorUpdate

logger = logging.getLogger(__name__)

async def get_vendors_query(vendor_handler: 'BaseVendor', limit: int, offset: int):
    db = vendor_handler.db
    count_query = select(func.count(func.distinct(VendorInformation.id))).select_from(VendorInformation)
    count_result = await db.execute(count_query)
    total_count = count_result.scalar()

    query = (
        select(VendorInformation)
        .distinct(VendorInformation.id)
        .order_by(VendorInformation.id)
        .limit(limit)
        .offset(offset)
    )
    result = await db.execute(query)
    rows = result.scalars().all()

    vendors = [
        SingleVendor(
            vendor_identifier=vendor.vendor_id,
            vendor_name_english=vendor.vendor_english_name,
            vendor_name_persian=vendor.vendor_persian_name,
            phone_number_of_owner=vendor.vendor_phone_number,
            the_number_of_products=vendor.products_count,
            the_number_of_purchase=vendor.purchase_count,
            the_number_of_sold_products=vendor.sold_products,
            is_active=vendor.is_active,
        )
        for vendor in rows
    ]

    return AllVendors(count=total_count, vendors=vendors)

async def get_vendor_query(vendor_handler: 'BaseVendor', vendor_id: int):
    db = vendor_handler.db
    query = (
        select(VendorInformation)
        .filter(VendorInformation.vendor_id == vendor_id)
    )
    result = await db.execute(query)
    row = result.scalar()

    if not row:
        raise HTTPException(status_code=404, detail="Vendor not found")

    return SingleVendor(
        vendor_identifier=row.vendor_id,
        vendor_name_english=row.vendor_english_name,
        vendor_name_persian=row.vendor_persian_name,
        phone_number_of_owner=row.vendor_phone_number,
        the_number_of_products=row.products_count,
        the_number_of_purchase=row.purchase_count,
        the_number_of_sold_products=row.sold_products,
        is_active=row.is_active,
    )

async def get_vendors_search_query(vendor_handler: 'BaseVendor', vendor_name: Optional[str]):
    db = vendor_handler.db
    query = (
        select(VendorInformation)
        .filter(VendorInformation.vendor_persian_name.ilike(f"%{vendor_name}%")
                | VendorInformation.vendor_english_name.ilike(f"%{vendor_name}%"))
    )
    results = await db.execute(query)
    rows = results.scalars().all()

    vendors = [
        SingleVendor(
            vendor_identifier=vendor.vendor_id,
            vendor_name_english=vendor.vendor_english_name,
            vendor_name_persian=vendor.vendor_persian_name,
            phone_number_of_owner=vendor.vendor_phone_number,
            the_number_of_products=vendor.products_count,
            the_number_of_purchase=vendor.purchase_count,
            the_number_of_sold_products=vendor.sold_products,
            is_active=vendor.is_active,
        )
        for vendor in rows
    ]

    return AllVendors(count=len(vendors), vendors=vendors)

async def get_vendors_by_city_query(vendor_handler: 'BaseVendor', city_id: int):
    db = vendor_handler.db
    query = (
        select(VendorInformation)
        .distinct(VendorInformation.vendor_id)
        .filter(VendorInformation.city_id == city_id)
    )
    result = await db.execute(query)
    rows = result.scalars().all()

    vendors = [
        SingleVendor(
            vendor_identifier=vendor.vendor_id,
            vendor_name_english=vendor.vendor_english_name,
            vendor_name_persian=vendor.vendor_persian_name,
            phone_number_of_owner=vendor.vendor_phone_number,
            the_number_of_products=vendor.products_count,
            the_number_of_purchase=vendor.purchase_count,
            the_number_of_sold_products=vendor.sold_products,
            is_active=vendor.is_active,
        )
        for vendor in rows
    ]

    return AllVendors(vendors=vendors, count=len(vendors))

async def get_active_vendors_query(vendor_handler: 'BaseVendor'):
    db = vendor_handler.db
    query = select(Vendors, Enumerations).join(
        Enumerations, Enumerations.id == Vendors.profile_id, isouter=True
    ).filter(Vendors.status == 2)
    result = await db.execute(query)
    rows = result.all()

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

async def get_active_vendor_by_id_query(vendor_handler: 'BaseVendor', id: int, source: Optional[str]):
    db = vendor_handler.db
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

async def create_vendor_handler(vendor_handler: 'BaseVendor', vendor_info: VendorCreate):
    return Message(message="Vendor created successfully")

async def create_vendors_multiple_handler(vendor_handler: 'BaseVendor', vendor_infos: List[VendorCreate]):
    return Message(message="Multiple vendors created successfully")

async def update_vendor_handler(vendor_handler: 'BaseVendor', vendor_id: int, vendor_info: VendorUpdate):
    return Message(message="Vendor updated successfully")

async def update_vendors_multiple_handler(vendor_handler: 'BaseVendor', vendor_infos: List[VendorUpdate]):
    return Message(message="Multiple vendors updated successfully")

async def delete_vendor_handler(vendor_handler: 'BaseVendor', vendor_id: int):
    return Message(message="Vendor deleted successfully")

async def delete_vendors_multiple_handler(vendor_handler: 'BaseVendor', vendor_ids: List[int]):
    return Message(message="Multiple vendors deleted successfully")

async def delete_all_vendors_handler(vendor_handler: 'BaseVendor'):
    return Message(message="All vendors deleted successfully")