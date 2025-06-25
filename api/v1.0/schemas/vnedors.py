from pydantic import BaseModel, field_validator


class VendorsBase(BaseModel):
    vendor_name: str
    phone_number_of_owner: str
    is_active: bool
    the_number_of_purchase: int


class Vendors(BaseModel):
    pass
