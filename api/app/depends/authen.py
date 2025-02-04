from services.user_service import UserService
from fastapi import HTTPException, status, Depends, Header
from fastapi.security import HTTPBearer, APIKeyHeader
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from models.user_model import User
from cores.common import decode_JWT
reusable_oauth2 = HTTPBearer(scheme_name='Authorization')

async def verify_user(
    db: AsyncSession = Depends(get_db), 
    http_authorization_credentials = Depends(reusable_oauth2)
) -> User:
    uid = decode_JWT(http_authorization_credentials.credentials).get('id', None)
    print(uid)
    if uid is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid user token')
   
    user_service = UserService(db)
    return await user_service.find(uid)
    
    
class AuthenService(SqlAchemyAbstract):
    """_summary_
    Desc:
        Lớp này chịu trách nhiệm thực thi việc kiểm tra tính hợp lệ của người dùng khi nhận được yêu cầu thực hiện tính năng
    """
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db), fake_Users = Depends(verify_user)):
        self._db = db
        self.fake_user = fake_Users