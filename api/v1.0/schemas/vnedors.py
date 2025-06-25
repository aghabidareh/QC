from pydantic import BaseModel, field_validator
from typing import Optional, List


class VendorsBase(BaseModel):
    vendor_name: str
    phone_number_of_owner: str
    is_active: bool
    the_number_of_purchase: int

    @field_validator('phone_number_of_owner')
    @classmethod
    def validate_phone_number(cls, v):
        pass

class Vendors(BaseModel):
    vendors = List[VendorsBase]
    count: int
