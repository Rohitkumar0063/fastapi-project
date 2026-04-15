from fastapi import Depends,HTTPException

from dotenv import load_dotenv
import os
load_dotenv()

from jose import jwt,JWTError
from datetime import datetime, timedelta



from database import user_collection
from fastapi.security import OAuth2PasswordBearer


SECRET_KEY =os.getenv("SECRET_KEY")
REFRESH_SECRET_KEY=os.getenv("REFRESH_SECRET_KEY")
ALGORITHM = "HS256"

oauth2scheme=OAuth2PasswordBearer(tokenUrl="/login")
async def  get_current_user(token:str=Depends(oauth2scheme)):
  
  try:
    payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])

    email=payload.get("sub")

    if not email:
      raise HTTPException(status_code=401,detail="Invalid token")
    
  except JWTError:
    raise HTTPException(status_code=401, detail="Token invalid")
  
  user =await user_collection.find_one({"email": email})

  if user is None:
        raise HTTPException(status_code=404, detail="User not found")

  return user


def create_token(data:dict):
  to_encode=data.copy()
  expire=datetime.utcnow()+timedelta(minutes=30)
  to_encode.update({"exp":expire})
  token=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
  return token

def refresh_token(data:dict):
   to_encode=data.copy()
   expire = datetime.utcnow() + timedelta(days=7)
   to_encode.update({"exp":expire})
   token=jwt.encode(to_encode,REFRESH_SECRET_KEY,algorithm="HS256")
   return token
   
  
  

  
