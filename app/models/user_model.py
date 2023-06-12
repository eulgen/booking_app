from beanie import Document,Indexed
from uuid import UUID,uuid4
from datetime import datetime
from pydantic import EmailStr,Field
from typing import Optional

class user(Document): 
    
    user_id:UUID=Field(default_factory=uuid4)
    username:Indexed(str,unique=True)
    hash_pass:str=None
    first_name:Optional[str]=None
    last_name:Optional[str]=None
    email:Indexed(EmailStr,unique=True)
    rule:str=None
    registered_at:datetime=Field(default_factory=datetime.utcnow)
    update_at:datetime=Field(default_factory=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"<user {self.email}>"

    def __str__(self) -> str:
        return self.email

    def __hash__(self) -> int:
        return hash(self.email)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, user):
            return self.email == other.email
        return False
    
    @classmethod
    async def by_email(self,email:str)->"user":
        return await self.find_one(self.email==email)
    
    class Collection:
        name="Users"