from passlib.context import CryptContext
from jose import jwt
from datetime import datetime,timedelta
from app.cnx_config.config import settings
from typing import Union,Any


pass_context=CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def get_password(password:str)->str:
    return pass_context.hash(password)

def verify_password(password:str,hash_pass:str)->bool:
    return pass_context.verify(secret=password,hash=hash_pass)

def create_access_token(subject:Union[str,Any],expires_delta:int=None)->str:
    if expires_delta is not None:
        expires_delta=datetime.utcnow()+expires_delta
    else:
        expires_delta=datetime.utcnow()+timedelta(minutes=settings.ACCESS_TOKEN_EXPIRATION)
    to_encode={
        "exp":expires_delta,
        "sub":str(subject)
    }
    encode_jwt=jwt.encode(to_encode,settings.JWT_SECRET_KEY,settings.ALGORITHM)
    return encode_jwt

def create_refresh_token(subject:Union[str,Any],expires_delta:int=None)->str:
    if expires_delta is not None:
        expires_delta=datetime.utcnow()+expires_delta
    else:
        expires_delta=datetime.utcnow()+timedelta(minutes=settings.REFRESH_TOKEN_EXPIRES_MINUTES)
    to_encode={
        "exp":expires_delta,
        "sub":str(subject)
    }
    encode_jwt=jwt.encode(to_encode,settings.JWT_REFRESH_SECRET_KEY,settings.ALGORITHM)
    return encode_jwt