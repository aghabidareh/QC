from pydantic import BaseModel, field_validator
import re

class Account(BaseModel):
    phone: str
    password: str

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, value):
        pattern = re.compile(r"^09\d{9}$")
        if not re.match(pattern, value):
            raise ValueError("شماره تلفن معتبر نمی‌باشد! باید با 09 شروع شود و 11 رقم باشد.")

        if not value.isascii() or not value.isdigit():
            raise ValueError("شماره تلفن باید فقط شامل اعداد انگلیسی (0-9) باشد.")

        return value
