from fastapi import APIRouter
import logging

from api.v1_0.schemas.vnedors import Vendors, Vendor, Message, VendorCreate, VendorUpdate

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

@vendor_router.get("/search", response_model=Vendors,
                   description="Get all vendors connected to the Quick Commerce in Basalam which is searched",
                   response_description="All vendors connected to the Quick Commerce in Basalam",
                   status_code=200)
async def get_vendors_search():
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
async def create_vendors_multiple(vendor_infos: [VendorCreate]):
    pass

@vendor_router.put("/update/{vendor_id}", response_model=Message,
                   description="Update a specific vendor",
                   response_description="Success Message",
                   status_code=200)
async def update_vendor(vendor_id: int, vendor_info: VendorUpdate):
    pass
