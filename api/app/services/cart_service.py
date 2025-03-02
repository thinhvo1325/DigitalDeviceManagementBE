from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.cart_model import Cart
from cores.handler_response import handler_response
from cores.common import create_token

class CartService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(Cart)

    async def create_rent(self, data, with_commit=True):
        try:
            result = await super().create(data, with_commit)
            return handler_response(200, data, "Tạo thông tin cho thuê thành công")
        except Exception as e:
            return handler_response(500, None, str(e))