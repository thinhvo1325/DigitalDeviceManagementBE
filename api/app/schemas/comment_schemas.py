from pydantic import BaseModel
from typing import Optional

class CommentCreateSchemas(BaseModel):
    rent_id: Optional[int]
    username: Optional[str] = None
    product_name: Optional[str] = None
    star: Optional[int] = None
    content: Optional[str] = None

class CommentSearchSchemas(BaseModel):
    rent_id: Optional[int] = None
    user_id: Optional[int] = None
    

class SortSchemas(BaseModel):
    sort_by: Optional[str] = 'created_at'
    order: Optional[str] = 'desc'