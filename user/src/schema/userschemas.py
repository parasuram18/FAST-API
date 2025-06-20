from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

# for custom error response
class ErrorRes(BaseModel):
    status : Optional[str] = "error"
    message : Optional[str] = "Something went wrong"

# input for role entry
class RoleInput(BaseModel):
    role_name : str
    description : str

# rolemaster response
class RoleRes(BaseModel):
    id : int
    role_name : str

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
    # role
    address : address

# user details response
class UserResponse(BaseModel):
    id : int
    email : EmailStr
    mobilenumber : str
    
    model_config = ConfigDict(from_attributes=True)

class MapRole(BaseModel):
    user : int
    role : int

class MapRes(BaseModel):
    status : Optional[str] = "success"
    message : Optional[str] = "User mappeed succesfully"

# login input
class Login(BaseModel):
    username : str
    password : str

class Token(BaseModel):
    access_token : str
    token_type : str
    model_config = ConfigDict(from_attributes=True)
