from src.schema.userschemas import *
from src.models.usermodels import *
from fastapi import APIRouter, HTTPException, status, Header, Request
from typing import Optional, Union, List
from src.core.database import Connect_DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, or_
from .auth import * #genetare_token, validate_token, get_current_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

@router.post('/role', response_model=Union[RoleRes, ErrorRes], status_code=status.HTTP_201_CREATED, dependencies=[Depends(oauth2_security)])
async def add_role(data : RoleInput, db : Connect_DB):
    try:
        role_obj = RoleMaster(**data.model_dump())
        db.add(role_obj)
        try:
            await db.commit()
            await db.refresh(role_obj)
            return role_obj
        
        except IntegrityError as e:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already exists"
            )
            # custom error response
            # return ErrorRes(status="error", message="role already exists")
    except Exception as e:
        return ErrorRes(status="Error", message=str(e))

@router.get('/role', response_model=List[RoleRes], dependencies=[Depends(oauth2_security)])
async def get_all_roles(request:Request, db : Connect_DB):
    roles = (await db.execute(select(RoleMaster))).scalars().all()
    return roles

# public
@router.post('/register', response_model=Union[UserResponse, ErrorRes], summary='register user')
async def register(data:RegisterUser, db : Connect_DB):
    try:
        userobj = CustomUser(mobilenumber=data.mobilenumber, email=data.email)
        userobj.set_password(data.password)
        db.add(userobj)
        await db.flush()

        # mapp default role as customer
        rolemapobj = RoleMapping(role=2, user=userobj.id)
        db.add(rolemapobj)
        # add user profile details
        profileobj = UserPersonalProfile(firstname=data.first_name, lastname=data.last_name, age=data.age, gender=data.gender, address=data.address)
        profileobj.address = data.address.dict()
        profileobj.user_id = userobj.id
        db.add(profileobj)

        await db.commit()
        await db.refresh(userobj)

        return userobj
    except Exception as e:
        await db.rollback()
        return ErrorRes(status='error', message=str(e))

@router.get('/', summary="get_all_users", response_model=Union[UserResponse, List[UserResponse], ErrorRes], dependencies=[Depends(oauth2_security)])#, dependencies=[Depends(oauth2_security)])
async def get_all_users(request:Request, db : Connect_DB, id : Optional[int] = None):
    try:
        if id is not None:
            result = await db.execute(select(CustomUser).where(CustomUser.id == id))
            data = result.scalar_one_or_none()
            if data == None:
                return ErrorRes(status="success", message="No user Found")
        else:
            data = (await db.execute(select(CustomUser))).scalars().all()

        return data
    except Exception as e:
        return ErrorRes(message=str(e))
    
@router.post('/map_role', response_model=Union[MapRes, ErrorRes], dependencies=[Depends(oauth2_security)])
async def map_role( request:MapRole, db:Connect_DB):
    try:
        mapobj = RoleMapping(**request.model_dump())
        db.add(mapobj)
        try:
            await db.commit()
            await db.refresh(mapobj)
            return MapRes()
        except IntegrityError:
            await db.rollback()
            return ErrorRes(message="Role Already mapped")
    except Exception as e:
        return ErrorRes(message=str(e))
    
#public
@router.post('/login', response_model=Token)
async def login(db:Connect_DB, request : OAuth2PasswordRequestForm = Depends()):
    data = await db.execute(select(CustomUser).where(CustomUser.email==request.username))
    user = data.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Invalid Credentials"
        )
    if not user.check_password(request.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail= "Incorrect password"
        )
    token = await genetare_token(user, db)

    return Token(access_token=token, token_type="bearer")



