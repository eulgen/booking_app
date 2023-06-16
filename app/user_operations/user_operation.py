from fastapi import HTTPException,status
from app.schemas.user_schema import userIn
from app.models.user_model import user
from app.security.security import get_password,verify_password
from pydantic import EmailStr
from typing import List,Optional
from uuid import UUID


# The `async def create_user(new_user:userIn)->user` function is creating a new user in the database.
# It takes a `userIn` object as input, which contains the user's information such as username, email,
# password, first name, and last name. It then creates a new `user` object with the provided
# information and inserts it into the database. Finally, it returns the newly created `user` object.
async def create_user(new_user:userIn)->user:
    if new_user.password=="admin":
        data_user=user(**new_user.dict(),hash_pass=get_password(new_user.password),rule="admin")
    else:
        data_user=user(**new_user.dict(),hash_pass=get_password(new_user.password),rule="user")
    return await data_user.insert()    

# The `async def find_user(email:EmailStr)->user` function is finding a user in the database by their
# email address. It takes an email address as input and returns a user object if found. If the user is
# not found, it raises an HTTPException with a 404 status code and a "User not found" detail message.
async def find_user(email:EmailStr)->user:
    try:
        return await user.find_one(user.email==email)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )


async def find_user_username(username:str)->user:
    try:
        return await user.find_one(user.username==username)
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

# `async def find_users()-> List[user]` is a function that finds all users in the database and returns
# a list of `user` objects. It uses the `find_all()` method of the `user` model to retrieve all users
# and then converts the result to a list. The function returns this list of `user` objects.
async def find_users()-> List[user]:
    users=await user.find_all().to_list()
    return users


# `async def authentificate(username:str, password:str)->user` is a function that authenticates a user
# by their username and password. It takes a username and password as input and returns a `user`
# object if the authentication is successful. It first calls the `find_user_username` function to find
# the user by their username. If the user is not found, it returns `None`. If the user is found, it
# verifies the password using the `verify_password` function from the `security` module. If the
# password is not valid, it returns `None`. If the authentication is successful, it returns the `user`
# object.
async def authentificate(username:str, password:str)->user:
    User=await find_user_username(username)
    if not User:
        return None
    if not verify_password(password,User.hash_pass):
        return None
    
    return User

"""async def authentificate(email:EmailStr, password:str)->user:
    User=await find_user(email)
    if not User:
        return None
    if not verify_password(password,User.hash_pass):
        return None
    
    return User"""


async def get_user_by_id(id:UUID) -> Optional[user]:
    User=await user.find_one(user.user_id==id)
    return User