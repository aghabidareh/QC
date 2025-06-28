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

class ActiveVendor(BaseModel):
    vendor_id: int
    profile_id: Optional[int]
    profile_name: Optional[str]
    working_time: Optional[List[dict]]
    extra : Optional[dict]

class ActiveVendors(BaseModel):
    vendors: List[ActiveVendor]
    count: int

class Profile(BaseModel):
    id: int
    title: Optional[str]
    extra: Optional[dict]

class Profiles(BaseModel):
    profiles: List[Profile]
    count: int
