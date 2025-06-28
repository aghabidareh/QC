from fastapi import APIRouter, Query
import logging
from typing import List

vendor_main_router = APIRouter(prefix="/main/vendors", tags=["Vendors Main"])
logger = logging.getLogger(__name__)


