from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = None
db = None

def connect_to_mongo():
    global client, db
    if not client:
        client = MongoClient(MONGO_URI)
        db = client["fastapi_notes"]
        print("Connected to MongoDB")
