from cores.databases.db_helper import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException
from cores.sqlachemy_abstract.async_sqlachemy_abstract import SqlAchemyAbstract
from models.comment_model import CommentModel
from cores.handler_response import handler_response
from cores.common import create_token
from sqlalchemy.future import select

class CommentService(SqlAchemyAbstract):
    _db = None
    def __init__(self, db: AsyncSession = Depends(get_db)) :
        self._db = db
        self.set_model(CommentModel)
    
    async def create_comment(self, data: CommentModel, with_commit=True):
        try:
            result = await super().create(data, with_commit)
            return handler_response(200, data, "Tạo comment thành công")
        except Exception as e:
            return handler_response(500, None, str(e))
    
    async def search_cmt(self, rent_id: int = None, user_id: int = None, sort_schema: dict = None):
        query = select(CommentModel)
        if rent_id is not None:
            query = query.where(CommentModel.rent_id == rent_id)
        if user_id is not None:
            query = query.where(CommentModel.user_id == user_id)
        
        result = await self.search_with_raw_query(query=query, sort_schema=sort_schema)
        return_data = []
        for item in result:
            data = item.__dict__
            data.pop('_sa_instance_state')
            return_data.append(data)
        return return_data