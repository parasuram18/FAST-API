from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing_extensions import Annotated
from fastapi import Depends
from . import config

DATABASE_URL = config.DATABASE_URL

# engine = create_engine(DATABASE_URL)
engine = create_async_engine(DATABASE_URL)

# SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False, autoflush=False, autocommit=False)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as db:
        try:
            yield db
        finally:
            await db.close()



Connect_DB = Annotated[AsyncSession, Depends(get_db)]

