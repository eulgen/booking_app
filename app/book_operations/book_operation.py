from app.models.user_model import user
from app.schemas.book_schema import bookIn,bookOut
from app.models.book_model import book
from typing import List,Any
from fastapi import HTTPException,status



async def new_book(Book:bookIn,owner:user)->book:
    new_bk=book(**Book.dict(),owner=owner)
    return await new_bk.insert()

async def find_book(booknameOrauthors:str)->List[book]:
    books=await find_all_books()
    found_bk=[]
    for bk in books:
        if (booknameOrauthors.lower() in bk.authors.lower())or(booknameOrauthors.lower() in bk.book_name.lower()):
            found_bk.append(bk)
    return found_bk

async def find_books_for_users(User:user)->List[book]:
    books=await book.find(book.owner.user_id==User.user_id).to_list()
    if len(books)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Books not found"
        )
    else: return books

async def find_all_books()->List[book]:
    books=await book.find_all().to_list()
    if len(books)==0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Books not found"
        )
    else: return books

"""async def pagging_data(bks: List[bookOut],page: int=1,size: int=5)-> dict:
    start=(page-1)*size
    end=start+size
    length_bks=len(bks)
    response={
        "data":bks[start:end],
        "total":length_bks,
        "count":size,
        "pagination":{}
    }
    return response"""


def read_bks(bks: List[bookOut],page: int=1,size: int=5):
    start=(page-1)*size
    end=start+size
    len_bks=len(bks)
    
    response={
        "data":bks[start:end],
        "total":len_bks,
        "count":size,
        "pagination":{}
    }
    
    if end>=len_bks:
        response["pagination"]["next"]=None
        
        if page>1:
            response["pagination"]["previous"]=f"posts?page_num={page-1}&page_size={size}"
        else:
            response["pagination"]["previous"]=None
    else:
        if page>1:
            response["pagination"]["previous"]=f"posts?page_num={page-1}&page_size={size}"
        else:
            response["pagination"]["previous"]=None
        
        response["pagination"]["next"]=f"posts?page_num={page+1}&page_size={size}"
    
    return response
