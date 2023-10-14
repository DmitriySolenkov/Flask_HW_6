from pydantic import BaseModel, Field
from sqlalchemy import ForeignKey


class UserIn(BaseModel):
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


class User(BaseModel):
    id: int
    name: str = Field(max_length=32)
    surname: str = Field(max_length=32)
    email: str = Field(max_length=128)
    password: str = Field(max_length=32)


class GoodsIn(BaseModel):
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float = Field(ge=0.01, le=100000)


class Goods(BaseModel):
    id: int
    title: str = Field(max_length=32)
    description: str = Field(max_length=128)
    price: float = Field(ge=0.01, le=100000)


class OrderIn(BaseModel):
    user_id: int = Field(ge=1)
    good_id: int = Field(ge=1)
    date_of_order: str = Field(max_length=10)
    status: str = Field(max_length=32)


class Order(BaseModel):
    id: int
    user_id: int = Field(ge=1)
    good_id: int = Field(ge=1)
    date_of_order: str = Field(max_length=10)
    status: str = Field(max_length=32)
