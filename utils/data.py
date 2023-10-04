import os
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(os.getenv("MONGO_URL"), server_api=ServerApi("1"))
database = client["tir_bot"]

def ping_database():
    try:
        client.admin.command("ping")
        print("Database connected!")
    except Exception as err:
        print(err)
