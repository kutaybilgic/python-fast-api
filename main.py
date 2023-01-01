from hashlib import new
from typing import List

from sqlalchemy import null
from models import LoginRequest, RegisterRequest, User, Product, ChangePasswordRequest
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import jsondb
import prediction
from fastapi.middleware.cors import CORSMiddleware

#  uvicorn main:app --reload

app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


productdb: List[Product] = []
userDb: List[User] = []

# read productDb from json file and store it in produc  tdb
userdbfile = jsondb.read_json("userDb.json")
productdbfile = jsondb.read_json("productDb.json")

for product in productdbfile:
    a = Product(**product)
    productdb.append(a)

for user in userdbfile:
    b = User(**user)
    userDb.append(b)


# get all products from productdb
@app.get("/products")
async def get_product():
    return productdb


# get a product from productdb by product name
@app.get("/products/{product_name}")
async def get_product(product_name: str):
    return jsondb.find_product("productDb.json", product_name)


# post a product to productdb
@app.post("/products")
async def create_product(product: Product):
    productdb.append(product)
    jsondb.write_json("productDb.json", product)


# get all users from userdb
@app.get("/users")
async def get_users():
    return userDb


# get a user from userdb by user name
@app.get("/users/{user_name}")
async def get_user(user_name: str):
    return jsondb.find_user(user_name)


# post a user to userdb
@app.post("/users")
async def create_user(user: User):
    userDb.append(user)
    jsondb.write_json("userDb.json", user)


# post a photo
@app.post("/photo")
async def predict(file: UploadFile = File(...)):
    img = Image.open(file.file)
    res = prediction.predictionImage(img)
    print(res)
    found_product = jsondb.find_product("productDb.json", res)
    print(found_product)
    return found_product


@app.post("/signup")
async def signup(request: RegisterRequest):
    user = jsondb.find_user(request.username)
    if(user != None):
        return {"message": "User already exists"}
    # create a new user according to the request
    newUser = User(username=request.username,
                   password=request.password, diets=request.diets)
    # newUser = User(request.username, request.password, request.diets)
    userDb.append(newUser)
    jsondb.write_json("userDb.json", newUser)
    # return a http status code 200
    return {"message": "User created successfully"}


@app.post("/login")
async def login(requst: LoginRequest):
    user = jsondb.find_user(requst.username)
    if(user == None):
        return {"message": "User does not exist"}
    foundUser = User(**user)
    if(foundUser.password != requst.password):
        return {"message": "Wrong password"}
    return {"message": "User logged in"}


# change the password of a user
@app.put("/users")
async def change_password(request: ChangePasswordRequest):
    print(request.username)
    user = jsondb.find_user(request.username)
    if(user == None):
        return {"message": "User does not exist"}
    foundUser = User(**user)
    if(foundUser.password != request.old_password):
        return {"message": "Wrong password"}
    if(request.new_password != request.new_password_confirmation):
        return {"message": "New passwords do not match"}
    foundUser.password = request.new_password
    jsondb.write_json("userDb.json", foundUser)
    return {"message": "Password changed"}
