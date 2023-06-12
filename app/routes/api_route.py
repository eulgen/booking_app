#Les routes définis ici concerne uniquement les utilisateurs

from fastapi import APIRouter
from app.routes.user_route import user_route
from app.routes.auth_route import auth_route
from app.routes.book_route import book_route


api_route = APIRouter()

"""@api_route.get("/")
# `def test()` is defining a function named `test` that returns a dictionary with a message "hello
# world" when the route defined by `@user_route.get("/")` is accessed.
def test():
    return {"message":"hello world"}
"""

api_route.include_router(user_route,prefix="/user",tags=["user"])
api_route.include_router(auth_route,prefix="/auth",tags=["auth"])
api_route.include_router(book_route,prefix="/book",tags=["book"])