from fastapi import APIRouter, Query
import logging
from typing import List

from api.v1_0.main.vendors.serializers import VendorIdSerializer

vendor_main_router = APIRouter(prefix="/main/vendors", tags=["Vendors Main"])
logger = logging.getLogger(__name__)

@vendor_main_router.get('/', response_model=VendorIdSerializer,
                        description='Get the identifier of Vendors',
                        status_code=200)
def get_all():
    pass
