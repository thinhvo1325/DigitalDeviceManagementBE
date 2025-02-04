from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean, JSON, PickleType, Text
from sqlalchemy.sql import func

class CommentModel(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'comment_model'

    id = Column(Integer, nullable=False, primary_key=True)
    
    user_id = Column(Integer, nullable=False)
    rent_id = Column(Integer, nullable=False)
    
    username = Column(String(100), nullable=True)
    product_name = Column(String(100), nullable=True)
    star = Column(Integer, nullable=True)
    content = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    deleted_at = Column(DateTime, nullable=True)