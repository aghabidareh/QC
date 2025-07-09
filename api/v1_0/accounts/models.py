from datetime import datetime
from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey, JSON, Boolean, DateTime
from sqlalchemy.orm import relationship

from api.database.database import Base


class Accounts(Base):
    __tablename__ = 'accounts'
    
    pass 
