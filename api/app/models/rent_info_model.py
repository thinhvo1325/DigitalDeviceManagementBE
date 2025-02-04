from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, PickleType, Text
from sqlalchemy.sql import func

class RentInfo(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'rental_information'

    id = Column(Integer, nullable=False, primary_key=True)
    
    user_id = Column(Integer, nullable=False)
    
    category = Column(String(100), nullable=True)
    title = Column(String(100), nullable=True)  
    description = Column(Text, nullable=True)
    
    images = Column(JSON, nullable=True)
    video = Column(JSON, nullable=True)
    rent_price = Column(JSON, nullable=True)
    
    address = Column(Text, nullable=True)
    cancel_policy = Column(Integer, nullable=True)
    sell_price = Column(String(20), nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)