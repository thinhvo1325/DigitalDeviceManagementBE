from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, Text, JSON

class Cart(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'cart'

    id = Column(Integer, nullable=False, primary_key=True)
    
    user_id = Column(Integer, nullable=True)
    title = Column(Text, nullable=True)
    image = Column(Text, nullable=True)
    days = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    is_paid = Column(Integer, nullable=True)
    rent_price = Column(JSON, nullable=True)