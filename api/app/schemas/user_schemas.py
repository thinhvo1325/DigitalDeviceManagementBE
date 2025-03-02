from pydantic import BaseModel
from typing import Optional

class LoginSchema(BaseModel):
    username: str
    password: str   
    is_google: Optional[bool] = False

class UserCreateSchema(BaseModel):
    fullname: Optional[str]
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    username: Optional[str]
    password: Optional[str]



class UserUpdateSchema(BaseModel):
    password: Optional[str] = None
    fullname: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    email: Optional[str] = None
    new_password: Optional[str] = None
