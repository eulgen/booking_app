from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.book_schema import bookIn,bookOut
from app.models.book_model import  book
from app.models.user_model import user
from app.dependencies.user_deps import get_current_user
from app.book_operations.book_operation import new_book,find_books_for_users,find_all_books,find_book,read_bks
from datetime import datetime
from typing import List,Dict
from app.cnx_config.config import settings
from pymongo import MongoClient
import json


book_route=APIRouter()


@book_route.post("/create_book",summary="create a book",response_model=bookOut)
async def create_book(Book:bookIn,owner:user=Depends(get_current_user)):
    return await new_book(Book,owner)

@book_route.get("/get_book",summary="Get a book")
async def get_book(booknameOrauthors:str,page:int=1,size: int=1)-> Dict[str,bookOut]:
    retrieve_book=await find_book(booknameOrauthors)
    for bk in retrieve_book:
        bk.view+=1
        await bk.update({"$set":bk.dict(exclude_unset=True)})
    client=MongoClient("mongodb://localhost:27017/")
    db=client["Booking"]
    col=db["books"]
    #print(f"type : {col.find_one()}")
    x=col.find_one()
    return {"message":x}

@book_route.get("/get_books_for_user",summary="Get all user's books")
async def get_books_for_user(page: int=1,size: int=5,User:user=Depends(get_current_user)):
    books=await find_books_for_users(User)

@book_route.get("/get_all_books",summary="Get all books",response_model=List[bookOut])
async def get_all_books(User:user=Depends(get_current_user)):
    if User.rule=="admin":
        return await find_all_books()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@book_route.get("/get_limited_books",summary="Get limited books",response_model=List[bookOut])
async def get_limited_books(User:user=Depends(get_current_user),number:int=1):
    if(User.rule=="admin"):
        books= await find_all_books()
        limited_books=[]
        for i in range(number):
            limited_books.append(books[i])
        return limited_books
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@book_route.put("/update_book",summary="update user's books",response_model=bookOut)
async def update_book(bk:bookIn,book_name:str,User:user=Depends(get_current_user)):
    last_bk=await find_book(book_name,User)
    new_bk=book(id=bk.id,
                book_id=last_bk.book_id,
                book_name=bk.book_name,
                authors=bk.authors,
                description=bk.description,
                copies=bk.copies,
                price=bk.price,
                update_at=datetime.utcnow(),
                owner=User) 
    await last_bk.update({"$set":new_bk.dict(exclude_unset=True)})
    return last_bk

@book_route.delete("/delete_book",summary="delete the user's book")
async def delete_book(book_name:str,User:user=Depends(get_current_user)):
    bk=await find_book(book_name,User)
    await bk.delete()
    return {"message":"successfully deleted"}

@book_route.post("/buy_book",summary="buy the book")
async def buy_book(book_name: str):
    bk=await book.find_one(book.book_name==book_name)
    bk.books_sold+=1
    bk.copies-=1
    bk.stars=(bk.books_sold/settings.NUMBER_MAX_BOOKS_SOLD)%settings.MAX_STARS
    return {"books sold ":bk.books_sold,"copies":bk.copies}