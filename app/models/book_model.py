from beanie import Document,Indexed,Link
from uuid import UUID,uuid4
from pydantic import Field
from typing import Optional
from datetime import datetime
from app.models.user_model import user


class book(Document):

    book_id:UUID=Field(default_factory=uuid4,unique=True)
    book_name:Indexed(str,unique=True)
    authors:str
    copies:int
    price:int
    description:str=Optional[str]
    view:Optional[int]=0
    stars:Optional[int]=0
    books_sold:Optional[int]=0
    registered_at:datetime=Field(default_factory=datetime.utcnow)
    update_at:datetime=Field(default_factory=datetime.utcnow)
    owner:Link[user]

    def __repr__(self) -> str:
        return f"<Book name {self.book_name}>"

    def __str__(self) -> str:
        return self.book_name

    def __hash__(self) -> int:
        return hash(self.book_name)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, book):
            return self.book_id == other.book_id
        return False
    
    class Collection:
        name="books"