from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship

from api.database.database import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    
    user_id = Column(String, primary_key=True)
    access_token = Column(String, nullable=False)
    refresh_token = Column(String, nullable=False)
