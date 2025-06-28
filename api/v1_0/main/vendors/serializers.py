from pydantic import BaseModel, field_validator
from typing import Optional, List
import re


class VendorIdSingle(BaseModel):
    vendor_id: int

    class Config:
        from_attributes = True


class VendorIdSerializer(BaseModel):
    vendors: List[VendorIdSingle]
    count: int

class ActiveVendors(BaseModel):
    vendor_id: int
    profile_id: int
    profile_name: str
    working_time: dict
    extra : dict
