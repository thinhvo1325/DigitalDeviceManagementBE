from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RentPriceSchema(BaseModel):
    price: Optional[str] = None
    time: Optional[str] = None
    
class CartCreateSchema(BaseModel):
    title: Optional[str] = None
    image: Optional[str] = None
    days: Optional[int] = None
    price: Optional[int] = None
    is_paid: Optional[int] = 1
    rent_price: Optional[list[RentPriceSchema]] = None
    
    