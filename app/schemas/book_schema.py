from pydantic import BaseModel,Field
from typing import Optional,List
from datetime import datetime
from app.models.book_model import book

class bookIn(BaseModel):
    book_name:str=Field(...,title="Book name",min_length=5,max_length=100)
    authors:str=Field(...,title="Authors",min_length=5,max_length=100)
    description:Optional[str]=None
    copies:int=0
    price:int=0


class bookOut(BaseModel):
    book_name:str
    authors:str
    description:str
    copies:int
    price:int
    books_sold:int=0
    view:int
    registered_at:datetime
    update_at:datetime

class pagination_bk(BaseModel):
    list_book:List[bookOut]
    total:int=0
    count:int=0
    previous_page:str=None
    next_page:str=None