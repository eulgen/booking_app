from pydantic import BaseSettings
from decouple import config

class Settings(BaseSettings):
    
    JWT_SECRET_KEY:str=config("JWT_SECRET_KEY",cast=str)
    JWT_REFRESH_SECRET_KEY:str=config("JWT_REFRESH_SECRET_KEY",cast=str)
    ALGORITHM="HS256"
    ACCESS_TOKEN_EXPIRATION=15 # minutes
    REFRESH_TOKEN_EXPIRES_MINUTES:int = 60*24*7 # 7 days
    
    #Routes
    API_ROUTE:str="/api"
    
    # Api settings
    PROJECT_NAME:str="Booking"
    VERSION:str="v4"
    API:str="/Booking"
    
    #Database
    MONGO_CONNECTION_STRING:str=config("MONGO_CONNECTION_STRING",cast=str)
    
    NUMBER_MAX_BOOKS_SOLD=1000000
    MAX_STARS=5
    
    class Config:
        case_sensitive=True



settings = Settings()