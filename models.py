from pydantic import BaseModel,EmailStr,Field
from typing import Annotated,Optional
from enum import Enum


class MessageResponse(BaseModel):
  message:str

class TokenResponse(BaseModel):
    token:  str
    refresh_token:  str
    token_type:  str

class UserResponse(BaseModel):
    user_name: str
    user_email: str
    user_phoneno: int
    user_role: str

class Product(BaseModel):
  product_name:str="unknown"
  product_price:int

class Role(str,Enum):
  USER="user"
  ADMIN="admin"
  SELLER="seller"  

class User(BaseModel):
  user_name:str
  user_email:EmailStr
  user_password:str
  user_phoneno:Annotated[int,Field(...,description="Enter Your phone no here")]
  user_role:Role=Role.USER



class UpdateUser(BaseModel):
  name:Optional[str]#mistake optional nhi baanya 
  email:Optional[EmailStr]
  phoneno:Optional[int]

class LogIn(BaseModel):
  email:str
  password:str


class OrderStatus(str,Enum):
  PENDING="pending"
  DELIEVERD="delievered"
  SHIPPED="shipped"
  CANCELED="CANCELLED"
  RETURNED="returned"
  
class Order(BaseModel):
  name_of_product:str
  quantity:int
  status:OrderStatus=OrderStatus.PENDING

class Update_Order_status(str,Enum):
  state:OrderStatus