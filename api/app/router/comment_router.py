from fastapi import APIRouter, Depends
from services.comment_service import CommentService
from schemas.comment_schemas import CommentCreateSchemas, CommentSearchSchemas, SortSchemas
from typing import Any
from cores.handler_response import response_return
from depends.authen import AuthenService
from unidecode import unidecode
router = APIRouter(
    prefix="/comment",
    tags=['Comment'],
    responses={404: {"description": "Not found"}},
)



@router.post("/create")
async def create(
    obj: CommentCreateSchemas,
    comment_service: CommentService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    obj = obj.dict()
    obj['user_id'] = authen.fake_user.id
    result  = await comment_service.create_comment(obj)
    return response_return(**result)


@router.get("/list")
async def list(
    obj: CommentSearchSchemas = Depends(),
    sort_schema: SortSchemas = Depends(),
    comment_service: CommentService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    obj = obj.dict()
    sort_schema = sort_schema.dict()
    reuslt = await comment_service.search_cmt(rent_id=obj['rent_id'], user_id=obj['user_id'], sort_schema=sort_schema)
    return response_return(200, reuslt, "Tìm thấy thông tin")  