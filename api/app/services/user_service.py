from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.user_model import User
from cores.handler_response import handler_response
from cores.common import create_token

class UserService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(User)

    async def find_user(self, username, password, is_google):
        try:
            checker = await self.search(fields={'username': username, "password": password}, is_absolute=True)
            if checker is None:
                if is_google:
                    data = {
                        'username': username,
                        'password': password
                    }
                    new_account = await self.create(data, with_commit=True)
                    new_account = new_account.__dict__
                    new_account.pop('_sa_instance_state')
                    new_account['access_token'] = create_token(new_account)
                    return handler_response(200, new_account, "Tìm thấy user")
                return handler_response(403, None, "Sai tài khoản hoặc mật khẩu")
            data = checker.__dict__
            data.pop('_sa_instance_state')
            data['access_token'] = create_token(data)
            return handler_response(200, data, "Tìm thấy user")
        except Exception as e:
            return handler_response(500, None, str(e))
        
    async def create_user(self, data: User, with_commit=True):
        try: 
            checker = await self.search(fields={'username': data.username}, is_absolute=True)
        
            if checker is not None:
                return handler_response(400, None, "User đã tồn tại")
            
            result = await super().create(data, with_commit)
            result = result.__dict__
            result.pop('_sa_instance_state')
            result['access_token'] = create_token(result)
            return handler_response(200, result, "Tạo user thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
        
    
    async def update_user(self, id, data, with_commit=True):
        try:
            checker = await self.find(id)
            if checker is None:
                return handler_response(403, None, "Sai tài khoản hoặc mật khẩu")
            new_password = data.get('new_password')
            if new_password is not None:
                data['password'] = new_password
            result = await super().update(id=id, data=data, with_commit=with_commit)
            return handler_response(200, data, "Cập nhật user thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
    

    async def delete_user(self, id, with_commit=True):
        try:
            checker = await self.find(id)
            if checker is None:
                return handler_response(404, None, "User không tồn tại")
            
            result = await super().delete(id, with_commit)
            return handler_response(200, result, "Xóa user thành công")
        except Exception as e:
            return handler_response(500, None, str(e))