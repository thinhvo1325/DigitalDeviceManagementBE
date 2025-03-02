from fastapi import APIRouter, Depends
from services.rent_service import RentService
from schemas.cart_schema import CartCreateSchema
from typing import Any
from cores.handler_response import response_return
from depends.authen import AuthenService
from services.cart_service import CartService
from unidecode import unidecode
import base64
import os
from uuid import uuid4
router = APIRouter(
    prefix="/cart",
    tags=['Cart'],
    responses={404: {"description": "Not found"}},
)



@router.post("/create")
async def create(
    obj: CartCreateSchema,
    cart_service: CartService = Depends(),
    authen: AuthenService = Depends()
) -> Any:

    obj = obj.dict()
    obj['user_id'] = authen.fake_user.id
    result = await cart_service.create(obj)
    result = result.__dict__
    result.pop('_sa_instance_state')
    return response_return(200, result, "Tạo thông tin giỏ hàng thành công")



@router.get("/list")
async def list(
    is_paid: int = 1,
    cart_service: CartService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    result = await cart_service.search(fields={'user_id': authen.fake_user.id, 'is_paid': is_paid}, is_get_first=False)
    return_data = []
    for r in result:
        r = r.__dict__
        r.pop('_sa_instance_state')
        return_data.append(r)
    return response_return(200, return_data, "Tạo thông tin giỏ hàng thành công")