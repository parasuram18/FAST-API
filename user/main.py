from fastapi import FastAPI
# import
from src.routers.userroutes import router as user_router

app = FastAPI()

app.include_router(user_router, prefix='/user')
