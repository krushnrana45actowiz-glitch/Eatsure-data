from pymongo import MongoClient
import json

client = MongoClient("mongodb://localhost:27017/")

db = client["eatsure_db"]

collection = db["products"]

with open("all_brands_products.json", "r", encoding="utf-8") as f:
    data = json.load(f)

if isinstance(data, list):

    collection.insert_many(data)

else:

    collection.insert_one(data)

print("Data Inserted Successfully")