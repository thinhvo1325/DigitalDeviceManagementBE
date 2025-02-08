from fastapi import APIRouter, Depends
from services.rent_service import RentService
from schemas.rent_schemas import RentCreateSchema, SortSchemas, RentSearchSchema, RentSChemas
from typing import Any
from cores.handler_response import response_return
from depends.authen import AuthenService
from services.rent_detail_service import RentDeailService
from unidecode import unidecode
router = APIRouter(
    prefix="/rent",
    tags=['Rent'],
    responses={404: {"description": "Not found"}},
)



@router.post("/create")
async def create(
    obj: RentCreateSchema,
    rent_service: RentService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    '''
    category: Danh mục \n
    title: Tiêu đề \n
    description: Mô tả\n
    
    images: Danh sách đường dẫn ảnh\n
    video: Danh sách đường dẫn video\n
    rent_price: [\n
        {\n
        "price": "100000",   \\\ Giá cho thuê\n
        "time": "for_1_days"      \\\ Thời gian cho thuê  (Gán cứng chuỗi trên)\n
        },\n
        {\n
        "price": "300000",   \\\ Giá cho thuê\n
        "time": "for_3_days"      \\\ Thời gian cho thuê (Gán cứng chuỗi trên)\n
        },\n
        {\n
        "price": "700000",   \\\ Giá cho thuê\n
        "time": "for_7_days"      \\\ Thời gian cho thuê (Gán cứng chuỗi trên)\n
        }\n
    ]\n
    
    address: địa chỉ\n
    cancel_policy: Điều khoản hủy bỏ 1: dễ dàng, 2: trung bình, 3: khó khăn\n
    sell_price: Giá bán FB\n
    '''
    obj = obj.dict()
    obj['user_id'] = authen.fake_user.id
    result  = await rent_service.create_rent(obj)
    return response_return(**result)

@router.get("/list")
async def list(
    obj: RentSearchSchema = Depends(),
    sort_schema: SortSchemas = Depends(),
    rent_service: RentService = Depends(),
    # authen: AuthenService = Depends()
) -> Any:
    obj = obj.dict()
    sort_schema = sort_schema.dict()
    
    if obj['rent_id'] is not None:
        result = await rent_service.find(obj['rent_id'])
        result = result.__dict__
        result.pop('_sa_instance_state')
        return response_return(200, result, "Tìm thấy thông tin")
    
    return_data = []
    if sort_schema['sort_by'] not in ['for_1_days', 'for_3_days', 'for_7_days']:
        result = await rent_service.search(order={sort_schema['sort_by']: sort_schema['order']}, is_get_first=False)
        text = obj['text']
        for r in result:
            r = r.__dict__
            r.pop('_sa_instance_state')
            if (text.strip().lower() in r['category'].strip().lower()) or \
                (unidecode(text.strip().lower()) in unidecode(r['category'].strip().lower())):
                return_data.append(r)
            elif (text.strip().lower() in r['title'].strip().lower()) or \
                (unidecode(text.strip().lower()) in unidecode(r['title'].strip().lower())):
                return_data.append(r)
            elif (text.strip().lower() in r['description'].strip().lower()) or \
                (unidecode(text.strip().lower()) in unidecode(r['description'].strip().lower())):
                return_data.append(r)
    else:
        result = await rent_service.search(is_get_first=False)
        data_merged = []
        for r in result:
            r = r.__dict__
            r.pop('_sa_instance_state')
            rent_price = r['rent_price']
            value = 0
            for price in rent_price:
                if price['time'] == sort_schema['sort_by']:
                    value = int(price['price'])
                    break
            data_merged.append((r, value))
        data_sorted = sorted(data_merged, key=lambda x: x[1], reverse=True if sort_schema['order'] == 'desc' else False)
        for r in data_sorted:
            if (text.strip().lower() in r['category'].strip().lower()) or \
                (unidecode(text.strip().lower()) in unidecode(r['category'].strip().lower())):
                return_data.append(r)
            elif (text.strip().lower() in r['title'].strip().lower()) or \
                (unidecode(text.strip().lower()) in unidecode(r['title'].strip().lower())):
                return_data.append(r)
            elif (text.strip().lower() in r['description'].strip().lower()) or \
                (unidecode(text.strip().lower()) in unidecode(r['description'].strip().lower())):
                return_data.append(r)
    return response_return(200, return_data, "Tìm thấy thông tin")  


@router.post("/rent")
async def rent(
    obj: RentSChemas,
    rent_deail_service: RentDeailService = Depends(),
    authen: AuthenService = Depends()
) -> Any:
    '''
    rent_id: id của rent\n
    quantity: số lượng thuê\n
    rent_price: theo for của sản phẩm \n
    Ví dụ: {\n
        "price": "300000",   \\\ Giá cho thuê\n
        "time": "for_3_days"      \\\ Thời gian cho thuê (Gán cứng chuỗi trên)\n
        },\n
    start_date: Thời gian bắt đầu thuê\n
    end_date: Thời gian kết thúc\n
    total_price: Tổng giá thuê\n
    '''
    obj = obj.dict()
    obj['user_id'] = authen.fake_user.id
    result  = await rent_deail_service.create_rent_detail(obj)
    return response_return(**result)