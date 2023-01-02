from hashlib import new
from typing import List, Optional
from uuid import UUID, uuid4
from pydantic import BaseModel
from enum import Enum


class Diet(str, Enum):
    gluten = "gluten"
    lactose = "lactose"
    vegan = "vegan"
    gluten_free = "gluten-free"
    lactose_free = "lactose-free"
    trace_gluten = "trace-gluten"
    trace_lactose = "trace-lactose"


class Role(str, Enum):
    admin = "admin"
    user = "user"


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    username: str
    password: str
    diets: List[Diet]


class Product(BaseModel):
    id: Optional[UUID] = uuid4()
    name: str
    ingredients: List[Diet]
    orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class RegisterRequest(BaseModel):
    username: str
    password: str
    diets: List[Diet]


# change password request
class ChangePasswordRequest(BaseModel):
    username: str
    old_password: str
    new_password: str
    new_password_confirmation: str
