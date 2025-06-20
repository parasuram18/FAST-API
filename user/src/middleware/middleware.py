from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from ..core.database import AsyncSessionLocal
from ..core.config import *
import jwt
from ..models.usermodels import CustomUser


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        auth = request.headers.get("Authorization")
        request.scope['user'] = None

        if auth and auth.startswith("Bearer "):
            token = auth.split(" ")[1]

            try:
                user_id = jwt.decode(token, SECRET_KEY, algorithms=["HS256"]).get("user_id")
                # Get DB session
                async with AsyncSessionLocal() as session:
                    result = await session.get(CustomUser, user_id)
                if result:
                    # request.user = result
                    request.scope['user'] = result 

            except jwt.ExpiredSignatureError:
                return JSONResponse(status_code=401, content={"detail":"Token Expired"})
            except jwt.InvalidTokenError:
                return JSONResponse(status_code=401, content={"detail":"Invalid token"})
            except Exception as e:
                print(str(e))
                return JSONResponse(status_code=401, content={"detail":"Authentication failed"})
            
        return await call_next(request)
