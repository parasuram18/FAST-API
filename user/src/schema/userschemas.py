from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# for custom error response
class ErrorRes(BaseModel):
    status : str
    message : str

# input for role entry
class RoleInput(BaseModel):
    role_name : str
    description : str

# rolemaster response
class RoleRes(BaseModel):
    id : int
    role : str

    model_config = ConfigDict(from_attributes=True)

# user address
class address(BaseModel):
    address1 : Optional[str] = None
    address2 : Optional[str] = None
    landmark : Optional[str] = None
    city : Optional[str] = None
    district : str
    pincode : Optional[str] = None

# create user
class RegisterUser(BaseModel):
    first_name : Optional[str] = None
    last_name : Optional[str] = None
    age : Optional[int] = None
    gender : Optional[str] = None
    mobilenumber : str
    email : EmailStr
    password : str
    address : address

# user details response
class UserResponse(BaseModel):
    id : int
    email : EmailStr
    mobilenumber : str
    
    model_config = ConfigDict(from_attributes=True)
