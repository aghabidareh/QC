from pydantic import BaseModel


class Account(BaseModel):
    phone: str
    password: str
