from fastapi import APIRouter, Depends
from schemas.user_schemas import UserCreateSchema, UserUpdateSchema, LoginSchema
from services.user_service import UserService
from depends.authen import AuthenService
from typing import Any
from cores.handler_response import response_return
router = APIRouter(
    prefix="/users",
    tags=['User'],
    responses={404: {"description": "Not found"}},
)

@router.get("/info")
async def info(
    user_service: UserService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    result =  await user_service.find(authen.fake_user.id)
    result = result.__dict__
    result.pop('_sa_instance_state')
    return response_return(200, result, "Tìm thấy user")

@router.post("/login")
async def login(
    obj: LoginSchema,
    user_service: UserService = Depends()
) -> Any:
    result  = await user_service.find_user(**obj.model_dump())
    return response_return(**result)

@router.post('/create')
async def create_users(
    obj: UserCreateSchema, 
    user_service: UserService = Depends()
) -> Any:
    result =  await user_service.create_user(obj)
    return response_return(**result)


@router.put("/update")
async def update_users(
    obj: UserUpdateSchema, 
    user_service: UserService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    result =  await user_service.update_user(authen.fake_user.id, obj.__dict__)
    return response_return(**result)


@router.delete("/delete")
async def delete_users(
    id:int,
    user_service: UserService = Depends()
) -> Any:
    result =  await user_service.delete_user(id)
    return response_return(**result)
