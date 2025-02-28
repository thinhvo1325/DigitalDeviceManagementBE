from cores.databases.db_helper import Base
from sqlalchemy import Column, Integer, String, Text

class User(Base):
    """
    Danh sách người dùng
    """
    __tablename__ = 'users'

    id = Column(Integer, nullable=False, primary_key=True)
    
    fullname = Column(Text, nullable=True)
    phone = Column(Text, nullable=True)
    address = Column(Text, nullable=True)
    email = Column(Text, nullable=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)
