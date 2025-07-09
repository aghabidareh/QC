from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship

from api.database.database import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer, autoincrement=True, primary_key=True)
    phone_number = Column(String, nullable=False)
    password = Column(String, nullable=False)
