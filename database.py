from colorama import Cursor
import pymongo
import json
from pymongo import MongoClient
import models


client = MongoClient('mongodb://localhost:27017/')
mydb = client['hci']
collection_users = mydb['users']
collection_products = mydb['products']


async def fetch_one_user(user_id):
    return await collection_users.find_one({"_id": user_id})


def fech_all_users():
    return collection_users.find()


async def fetch_one_product(product_id):
    return await collection_products.find_one({"_id": product_id})


async def fetch_all_products():
    products = []
    cursor = collection_products.find({})
    async for product in cursor:
        products.append(models.Product(**product))
    return products
