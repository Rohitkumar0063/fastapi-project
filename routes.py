from models import Product,User,UpdateUser,Order,LogIn,Role,Update_Order_status,MessageResponse,TokenResponse,UserResponse
from jose import jwt,JWTError
from database import user_collection,order_collection
from fastapi import APIRouter,Depends,HTTPException
router=APIRouter(tags=["Orders"])
from auth import get_current_user,create_token,refresh_token,REFRESH_SECRET_KEY,ALGORITHM
from hashing import verify,hashing_password
from bson import ObjectId



@router.post("/register_user",response_model=MessageResponse)
async def create_user(new_user:User):
  dumping=new_user.model_dump()
  dumping["password"]=hashing_password(dumping["password"])
  await user_collection.insert_one(dumping)
  return {"message":"user created successfully"}

@router.get("/get_all_users")
async def get_all_users(page:int=1,limit:int=10,current_user: User = Depends(get_current_user)):
  if (current_user ["role"] != Role.ADMIN.value) :
    raise HTTPException(status_code=403,detail="Not Allowed")
  skip=(page-1)*10
  users = []
  async for user in user_collection.find().skip(skip).limit(limit):
        user["_id"] = str(user["_id"])
        users.append(user)
  
  total = await user_collection.count_documents({})

  return {
        "page": page,
        "limit": limit,
        "total_users": total,
        "total_pages": -(-total // limit),
        "users": users
    }

@router.get("/user/{user_id}/{email}",response_model=UserResponse)
async def get_specific_user(user_id:str,email:str,current_user: User = Depends(get_current_user)):
  if (current_user ["role"] != Role.ADMIN.value and current_user ["email"]!= email):
    raise HTTPException(status_code=403,detail="Not Allowed")
  data= await user_collection.find_one({"email":email,"user_id":user_id})
  if not data:
    raise HTTPException(status_code=404,detail="user not found")
  data.pop("_id",None)
  return data
  
@router.patch("/update_user_values/{email}")
async def update_values(email:str,user:UpdateUser,current_user: User = Depends(get_current_user)):
  if current_user["role"] !=Role.ADMIN.value and current_user["email"]!=email:
    raise HTTPException(status_code=403,detail="Not Allowed")
  
  update_data=user.model_dump(exclude_unset=True)
  
  data=await user_collection.find_one({"email":email}) 

  if not data:
    return {"message":"user not found"}
  
  await user_collection.update_one(
    {"email":email},
    {"$set":update_data}

  )
  return {"message": "User updated successfully"}

# @app.get("/get_order")
# async def get_order()

@router.post("/create_order")
async def create_order(new_order:Order,current_user: User = Depends(get_current_user)):
  dumping=new_order.model_dump()
  dumping["user_id"]=current_user["email"]
  result =await order_collection.insert_one(dumping)
  return {"message":"order created successfully",
          "order_id":str(result.inserted_id)
          }


@router.get("/get_order")
async def get_order(page:int=1,limit:int=10,current_user:User=Depends(get_current_user)):
  if current_user["role"]!=Role.ADMIN.value:
   raise HTTPException(status_code=403,detail="You are not admin to view all these details")
  

  skip=(page-1)*limit

  orders=[]
  async for order in order_collection.find().skip(skip).limit(limit):
    order["_id"] = str(order["_id"])
    orders.append(order)

  total=await order_collection.count_documents({})
  return {
          "page": page,
        "limit": limit,
        "total_orders": total,
        "total_pages": -(-total // limit),  # ceiling division
        "orders": orders
  }


@router.get("/get_order/{order_id}")
async def get_specific_order(order_id:str,current_user=Depends(get_current_user)):
  order=await order_collection.find_one({"_id":ObjectId(order_id)})
  if not order:
        raise HTTPException(status_code=404, detail="Order not found")
  if current_user["role"] != Role.ADMIN.value and order["user_id"] !=current_user["email"]:
    raise HTTPException(status_code=403, detail="Not allowed")
  order["_id"]=str(order["_id"])
  return order

@router.patch("/update_order_status/{order_id}/status")
async def update_status(order_id:str,status:Update_Order_status,current_user=Depends(get_current_user)):
  data=await order_collection.find_one({"_id":ObjectId(order_id)})
  if not data:
    raise HTTPException(status_code=404, detail="Order not found")
  
  if current_user["role"]!=Role.ADMIN.value and data["user_id"]!=current_user["email"]:
    raise HTTPException(status_code=403, detail="Not allowed")
    
  await order_collection.update_one(
    {"_id": ObjectId(order_id)},
        {"$set": {"status": status.value}}
  )#update_one 2 para leta hai which one and what to change
  return {"message": "Order status updated"}

    


@router.post("/login",response_model=TokenResponse)
async def login(values:LogIn):

  data=await user_collection.find_one({"email":values.email})
  if data==None:
    raise HTTPException(status_code=404,detail="User email or Passowrd is wrong ")
  if not verify(values.password,data["password"]):
    raise HTTPException(status_code=401,detail="Wrong Password")
  access_token=create_token({"sub":values.email})
  refreshtoken=refresh_token({"sub":values.email})
  return{
    "token":access_token,
    "refresh_token":refreshtoken,
    "token_type":"bearer",
    "message":"login successful"}

@router.post("/refresh")
async def refresh_token(refresh_token:str):
  try:
    payload=jwt.decode(refresh_token,REFRESH_SECRET_KEY,ALGORITHM)
    email=payload.get("sub")
    if not email:
      raise HTTPException(status_code=401, detail="Invalid refresh token")
  except JWTError:
    raise HTTPException(status_code=401, detail="Refresh token expired or invalid")
  #checking agar db mai user hai ya nhi there is a strong reason bheind it 
  user_check=await user_collection.find_one({"email":email})
  if not user_check:
    raise HTTPException(status_code=404, detail="User not found")
  new_access_token=create_token({"sub":user_check["email"]})
  return {"access_token": new_access_token, "token_type": "bearer"}

@router.delete("/delete_user/{email}")
async def delete_user(email:str,current_user=Depends(get_current_user)):
  if current_user["role"]!=Role.ADMIN.value and current_user["email"]!=email:
    raise HTTPException(status_code=403, detail="Not allowed")
  data= await user_collection.find_one({"email":email})
  if not data:
    raise HTTPException(status_code=404, detail="User not found")
  await user_collection.delete_one({"email": email})
  return {"message": "User deleted successfully"}




@router.delete("/delete_order/{order_id}")
async def delete_user(user_id:str,current_user=Depends(get_current_user)):

  data=order_collection.find_one({"id":ObjectId["order_id"]})
  if not data:
    raise HTTPException
  if data["role"] != Role.ADMIN.value and current_user["email"]!= user_id:
    return {"message":"not authorized"}
    
  await order_collection.delete_one({"order":data["user_id"]})
  return ({"message":"done deletion"})