from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, PickleType, Text
from sqlalchemy.sql import func

class RentDetail(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'rental_detail'

    id = Column(Integer, nullable=False, primary_key=True)
    
    rent_id = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=True)
    rent_price = Column(JSON, nullable=True)
    
    start_date = Column(DateTime, nullable=True)
    end_date = Column(DateTime, nullable=True)
    total_price = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)
    
    