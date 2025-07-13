from pydantic import BaseModel, field_validator
import re

class Account(BaseModel):
    user_id: str
    access_token: str
    refresh_token: str | None = None
