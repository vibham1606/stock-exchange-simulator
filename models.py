from pydantic import BaseModel

class Order(BaseModel):
    order_id: int
    user_id: int
    order_type: str
    price: int
    quantity: int
    stock_id: int

class User(BaseModel):
    user_id: int
    name: str
    balance: int