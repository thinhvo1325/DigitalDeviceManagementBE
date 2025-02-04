from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.rent_info_model import RentInfo
from cores.handler_response import handler_response
from cores.common import create_token

class RentService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(RentInfo)

    
    async def create_rent(self, data: RentInfo, with_commit=True):
        try:
            result = await super().create(data, with_commit)
            return handler_response(200, data, "Tạo thông tin cho thuê thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
        
    # async def find_user(self, username, password):
    #     try:
    #         checker = await self.search(fields={'username': username, "password": password}, is_absolute=True)
    #         if checker is None:
    #             return handler_response(403, None, "Sai tài khoản hoặc mật khẩu")
    #         data = checker.__dict__
    #         data.pop('_sa_instance_state')
    #         data['access_token'] = create_token(data)
    #         return handler_response(200, data, "Tìm thấy user")
    #     except Exception as e:
    #         return handler_response(500, None, str(e))