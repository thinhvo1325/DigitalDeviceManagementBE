from fastapi import APIRouter, Depends
from services.rent_service import RentService
from schemas.cart_schema import CartCreateSchema, UpdateCartSchema
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

@router.delete("/delete")
async def delete(
    id: int,
    cart_service: CartService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    result = await cart_service.delete(id)
    return response_return(200, {}, "Tạo thông tin giỏ hàng thành công")

@router.put("/update")
async def update(
    obj: UpdateCartSchema,
    cart_service: CartService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    for data in obj.data:
        result = await cart_service.update(data.ids, data={"is_paid": 2,
                                                           "days": data.days,
                                                           "price": data.price})
        
    
    # Send email with updated items information
    email_content = "Bạn đã thanh toán thành công:\n"
    for data in obj.data:
        item = await cart_service.search(fields={'id': data.ids}, is_get_first=True)
        email_content += f"Sản phẩm: {item.title}, Số ngày thuê: {data.days}, Giá: {data.price}\n"
        
    from mail import send_email
        # Assuming you have a function to send email
    send_email(authen.fake_user.email, email_content)
    return response_return(200, {}, "Tạo thông tin giỏ hàng thành công")