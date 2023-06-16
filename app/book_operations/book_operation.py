from app.models.user_model import user
from app.schemas.book_schema import bookIn
from app.models.book_model import book
from typing import List
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
    books=await book.find(book.owner.id==User.id).to_list()
    print(f"len books:{len(books)}\n")
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