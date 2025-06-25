from fastapi import APIRouter
import logging

vendor_router = APIRouter(prefix="/vendors", tags=["Vendors"])
logger = logging.getLogger(__name__)


