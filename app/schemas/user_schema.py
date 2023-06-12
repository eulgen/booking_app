from pydantic import BaseModel,EmailStr,Field
from uuid import UUID
from typing import Optional


#Informations qui seront entrées par les utilisateurs
class userIn(BaseModel):
    email:EmailStr=Field(...,description="email input")
    username:str=Field(...,min_length=3,max_length=50)
    password:str=Field(...,min_length=3,max_length=50)
    first_name:Optional[str]=None
    last_name:Optional[str]=None


#Informations pouvant etre renvoyés en sortie
class userOut(BaseModel):
    user_id:UUID
    email:EmailStr
    username:str
    first_name:str
    last_name:str
    rule:str
