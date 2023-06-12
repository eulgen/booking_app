from fastapi import APIRouter,Depends,HTTPException,status,Body
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.auth_schema import TokenSchema,TokenPayload
from app.user_operations.user_operation import authentificate
from app.security.security import create_access_token,create_refresh_token
from app.dependencies.user_deps import get_current_user
from app.cnx_config.config import settings
from app.models.user_model import user
from app.schemas.user_schema import userOut,userIn
from typing import Any
from jose import jwt,JWTError
from pydantic import ValidationError


auth_route=APIRouter()


@auth_route.post("/login",summary="create access and refresh token",response_model=TokenSchema)
async def login(form_data:OAuth2PasswordRequestForm=Depends())->Any:
    User=await authentificate(form_data.username,form_data.password)
    if not User:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect Username or Password"
        )
        
    return{
        "access_token":create_access_token(User.user_id),
        "refresh_token":create_refresh_token(User.user_id)
    }


@auth_route.post("/refresh",summary="refresh the access token",response_model=TokenSchema)
async def refresh_token(refresh_token:str=Body(...)):
    try:
        payload=jwt.decode(
            refresh_token,
            settings.JWT_REFRESH_SECRET_KEY,
            settings.ALGORITHM
        )
        token_data=TokenPayload(**payload)
    except(JWTError,ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid token",
            headers={"WWW-Authentificate":"Bearer"}
        )
    User = await user.find_one(user.user_id==token_data.sub)
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid token for user"
        )
    return {
        "access_token":create_access_token(User.user_id),
        "refresh_token":create_refresh_token(User.user_id)
    }


@auth_route.post("/test_token",summary="Test if the token is valid",response_model=userOut)
async def test_token(User:userIn=Depends(get_current_user)):
    return User