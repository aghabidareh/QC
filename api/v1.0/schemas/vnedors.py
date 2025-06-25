from pydantic import BaseModel, field_validator
from typing import Optional, List
import re


class VendorsBase(BaseModel):
    vendor_identifier: int
    vendor_name_persian: str
    vendor_name_english: str
    phone_number_of_owner: str
    is_active: bool
    the_number_of_purchase: int
    the_number_of_products: int
    the_number_of_sold_products: int

    @field_validator('phone_number_of_owner')
    @classmethod
    def validate_phone_number(cls, value):
        pattern = re.compile(r"^09\d{9}$")
        if not re.match(pattern, value):
            raise ValueError("شماره تلفن معتبر نمی‌باشد! باید با 09 شروع شود و 11 رقم باشد.")

        if not value.isascii() or not value.isdigit():
            raise ValueError("شماره تلفن باید فقط شامل اعداد انگلیسی (0-9) باشد.")

        return value

    class Config:
        from_attributes = True


class Vendors(BaseModel):
    vendors = List[VendorsBase]
    count: int

class VendorCreate(BaseModel):
    pass
