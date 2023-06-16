from fastapi import APIRouter,HTTPException,status,Depends
from app.schemas.user_schema import userIn,userOut,pagination_usr
from app.models.user_model import user
from app.user_operations.user_operation import create_user,find_user,find_users
from app.security.security import get_password
from app.dependencies.user_deps import get_current_user
from pydantic import EmailStr
from datetime import datetime
from typing import List
from math import ceil

user_route = APIRouter()


@user_route.post("/create_user",summary="creation of user",response_model=userOut)
async def route_create_user(new_user:userIn):
    return await create_user(new_user)

@user_route.get("/get_user",summary="get one user",response_model=user)
async def get_user(User=Depends(get_current_user)):
    User=await find_user(User.email)
    return User.__dict__


"""@user_route.get("/get_all_users",summary="get all users")
async def get_users()->list:
    return await find_users()"""



@user_route.get("/get_all_users/page={page}&size={size}",summary="get all users",response_model=List[userOut])
async def get_users(User:user=Depends(get_current_user),page: int=1,size: int=10):
    if(User.rule=="admin"):
        retrieve_user=await find_users()
        len_books=len(retrieve_user)
        start=(page-1)*size
        end=start+size

        if end==len_books:
            next_page=None
        
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_all_users/page={page-1}&size={size}"
            else:
                previous_page=None
        else:
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_all_users/page={page-1}&size={size}"
            else:
                previous_page=None
        
        if end>len_books:
            next_page=None
        
            next_page=f"http://127.0.0.1:8000/api/book/get_all_users/page={page+1}&size={size}"
        
        response_page=pagination_usr(
            list_book=retrieve_user[start:end],
            total=len_books,
            count=ceil(len_books/size),
            previous_page=previous_page,
            next_page=next_page
        )
        return response_page

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@user_route.get("/get_limited_users/page={page}&size={size}",summary="get limited users",response_model=pagination_usr)
async def get_limited_users(User:user=Depends(get_current_user),page: int=1,size:int=10):
    if(User.rule=="admin"):
        users= await find_users()
        limited_users=[]
        for i in range(size):
            limited_users.append(users[i])

        len_books=len(limited_users)
        start=(page-1)*size
        end=start+size

        if end==len_books:
            next_page=None
        
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_limited_users/page={page-1}&size={size}"
            else:
                previous_page=None
        else:
            if page>1:
                previous_page=f"http://127.0.0.1:8000/api/book/get_limited_users/page={page-1}&size={size}"
            else:
                previous_page=None
        
            next_page=f"http://127.0.0.1:8000/api/book/get_all_users/page={page+1}&size={size}"
        
        if end>len_books:
            next_page=None
        
        response_page=pagination_usr(
            list_book=limited_users[start:end],
            total=len_books,
            count=ceil(len_books/size),
            previous_page=previous_page,
            next_page=next_page
        )
        return response_page

    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@user_route.put("/update_user",summary="updating the user",response_model=userOut)
async def route_update_user(User:userIn,new_user:user=Depends(get_current_user)):
    new_user.username=User.username
    new_user.email=User.email
    new_user.hash_pass=get_password(User.password)
    new_user.first_name=User.first_name
    new_user.last_name=User.last_name
    new_user.update_at=datetime.utcnow()
    if User.password=="admin":
        new_user.rule="admin"
    else: new_user.rule="user"
    await new_user.update({"$set":new_user.dict(exclude_unset=True)})
    return new_user

@user_route.delete("/delete_user",summary="delete the user")
async def route_delete_user(User:user=Depends(get_current_user)):
    user_data=await find_user(User.email)
    if(user_data.rule=="admin"):
        await user_data.delete()
        return {"message":"correctly deleted"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )