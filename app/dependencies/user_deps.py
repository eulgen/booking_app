from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,HTTPException,status
from app.cnx_config.config import settings
from app.schemas.auth_schema import TokenPayload
from app.user_operations.user_operation import get_user_by_id
from app.models.user_model import user
from datetime import datetime
from jose import jwt
from pydantic import ValidationError




# `reusable_auth` is an instance of `OAuth2PasswordBearer` class from the `fastapi.security` module.
# It is used to define the authentication scheme for the API and to specify the token URL for the
# login endpoint. It is also used as a dependency for the `get_current_user` function to extract the
# JWT token from the request header and validate it.
reusable_auth=OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_ROUTE}/auth/login",
    scheme_name="JWT"
)

# `async def get_current_user(token:str=Depends(reusable_auth))` is a function that extracts the JWT
# token from the request header and validates it. It uses the `reusable_auth` instance of the
# `OAuth2PasswordBearer` class to define the authentication scheme for the API and to specify the
# token URL for the login endpoint. The function then decodes the JWT token using the `jwt.decode`
# method from the `jose` module and validates the token payload using the `TokenPayload` schema from
# the `app.schemas.auth_schema` module. If the token is valid, the function retrieves the user
# information from the database using the `get_user_by_id` function from the
# `app.user_operations.user_operation` module and returns the user object. If the token is invalid or
# expired, the function raises an HTTPException with the appropriate status code and error message.
async def get_current_user(token:str=Depends(reusable_auth)) -> user:
    try:
        payload=jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp)<datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                details="Token expired",
                headers={"WWW-Authentificate":"Bearer"}
            )
    
    except(jwt.JWTError,ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authentificate":"Bearer"}
        )
        
    User=await get_user_by_id(token_data.sub)
    
    if not User:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Could not find user"
        )
    
    return User