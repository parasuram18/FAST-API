from src.schema.userschemas import *
from src.models.usermodels import *
from fastapi import APIRouter, HTTPException, status
from typing import Optional, Union, List
from src.core.database import Connect_DB
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, and_, or_

router = APIRouter()

@router.post('/role', response_model=Union[RoleRes, ErrorRes])
async def add_role(data : RoleInput, db : Connect_DB):
    try:
        role_obj = RoleMaster(**data.model_dump())
        db.add(role_obj)
        try:
            db.commit()
            db.refresh(role_obj)
            return role_obj
        
        except IntegrityError as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Role already exists"
            )
            # custom error response
            # return ErrorRes(status="error", message="role already exists")
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

@router.get('/role', response_model=List[RoleRes])
async def get_all_roles(db : Connect_DB):
    roles = (await db.execute(select(RoleMaster))).scalars().all()
    return roles

@router.post('/register', response_model=Union[UserResponse, ErrorRes], summary='register user')
async def register(data:RegisterUser, db : Connect_DB):
    try:
        userobj = CustomUser(mobilenumber=data.mobilenumber, email=data.email)
        userobj.set_password(data.password)
        db.add(userobj)
        await db.flush()

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

@router.get('/', summary="get_all_users", response_model=Union[UserResponse, List[UserResponse], ErrorRes])
async def create_blog(db : Connect_DB, id : Optional[int] = None):
    try:
        if id is not None:
            result = await db.execute(select(CustomUser).where(CustomUser.id == id))
            data = result.scalar_one_or_none()
            profileobj = data.profile
            print(profileobj.firstname)

            roles = data.roles
            print(roles)

        else:
            data = (await db.execute(select(CustomUser))).scalars().all()

        return data
    except Exception as e:
        return ErrorRes(status='error', message=str(e))