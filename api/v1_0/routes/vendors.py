from fastapi import APIRouter, Query
import logging
from typing import List, Optional

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.sql import func

from api.database.database import get_db
from api.v1_0.models.vendors import VendorInformation
from api.v1_0.schemas.vnedors import Vendors, Vendor, Message, VendorCreate, VendorUpdate

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])
logger = logging.getLogger(__name__)


@vendor_router.get("/", response_model=Vendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db),
):
    count_query = select(func.count(func.distinct(VendorInformation.id))).select_from(Vendors)
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
    rows = result.fetchall()

    vendors =[
        Vendor(
            vendor_identifier=vendor.vendor_identifier,
            vendor_name_english=vendor.vendor_name_english,
            vendor_name_persian=vendor.vendor_name_persian,
            phone_number_of_owner=vendor.phone_number_of_owner,
            the_number_of_products=vendor.the_number_of_products,
            the_number_of_purchase=vendor.the_number_of_purchase,
            the_number_of_sold_products=vendor.the_number_of_sold_products,
            is_active=vendor.is_active,
        )
        for vendor in rows
    ]

    return Vendors(count=total_count, vendors=vendors)


@vendor_router.get("/{vendor_id}", response_model=Vendor,
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
    row = result.first()

    return Vendor(
        vendor_identifier=row.vendor_identifier,
        vendor_name_english=row.vendor_name_english,
        vendor_name_persian=row.vendor_name_persian,
        phone_number_of_owner=row.phone_number_of_owner,
        the_number_of_products=row.the_number_of_products,
        the_number_of_purchase=row.the_number_of_purchase,
        the_number_of_sold_products=row.the_number_of_sold_products,
        is_active=row.is_active,
    )


@vendor_router.get("/search", response_model=Vendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam which is searched",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors_search(
        vendor_name: str = Query(None, description="the user can search english or persian name, both"),
        db: AsyncSession = Depends(get_db),
):
    pass


@vendor_router.post("/add", response_model=Message,
                    description="Create a new vendor whom want to connect to Quick Commerce in Basalam",
                    response_description="Success Message",
                    status_code=201)
async def create_vendor(vendor_info: VendorCreate):
    pass


@vendor_router.post("/add-multiple", response_model=Message,
                    description="Add new vendors whom want to connect to Quick Commerce in Basalam",
                    response_description="Success Message",
                    status_code=201)
async def create_vendors_multiple(vendor_infos: List[VendorCreate]):
    pass


@vendor_router.put("/update/{vendor_id}", response_model=Message,
                   description="Update a specific vendor",
                   response_description="Success Message",
                   status_code=200)
async def update_vendor(vendor_id: int, vendor_info: VendorUpdate):
    pass


@vendor_router.put("/update-multiple", response_model=Message,
                   description="Update a specific vendors",
                   response_description="Success Message",
                   status_code=200)
async def update_vendors_multiple(vendor_infos: List[VendorUpdate]):
    pass


@vendor_router.delete("/delete/{vendor_id}", response_model=Message,
                      description="Delete a specific vendor",
                      response_description="Success Message",
                      status_code=200)
async def delete_vendor(vendor_id: int):
    pass


@vendor_router.delete("/delete-multiple", response_model=Message,
                      description="Delete a specific vendors",
                      response_description="Success Message",
                      status_code=200)
async def delete_vendors_multiple(vendor_ids: List[int]):
    pass

@vendor_router.delete("/delete-all", response_model=Message,
                      description="Delete all vendors",
                      response_description="Success Message",
                      status_code=200)
async def delete_all_vendors():
    pass
