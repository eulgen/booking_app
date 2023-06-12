from fastapi import APIRouter,HTTPException,status,Depends
from app.schemas.user_schema import userIn,userOut
from app.models.user_model import user
from app.user_operations.user_operation import create_user,find_user,find_users
from app.security.security import get_password
from app.dependencies.user_deps import get_current_user
from pydantic import EmailStr
from datetime import datetime


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



@user_route.get("/get_all_users",summary="get all users")
async def get_users(User:user=Depends(get_current_user))->list:
    if(User.rule=="admin"):
        return await find_users()
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Requires administrator rights"
        )

@user_route.get("/get_limited_users",summary="get limited users")
async def get_limited_users(User:user=Depends(get_current_user),number:int=1)->list:
    if(User.rule=="admin"):
        users= await find_users()
        limited_users=[]
        for i in range(number):
            limited_users.append(users[i])
        return limited_users
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