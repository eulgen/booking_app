from fastapi import APIRouter,Depends,HTTPException,status
from app.schemas.book_schema import bookIn,bookOut,pagination_bk
from app.models.book_model import  book
from app.models.user_model import user
from app.dependencies.user_deps import get_current_user
from app.book_operations.book_operation import new_book,find_books_for_users,find_all_books,find_book
from datetime import datetime
from typing import List,Dict
from app.cnx_config.config import settings


book_route=APIRouter()


@book_route.post("/create_book",summary="create a book",response_model=bookOut)
async def create_book(Book:bookIn,owner:user=Depends(get_current_user)):
    return await new_book(Book,owner)

@book_route.get("/get_book={booknameOrauthors}&page={page}&size={size}",summary="Get a book",response_model=pagination_bk)
async def get_book(booknameOrauthors:str,page:int=1,size:int=10):
    retrieve_book=await find_book(booknameOrauthors)
    for bk in retrieve_book:
        bk.view+=1
        await bk.update({"$set":bk.dict(exclude_unset=True)})
    len_books=len(retrieve_book)
    start=(page-1)*size
    end=start+size

    if end>len_books:
        raise HTTPException(
            status_code=404,
            detail="List of book not found"
        )
    if end==len_books:
        next_page=None
        
        if page>1:
            previous_page=f"http://127.0.0.1:8000/api/book/get_book={booknameOrauthors}&page={page-1}&size={size}"
        else:
            previous_page=None
    else:
        if page>1:
            previous_page=f"http://127.0.0.1:8000/api/book/get_book={booknameOrauthors}&page={page-1}&size={size}"
        else:
            previous_page=None
        
        next_page=f"http://127.0.0.1:8000/api/book/get_book={booknameOrauthors}&page={page+1}&size={size}"
    
    response_page=pagination_bk(
        list_book=retrieve_book[start:end],
        total=len_books,
        count=len_books/size,
        previous_page=previous_page,
        next_page=next_page
    )
    return response_page

@book_route.get("/get_books_for_user/page={page}&size={size}",summary="Get all user's books",response_model=pagination_bk)
async def get_books_for_user(User:user=Depends(get_current_user),page: int=1,size: int=10):
    books=await find_books_for_users(User)
    len_books=len(books)
    start=(page-1)*size
    end=start+size

    if end>len_books:
        raise HTTPException(
            status_code=404,
            detail="List of book not found"
        )
    if end==len_books:
        next_page=None
    
        if page>1:
            previous_page=f"http://127.0.0.1:8000/api/book/get_books_for_user/page={page-1}&size={size}"
        else:
            previous_page=None
    else:
        if page>1:
            previous_page=f"http://127.0.0.1:8000/api/book/get_books_for_user/page={page-1}&size={size}"
        else:
            previous_page=None
    
        next_page=f"http://127.0.0.1:8000/api/book/get_books_for_user/page={page+1}&size={size}"
    response_page=pagination_bk(
    list_book=books[start:end],
    total=len_books,
    count=len_books/size,
    previous_page=previous_page,
    next_page=next_page
    )
    
    return response_page

@book_route.get("/get_all_books",summary="Get all books",response_model=pagination_bk)
async def get_all_books(User:user=Depends(get_current_user),page:int=1,size:int=10):
    if User.rule=="admin":
        books= await find_all_books()
        len_books=len(books)
        start=(page-1)*size
        end=start+size

        if end>len_books:
            raise HTTPException(
                status_code=404,
                detail="List of book not found"
            )
        if end==len_books:
            next_page=None
        
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_all_books/page={page-1}&size={size}"
            else:
                previous_page=None
        else:
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_all_books/page={page-1}&size={size}"
            else:
                previous_page=None
        
            next_page=f"http://127.0.0.1:8000/api/book/get_all_books/page={page+1}&size={size}"
        response_page=pagination_bk(
        list_book=books[start:end],
        total=len_books,
        count=len_books/size,
        previous_page=previous_page,
        next_page=next_page
        )
        return response_page

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@book_route.get("/get_limited_books",summary="Get limited books",response_model=pagination_bk)
async def get_limited_books(User:user=Depends(get_current_user),size:int=10,page:int=1):
    if(User.rule=="admin"):
        books= await find_all_books()
        limited_books=[]
        for i in range(size):
            limited_books.append(books[i])
        len_books=len(limited_books)
        start=(page-1)*size
        end=start+size

        if end>len_books:
            raise HTTPException(
                status_code=404,
                detail="List of book not found"
            )
        if end==len_books:
            next_page=None
        
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_limited_books/page={page-1}&size={size}"
            else:
                previous_page=None
        else:
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_limited_books/page={page-1}&size={size}"
            else:
                previous_page=None
        
            next_page=f"http://127.0.0.1:8000/api/book/get_limited_books/page={page+1}&size={size}"
        response_page=pagination_bk(
        list_book=limited_books[start:end],
        total=len_books,
        count=len_books/size,
        previous_page=previous_page,
        next_page=next_page
        )
        return response_page

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@book_route.put("/update_book={book_name}",summary="update user's books",response_model=bookOut)
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

@book_route.delete("/delete_book={book_name}",summary="delete the user's book")
async def delete_book(book_name:str,User:user=Depends(get_current_user)):
    bk=await find_book(book_name,User)
    await bk.delete()
    return {"message":"successfully deleted"}

@book_route.post("/buy_book={book_name}",summary="buy the book")
async def buy_book(book_name: str):
    bk=await book.find_one(book.book_name==book_name)
    bk.books_sold+=1
    bk.copies-=1
    bk.stars=(bk.books_sold/settings.NUMBER_MAX_BOOKS_SOLD)%settings.MAX_STARS
    return {"books sold ":bk.books_sold,"copies":bk.copies}