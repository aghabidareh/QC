from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, Json, Boolean, DateTime
from sqlalchemy.orm import relationship

from api.database.database import Base


class Enumerations(Base):
    __tablename__ = 'enumerations'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    parent_id = Column(Integer, ForeignKey('enumerations.id', cascade="all, delete-orphan", ondelete="CASCADE"))
    text = Column(String)
    extra = Column(Json)
    status = Column(Boolean)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(DateTime, onupdate=datetime.now)


class Vendors(Base):
    __tablename__ = 'vendors'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vendor_id = Column(Integer)
    profile_id = Column(Integer, ForeignKey('enumerations.id', ondelete="CASCADE"))
    working_times = None
    start_date = Column(DateTime)
    extra = Column(Json)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(DateTime, onupdate=datetime.now)
    status = Column(Integer)


class VendorInformation(Base):
    __tablename__ = 'vendor_infos'
