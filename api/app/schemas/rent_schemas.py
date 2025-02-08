from pydantic import BaseModel
from typing import Optional
from datetime import datetime
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
    rent_id: Optional[int] = None

class SortSchemas(BaseModel):
    sort_by: Optional[str] = 'created_at'
    order: Optional[str] = 'desc'
    

class RentSChemas(BaseModel):
    rent_id: Optional[int] = None
    quantity: Optional[int] = None
    rent_price: Optional[RentPriceSchema] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    total_price: Optional[str] = None