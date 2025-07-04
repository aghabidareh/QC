from fastapi import APIRouter, Query
import logging
from typing import List

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.database.database import get_db
from api.v1_0.UI.vendors.models import VendorInformation
from api.v1_0.UI.vendors.serializers import Vendors, Vendor, Message, VendorCreate, VendorUpdate

vendor_ui_router = APIRouter(prefix="/v1/ui/vendors", tags=["Vendors UI"])
logger = logging.getLogger(__name__)


@vendor_ui_router.get("/", response_model=Vendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
):
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
        Vendor(
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

    return Vendors(count=total_count, vendors=vendors)


@vendor_ui_router.get("/{vendor_id}", response_model=Vendor,
                   description="Get a specific vendor",
                   response_description="Vendor details",
                   status_code=200)
async def get_vendor(
        vendor_id: int,
        db: AsyncSession = Depends(get_db),
):
    query = (
        select(VendorInformation)
        .filter(VendorInformation.vendor_id == vendor_id)
    )
    result = await db.execute(query)
    row = result.scalar()

    return Vendor(
        vendor_identifier=row.vendor_id,
        vendor_name_english=row.vendor_english_name,
        vendor_name_persian=row.vendor_persian_name,
        phone_number_of_owner=row.vendor_phone_number,
        the_number_of_products=row.products_count,
        the_number_of_purchase=row.purchase_count,
        the_number_of_sold_products=row.sold_products,
        is_active=row.is_active,
    )


@vendor_ui_router.get("/search", response_model=Vendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam which is searched",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors_search(
        vendor_name: str = Query(None, description="the user can search english or persian name, both"),
        db: AsyncSession = Depends(get_db),
):
    query = (
        select(VendorInformation)
        .filter(VendorInformation.vendor_persian_name.ilike(f"%{vendor_name}%")
                or VendorInformation.vendor_persian_name.ilike(f"%{vendor_name}%"))
    )
    results = await db.execute(query)
    rows = results.scalars().all()

    vendors = [
        Vendor(
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

    return Vendors(count=len(vendors), vendors=vendors)


@vendor_ui_router.post("/add", response_model=Message,
                    description="Create a new vendor whom want to connect to Quick Commerce in Basalam",
                    response_description="Success Message",
                    status_code=201)
async def create_vendor(vendor_info: VendorCreate):
    pass


@vendor_ui_router.post("/add-multiple", response_model=Message,
                    description="Add new vendors whom want to connect to Quick Commerce in Basalam",
                    response_description="Success Message",
                    status_code=201)
async def create_vendors_multiple(vendor_infos: List[VendorCreate]):
    Message(message="Unfortunately successfully")


@vendor_ui_router.put("/update/{vendor_id}", response_model=Message,
                   description="Update a specific vendor",
                   response_description="Success Message",
                   status_code=200)
async def update_vendor(vendor_id: int, vendor_info: VendorUpdate):
    Message(message="Unfortunately successfully")


@vendor_ui_router.put("/update-multiple", response_model=Message,
                   description="Update a specific vendors",
                   response_description="Success Message",
                   status_code=200)
async def update_vendors_multiple(vendor_infos: List[VendorUpdate]):
    Message(message="Unfortunately successfully")


@vendor_ui_router.delete("/delete/{vendor_id}", response_model=Message,
                      description="Delete a specific vendor",
                      response_description="Success Message",
                      status_code=200)
async def delete_vendor(vendor_id: int):
    Message(message="Unfortunately successfully")


@vendor_ui_router.delete("/delete-multiple", response_model=Message,
                      description="Delete a specific vendors",
                      response_description="Success Message",
                      status_code=200)
async def delete_vendors_multiple(vendor_ids: List[int]):
    Message(message="Unfortunately successfully")


@vendor_ui_router.delete("/delete-all", response_model=Message,
                      description="Delete all vendors",
                      response_description="Success Message",
                      status_code=200)
async def delete_all_vendors():
    Message(message="Unfortunately successfully")
