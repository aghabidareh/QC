import logging
from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from api.database.database import get_db
from api.v1_0.vendors.serializers import AllVendors, SingleVendor, ActiveVendors, Message, VendorCreate, VendorUpdate
from api.v1_0.vendors.base_vendor import BaseVendor
from api.v1_0.vendors.vendor_utils import (
    get_vendors_query,
    get_vendor_query,
    get_vendors_search_query,
    get_vendors_by_city_query,
    get_active_vendors_query,
    get_active_vendor_by_id_query,
    create_vendor_handler,
    create_vendors_multiple_handler,
    update_vendor_handler,
    update_vendors_multiple_handler,
    delete_vendor_handler,
    delete_vendors_multiple_handler,
    delete_all_vendors_handler
)

vendor_router = APIRouter(prefix="/v1/vendors", tags=["Vendors"])
logger = logging.getLogger(__name__)


@vendor_router.get("/", response_model=AllVendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors(
        limit: int = Query(10, ge=1, le=100),
        offset: int = Query(0, ge=0),
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await get_vendors_query(vendor_handler, limit, offset)


@vendor_router.get("/{vendor_id}", response_model=SingleVendor,
                   description="Get a specific vendor",
                   response_description="Vendor details",
                   status_code=200)
async def get_vendor(
        vendor_id: int,
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await get_vendor_query(vendor_handler, vendor_id)


@vendor_router.get("/search", response_model=AllVendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam which is searched",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors_search(
        vendor_name: str = Query(None, description="the user can search english or persian name, both"),
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await get_vendors_search_query(vendor_handler, vendor_name)


@vendor_router.get("/city/{city_id}", response_model=AllVendors,
                   description='Get vendors by the city identifier',
                   status_code=200)
async def get_single_by_city_id(
        city_id: int,
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await get_vendors_by_city_query(vendor_handler, city_id)


@vendor_router.get('/actives/list', response_model=ActiveVendors,
                   description='Get all active vendors',
                   status_code=200)
async def all_actives(
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await get_active_vendors_query(vendor_handler)


@vendor_router.get('/actives/single/{id}', response_model=ActiveVendors,
                   description='Get the active vendor by id',
                   status_code=200)
async def get_active_by_id(
        id: int,
        source: Optional[str] = Query(None, enum=["vendor", "profile"]),
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await get_active_vendor_by_id_query(vendor_handler, id, source)


@vendor_router.post("/add", response_model=Message,
                    description="Create a new vendor whom want to connect to Quick Commerce in Basalam",
                    response_description="Success Message",
                    status_code=201)
async def create_vendor(
        vendor_info: VendorCreate,
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await create_vendor_handler(vendor_handler, vendor_info)


@vendor_router.post("/add-multiple", response_model=Message,
                    description="Add new vendors whom want to connect to Quick Commerce in Basalam",
                    response_description="Success Message",
                    status_code=201)
async def create_vendors_multiple(
        vendor_infos: List[VendorCreate],
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await create_vendors_multiple_handler(vendor_handler, vendor_infos)


@vendor_router.put("/update/{vendor_id}", response_model=Message,
                   description="Update a specific vendor",
                   response_description="Success Message",
                   status_code=200)
async def update_vendor(
        vendor_id: int,
        vendor_info: VendorUpdate,
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await update_vendor_handler(vendor_handler, vendor_id, vendor_info)


@vendor_router.put("/update-multiple", response_model=Message,
                   description="Update a specific vendors",
                   response_description="Success Message",
                   status_code=200)
async def update_vendors_multiple(
        vendor_infos: List[VendorUpdate],
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await update_vendors_multiple_handler(vendor_handler, vendor_infos)


@vendor_router.delete("/delete/{vendor_id}", response_model=Message,
                      description="Delete a specific vendor",
                      response_description="Success Message",
                      status_code=200)
async def delete_vendor(
        vendor_id: int,
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await delete_vendor_handler(vendor_handler, vendor_id)


@vendor_router.delete("/delete-multiple", response_model=Message,
                      description="Delete a specific vendors",
                      response_description="Success Message",
                      status_code=200)
async def delete_vendors_multiple(
        vendor_ids: List[int],
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await delete_vendors_multiple_handler(vendor_handler, vendor_ids)


@vendor_router.delete("/delete-all", response_model=Message,
                      description="Delete all vendors",
                      response_description="Success Message",
                      status_code=200)
async def delete_all_vendors(
        db: AsyncSession = Depends(get_db)
):
    vendor_handler = BaseVendor(db)
    return await delete_all_vendors_handler(vendor_handler)
