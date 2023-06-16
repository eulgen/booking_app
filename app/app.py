from beanie import init_beanie
from fastapi import FastAPI
from app.models.user_model import user
from app.models.book_model import book
from app.cnx_config.config import settings
from app.routes.api_route import api_route
from motor.motor_asyncio import AsyncIOMotorClient

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION
)

@app.get("/")
def hello():
    return {"message":"hello world"}

# `@app.on_event("startup")` is a decorator in FastAPI that registers a function to be executed when
# the application starts up. In this case, the function `app_init()` is registered to initialize
# crucial application services, such as connecting to the database and initializing Beanie (an async
# MongoDB ODM).
@app.on_event("startup")
async def app_init():
    
    db_client=AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING).Booking
    
    await init_beanie(
        database=db_client,
        document_models=[
            user,
            book
        ]
    )


# `app.include_router` is a method in FastAPI that allows you to include a router (a collection of
# routes/endpoints) in your application. In this case, it is including the `user_route` router with
# the prefix specified in the `settings` module and tagging it with the label "user route". This means
# that any requests to the specified prefix will be handled by the routes defined in the `user_route`
# router.
app.include_router(api_route,prefix=settings.API_ROUTE)