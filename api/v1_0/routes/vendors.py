from fastapi import APIRouter
import logging

from api.v1_0.schemas.vnedors import Vendors, Vendor

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])
logger = logging.getLogger(__name__)

@vendor_router.get("/", response_model=Vendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors():
    pass

@vendor_router.get("/{vendor_id}", response_model=Vendor,
                   description="Get a specific vendor",
                   response_description="Vendor details",
                   status_code=200)
async def get_vendor(vendor_id: int):
    pass
