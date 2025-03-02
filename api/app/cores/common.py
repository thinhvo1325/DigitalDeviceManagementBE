from datetime import datetime, timedelta
import json
import os
from fastapi import HTTPException
import os


SPLID_DATE_CHAR = '/'
DATE_FORMAT = SPLID_DATE_CHAR.join(['%Y', '%m', '%d'])
SPLID_DATETIME_CHAR = ' '
DATETIME_FORMAT = SPLID_DATETIME_CHAR.join([DATE_FORMAT, '%H:%M:%S'])
ES_DATE_FORMAT = 'yyyy/MM/dd HH:mm:ss||yyyy/MM/dd||yyyy/MM||yyyy'
USER_RECORD_EXPIRED_DAYS = 1


def dump_str_to_date_format(value: str = None, clock: bool = True):
    date_format = ''
    if value:
        try:
            date_format = '%Y'
            value = datetime.strptime(value, date_format)
        except Exception:
            try:
                date_format = SPLID_DATE_CHAR.join(['%Y', '%m'])
                value = datetime.strptime(value, date_format)
            except Exception:
                try:
                    date_format = DATE_FORMAT
                    value = datetime.strptime(value, date_format)
                except Exception:
                    try:
                        if not clock:
                            return ResponseHandler(status_code=422,
                                                   detail="Wrong format. Format must be in this list['%Y', '%Y/%m', '%Y/%m/%d']")

                        date_format = DATETIME_FORMAT
                        value = datetime.strptime(value, date_format)
                    except Exception:
                        return ResponseHandler(status_code=422,
                                       detail="Wrong format. Format must be in this list['%Y', '%Y/%m', '%Y/%m/%d', '%Y/%m/%d %H:%M:%S']")

    return {
        'value': value,
        'format': date_format,
    }

def ResponseHandler(status_code: int = 200, **kwargs):
    '''
        status_code: status trả về vd: 200, 400,... (mặc định là 200)
        detail: chi tiết lỗi trả về. Nên trả về khi status_code là status_code lỗi
        **kwargs: data trả về
    '''
    if 200 <= status_code <= 500:
        return {'data': kwargs}
    if 'detail' not in kwargs:
        print('Error detail must be included')

    raise HTTPException(status_code=status_code, detail=kwargs.get('detail', ''))


from jose import JWTError, jwt as jose_jwt

def create_token(data: dict):
    encoded_jwt = jose_jwt.encode(data, '1122334455', algorithm='HS256')
    return encoded_jwt

def create_access_token(expires_delta: timedelta | None = None):
    to_encode = {'id': 1}

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=9999999)
    to_encode.update({"exp": expire})
    encoded_jwt = jose_jwt.encode(to_encode, os.environ['SECRET_KEY'], algorithm='HS256')
    return encoded_jwt


def create_token_authen(service: str):
    if service == 'profile':
        target_ip = os.environ['TARGET_PROFILE_IP']
    elif service == 'user':
        target_ip = os.environ['TARGET_USER_IP']
    else:
        raise HTTPException(status_code=404, detail='Invalid service url')
    
    user_token = jose_jwt.encode({"service_name": "be-tva-service"}, os.environ['SECRET_KEY'], algorithm='HS256')
    payload = {
        'origin_ip': os.environ['ORIGIN_IP'],
        'target_ip': target_ip,
        'user_token': user_token
    }
    token = jose_jwt.encode(payload, os.environ['PRIVATE_KEY'])
    return token

def decode_JWT(token: str, with_secret_key: bool = True):
    try:
        return jose_jwt.decode(token, key=None, options={"verify_signature":False})
    except JWTError as e:
        return ResponseHandler(status_code=403, detail='Invalid token')