
from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.rent_detail_model import RentDetail
from cores.handler_response import handler_response
from cores.common import create_token

class RentDeailService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(RentDetail)
    
    async def create_rent_detail(self, data: RentDetail, with_commit=True):
        try:
            result = await super().create(data, with_commit)
            return handler_response(200, data, "Tạo thông tin cho thuê thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
        