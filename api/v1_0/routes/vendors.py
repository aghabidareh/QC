from fastapi import APIRouter
import logging

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])
logger = logging.getLogger(__name__)

@vendor_router.get("/", response_model=Vendors)
