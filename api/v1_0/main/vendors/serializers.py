from pydantic import BaseModel, field_validator
from typing import Optional, List
import re

class VendorIdBase(BaseModel):
    vendor_id: int

    class Config:
        from_attributes = True

class VendorIdSerializer(BaseModel):
    vendors: List[VendorIdBase]
    count: int
