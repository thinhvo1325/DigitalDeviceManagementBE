from pydantic import BaseModel
from typing import Optional

class RentPriceSchema(BaseModel):
    price: Optional[str] = None
    time: Optional[str] = None

class RentCreateSchema(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    
    images: Optional[list] = None
    video: Optional[list] = None
    rent_price: Optional[list[RentPriceSchema]] = None
    
    address: Optional[str] = None
    cancel_policy: Optional[int] = None
    sell_price: Optional[str] = None
    
class RentSearchSchema(BaseModel):
    text: Optional[str] = ''

class SortSchemas(BaseModel):
    sort_by: Optional[str] = 'created_at'
    order: Optional[str] = 'desc'