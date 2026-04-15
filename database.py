from motor.motor_asyncio import AsyncIOMotorClient

from dotenv import load_dotenv
import os 
load_dotenv()
MONGO_URL=os.getenv("MONGO_URL")

client=AsyncIOMotorClient(MONGO_URL)
db=client["myapp"]

user_collection=db["users"]
order_collection=db["orders"]


