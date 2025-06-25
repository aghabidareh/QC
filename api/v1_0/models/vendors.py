from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger
from sqlalchemy.orm import relationship

from api.database.database import Base


class Enumerations(Base):
    __tablename__ = 'enumerations'


class Vendors(Base):
    __tablename__ = 'vendors'


class VendorInformation(Base):
    __tablename__ = 'vendor_infos'
