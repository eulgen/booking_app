from pydantic import BaseModel,Field
from typing import Optional
from datetime import datetime
from typing import List

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

class paginOut(BaseModel):
    list_book:List[bookOut]