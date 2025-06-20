import jwt, os
from datetime import datetime, timedelta
from ..core.database import Connect_DB, AsyncSessionLocal
from sqlalchemy import select
from ..models.usermodels import *
from dotenv import load_dotenv
from ..core import config
from fastapi import HTTPException, Request, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, OAuth2PasswordBearer
from typing_extensions import Annotated

SECRET_KEY = config.SECRET_KEY
JWT_ALGORITHM = config.JWT_ALGORITHM
JWT_EXPIRE_TIME = config.JWT_EXPIRE_TIME

bearer = HTTPBearer()
http_security =Annotated[HTTPAuthorizationCredentials, Depends(bearer)]
          
# use it for protected endpoints
oauth2 = OAuth2PasswordBearer(tokenUrl='/user/login/')

# authenticate users in every request, act like a middleware
# protected routes deprnds on this function
async def oauth2_security(request:Request, db:Connect_DB, token : str = Depends(oauth2)):
    try:
        user_id = (await validate_token(token)).get("user_id")
        result = await db.get(CustomUser, user_id)
        if result is not None:
            request.scope['user'] = result
        else:
            request.scope['user'] = None

    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        print(str(e))
        raise HTTPException(status_code=401, detail="Authentication failed")
    




async def payload_handler(userobj, db):

    roleobj = await db.execute(select(RoleMaster).where(RoleMaster.id==userobj.roles[0].role))
    role = roleobj.scalar().role_name

    payload = {
        "user_id" : userobj.id,
        "email" : userobj.email,
        "role" : role,
        "exp" : datetime.utcnow() + timedelta(seconds=JWT_EXPIRE_TIME) 
    }
    return payload

async def genetare_token(userobj, db):
    
    payload = await payload_handler(userobj, db)
    token = jwt.encode(payload, SECRET_KEY, JWT_ALGORITHM)

    return token

async def validate_token(token):
    try:
        
        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        return payload
    
    except jwt.ExpiredSignatureError:
        return JSONResponse(status_code=401, content={"detail":"Token Expired"})
    except jwt.InvalidTokenError:
        return JSONResponse(status_code=401, content={"detail":"Invalid token"})

async def get_user_role(request):
    try:
        
        token = dict(request.headers).get('authorization').split(' ')[1]

        payload = jwt.decode(token, key=SECRET_KEY, algorithms=[JWT_ALGORITHM])
        
        return payload.get('role')
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=401, detail="Token Expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401, detail="Invalid token"
        )
    
async def get_user_by_id(user_id, db:Connect_DB):
    result = await db.execute(select(CustomUser).where(CustomUser.id==user_id))
    obj = result.scalar_one_or_none()
    return obj