from fastapi import FastAPI
# import
from src.routers.userroutes import router as user_router
from src.middleware.middleware import *
app = FastAPI()

app.include_router(user_router, prefix='/user')


# app.add_middleware(AuthMiddleware)