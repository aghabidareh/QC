from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship

from api.database.database import Base


class Enumerations(Base):
    __tablename__ = 'enumerations'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    parent_id = Column(Integer, ForeignKey('enumerations.id', ondelete="CASCADE"))
    title = Column(String)
    extra = Column(JSON)
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
    extra = Column(JSON)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.now)
    deleted_at = Column(DateTime, onupdate=datetime.now)
    status = Column(Integer)


class VendorInformation(Base):
    __tablename__ = 'vendor_infos'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    vendor_id = Column(Integer)
    vendor_persian_name = Column(String)
    vendor_english_name = Column(String)
    vendor_phone_number = Column(String)
    is_active = Column(Boolean)
    purchase_count = Column(Integer)
    products_count = Column(Integer)
    sold_products = Column(Integer)
    same_city_orders = Column(Integer)
    vendor_url = Column(String)
    city_name = Column(String)
    city_id = Column(Integer)
    user_id = Column(Integer)
