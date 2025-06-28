from pydantic import BaseModel, field_validator
from typing import Optional, List
import re


class Profile(BaseModel):
    id: int
    title: Optional[str]
    extra: Optional[dict]

class Profiles(BaseModel):
    profiles: List[Profile]
    count: int
