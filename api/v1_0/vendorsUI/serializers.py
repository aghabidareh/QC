from pydantic import BaseModel, field_validator
from typing import Optional, List
import re


class Vendor(BaseModel):
    vendor_identifier: Optional[int]
    vendor_name_persian: Optional[str]
    vendor_name_english: Optional[str]
    phone_number_of_owner: Optional[str]
    is_active: Optional[bool]
    the_number_of_purchase: Optional[int]
    the_number_of_products: Optional[int]
    the_number_of_sold_products: Optional[int]

    class Config:
        from_attributes = True


class Vendors(BaseModel):
    vendors: List[Vendor]
    count: int


class VendorCreate(BaseModel):
    vendor_identifier: Optional[int]
    vendor_name_persian: Optional[str]
    vendor_name_english: Optional[str]
    phone_number_of_owner: Optional[str]
    is_active: Optional[bool]
    the_number_of_purchase: Optional[int]
    the_number_of_products: Optional[int]
    the_number_of_sold_products: Optional[int]

    @field_validator('phone_number_of_owner')
    @classmethod
    def validate_phone_number(cls, value):
        pattern = re.compile(r"^09\d{9}$")
        if not re.match(pattern, value):
            raise ValueError("شماره تلفن معتبر نمی‌باشد! باید با 09 شروع شود و 11 رقم باشد.")

        if not value.isascii() or not value.isdigit():
            raise ValueError("شماره تلفن باید فقط شامل اعداد انگلیسی (0-9) باشد.")

        return value

    @field_validator('vendor_name_persian')
    @classmethod
    def validate_vendor_name_persian(cls, value):
        length_of_vendor_name_persian = len(value)
        if length_of_vendor_name_persian < 6:
            raise ValueError("در اسم فارسی یک غرفه، حروف نمیتوانند کمتر از ۶ کاراکتر باشند!")

        if length_of_vendor_name_persian > 90:
            raise ValueError("در اسم فارسی یک غرفه، تعداد حروف نمیتواند از ۹۰ کاراکتر تخطی کند.")

        return value

    @field_validator('vendor_name_english')
    @classmethod
    def validate_vendor_name_english(cls, value):
        length_of_vendor_name_english = len(value)
        if length_of_vendor_name_english < 3:
            raise ValueError("در اسم انگلیسی یک غرفه، حروف نمیتوانند کمتر از ۳ کاراکتر باشند!")

        if length_of_vendor_name_english > 120:
            raise ValueError("در اسم انگلیسی یک غرفه، تعداد حروف نمیتواند از ۱۲۰ کاراکتر تخطی کند.")

        return value


class VendorUpdate(BaseModel):
    vendor_identifier: Optional[int]
    vendor_name_persian: Optional[str]
    vendor_name_english: Optional[str]
    phone_number_of_owner: Optional[str]
    is_active: Optional[bool]
    the_number_of_purchase: Optional[int]
    the_number_of_products: Optional[int]
    the_number_of_sold_products: Optional[int]


class Message(BaseModel):
    message: str
