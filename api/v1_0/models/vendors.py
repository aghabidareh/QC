from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from api.database.database import Base


class Enumerations(Base):
    pass


class Vendors(Base):
    pass


class VendorInformation(Base):
    pass
