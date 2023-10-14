from fastapi import FastAPI
import databases
import sqlalchemy
from pydantic import BaseModel, Field
from typing import List
from models import User, UserIn, Goods, GoodsIn, Order, OrderIn
from sqlalchemy import ForeignKey

DATABASE_URL = "sqlite:///mydatabase.db"
database = databases.Database(DATABASE_URL)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(DATABASE_URL)
metadata.create_all(engine)
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

users = sqlalchemy.Table("users", metadata,
                         sqlalchemy.Column(
                             "id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("name", sqlalchemy.String(32)),
                         sqlalchemy.Column("surname", sqlalchemy.String(32)),
                         sqlalchemy.Column("email", sqlalchemy.String(128)),
                         sqlalchemy.Column("password", sqlalchemy.String(32)),
                         )

goods = sqlalchemy.Table("goods", metadata,
                         sqlalchemy.Column(
                             "id", sqlalchemy.Integer, primary_key=True),
                         sqlalchemy.Column("title", sqlalchemy.String(32)),
                         sqlalchemy.Column(
                             "description", sqlalchemy.String(128)),
                         sqlalchemy.Column("price", sqlalchemy.Float),
                         )

orders = sqlalchemy.Table("orders", metadata,
                          sqlalchemy.Column(
                              "id", sqlalchemy.Integer, primary_key=True),
                          sqlalchemy.Column(
                              "user_id", sqlalchemy.Integer, ForeignKey('users.id')),
                          sqlalchemy.Column(
                              "good_id", sqlalchemy.Integer, ForeignKey('goods.id')),
                          sqlalchemy.Column(
                              "date_of_order", sqlalchemy.String(32)),
                          sqlalchemy.Column(
                              "status", sqlalchemy.String(32))
                          )

engine = sqlalchemy.create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
metadata.create_all(engine)


@app.get("/create_notes/")
async def create_notes():
    query = users.insert().values(name="Dmitriy", surname="Solenkov",
                                  email='SolDm@mail.ru', password='password')
    await database.execute(query)
    query = users.insert().values(name="Alex", surname="Ivanov",
                                  email='IvAl@mail.ru', password='password')
    await database.execute(query)
    query = users.insert().values(name="Max", surname="Stepanov",
                                  email='StMa@mail.ru', password='password')
    await database.execute(query)
    query = goods.insert().values(title="Toothbrush", description="Very usefull thing",
                                  price='2.49')
    await database.execute(query)
    query = goods.insert().values(title="Toothpaste", description="You need a toothbrush to use it",
                                  price='7.19')
    await database.execute(query)
    query = goods.insert().values(title="Coke", description="Refreshing!",
                                  price='0.69')
    await database.execute(query)
    query = orders.insert().values(user_id="2", good_id="1",
                                   date_of_order="2023-10-10", status="Closed")
    await database.execute(query)
    query = orders.insert().values(user_id="1", good_id="3",
                                   date_of_order="2022-01-27", status="In delivery")
    await database.execute(query)


@app.get("/users/", response_model=List[User])
async def read_users():
    query = users.select()
    return await database.fetch_all(query)


@app.get("/goods/", response_model=List[Goods])
async def read_goods():
    query = goods.select()
    return await database.fetch_all(query)


@app.get("/orders/", response_model=List[Order])
async def read_orders():
    query = orders.select()
    return await database.fetch_all(query)


@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    query = users.select().where(users.c.id == user_id)
    return await database.fetch_one(query)


@app.get("/goods/{goods_id}", response_model=Goods)
async def read_goods(goods_id: int):
    query = goods.select().where(goods.c.id == goods_id)
    return await database.fetch_one(query)


@app.get("/orders/{order_id}", response_model=Order)
async def read_order(order_id: int):
    query = orders.select().where(orders.c.id == order_id)
    return await database.fetch_one(query)


@app.post("/users/", response_model=User)
async def create_user(user: UserIn):
    query = users.insert().values(name=user.name, surname=user.surname,
                                  email=user.email, password=user.password)
    last_record_id = await database.execute(query)
    return {**user.dict(), "id": last_record_id}


@app.post("/goods/", response_model=Goods)
async def create_goods(good: GoodsIn):
    query = goods.insert().values(title=good.title, description=good.description,
                                  price=good.price)
    last_record_id = await database.execute(query)
    return {**good.dict(), "id": last_record_id}


@app.post("/orders/", response_model=Order)
async def create_order(order: OrderIn):
    query = orders.insert().values(user_id=order.user_id, good_id=order.good_id,
                                   date_of_order=order.date_of_order, status=order.status)
    last_record_id = await database.execute(query)
    return {**order.dict(), "id": last_record_id}


@app.put("/users/{user_id}", response_model=User)
async def update_user(user_id: int, new_user: UserIn):
    query = users.update().where(users.c.id == user_id).values(**new_user.dict())
    await database.execute(query)
    return {**new_user.dict(), "id": user_id}


@app.put("/goods/{good_id}", response_model=Goods)
async def update_good(good_id: int, new_good: GoodsIn):
    query = goods.update().where(goods.c.id == good_id).values(**new_good.dict())
    await database.execute(query)
    return {**new_good.dict(), "id": good_id}


@app.put("/orders/{order_id}", response_model=Order)
async def update_order(order_id: int, new_order: OrderIn):
    query = orders.update().where(orders.c.id == order_id).values(**new_order.dict())
    await database.execute(query)
    return {**new_order.dict(), "id": order_id}


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    query = users.delete().where(users.c.id == user_id)
    await database.execute(query)
    return {'message': 'User deleted'}


@app.delete("/goods/{good_id}")
async def delete_good(good_id: int):
    query = goods.delete().where(goods.c.id == good_id)
    await database.execute(query)
    return {'message': 'Good deleted'}


@app.delete("/orders/{order_id}")
async def delete_order(order_id: int):
    query = orders.delete().where(orders.c.id == order_id)
    await database.execute(query)
    return {'message': 'Order deleted'}
