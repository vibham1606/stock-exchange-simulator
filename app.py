from fastapi import FastAPI
import psycopg2
from models import Order
from matching_engine import run_matching
from models import Order, User
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = psycopg2.connect(
    host="localhost",
    database="stock_exchange",
    user="postgres",
    password="Password@16"
)

cursor = conn.cursor()

@app.get("/")
def home():
    return {"message": "Stock Exchange Simulator Running"}

@app.get("/users")
def get_users():

    cursor.execute("""
    SELECT * FROM Users
    """)

    users = cursor.fetchall()

    result = []

    for user in users:

        result.append({
        "user_id": user[0],
        "name": user[1],
        "balance": user[2],
        "shares": user[3]
    })

    return result

@app.get("/orders")
def get_orders():

    cursor.execute("""
    SELECT * FROM Orders
    """)

    orders = cursor.fetchall()

    result = []

    for order in orders:

        result.append({
        "order_id": order[0],
        "user_id": order[1],
        "order_type": order[2],
        "price": order[3],
        "quantity": order[4],
        "stock_id": order[5]
    })

    return result

@app.get("/trades")
def get_trades():

    cursor.execute("""
    SELECT * FROM Trades
    """)

    trades = cursor.fetchall()

    result = []

    for trade in trades:

        result.append({
        "trade_id": trade[0],
        "buyer_id": trade[1],
        "seller_id": trade[2],
        "trade_price": trade[3],
        "quantity": trade[4]
    })

    return result

@app.get("/stocks")
def get_stocks():

    cursor.execute("""
    SELECT * FROM Stocks
    """)

    stocks = cursor.fetchall()

    result = []

    for stock in stocks:

        result.append({
            "stock_id": stock[0],
            "symbol": stock[1]
        })

    return result

@app.get("/portfolio/{user_id}")
def get_portfolio(user_id: int):

    cursor.execute("""
    SELECT
        Stocks.symbol,
        Portfolio.quantity
    FROM Portfolio
    JOIN Stocks
    ON Portfolio.stock_id = Stocks.stock_id
    WHERE Portfolio.user_id = %s
    """,
      (user_id,))

    portfolio = cursor.fetchall()

    result = []

    for row in portfolio:

     result.append({
        "stock": row[0],
        "quantity": row[1]
        })

    return result



@app.post("/order")
def place_order(order: Order):

    cursor.execute("""
    INSERT INTO Orders
    (order_id,user_id,order_type,price,quantity,stock_id)
    VALUES(%s,%s,%s,%s,%s,%s)
    """,
    (
        order.order_id,
        order.user_id,
        order.order_type,
        order.price,
        order.quantity,
        order.stock_id
    ))

    conn.commit()

    return {"message": "Order Added Successfully"}

@app.post("/match")
def match_orders():

    run_matching()

    return {"message": "Matching Engine Executed Successfully"}

@app.get("/orderbook")
def get_orderbook():

    cursor.execute("""
    SELECT
        Orders.order_id,
        Users.name,
        Stocks.symbol,
        Orders.price,
        Orders.quantity
    FROM Orders
    JOIN Users
    ON Orders.user_id = Users.user_id
    JOIN Stocks
    ON Orders.stock_id = Stocks.stock_id
    WHERE Orders.order_type = 'BUY'
    ORDER BY Orders.price DESC
    """)

    buy_orders = cursor.fetchall()

    cursor.execute("""
    SELECT
        Orders.order_id,
        Users.name,
        Stocks.symbol,
        Orders.price,
        Orders.quantity
    FROM Orders
    JOIN Users
    ON Orders.user_id = Users.user_id
    JOIN Stocks
    ON Orders.stock_id = Stocks.stock_id
    WHERE Orders.order_type = 'SELL'
    ORDER BY Orders.price ASC
    """)

    sell_orders = cursor.fetchall()

    return {
        "buy_orders": [
            {
                "order_id": row[0],
                "user": row[1],
                "stock": row[2],
                "price": row[3],
                "quantity": row[4]
            }
            for row in buy_orders
        ],

        "sell_orders": [
            {
                "order_id": row[0],
                "user": row[1],
                "stock": row[2],
                "price": row[3],
                "quantity": row[4]
            }
            for row in sell_orders
        ]
    }

@app.post("/user")
def create_user(user: User):

    cursor.execute("""
    INSERT INTO Users
    (user_id,name,balance,shares)
    VALUES(%s,%s,%s,%s)
    """,
    (
        user.user_id,
        user.name,
        user.balance,
        0
    ))

    conn.commit()

    return {
        "message": "User Created Successfully"
    }


@app.delete("/order/{order_id}")
def delete_order(order_id: int):

    cursor.execute("""
    DELETE FROM Orders
    WHERE order_id = %s
    """,
    (order_id,))

    conn.commit()

    return {
        "message": "Order Deleted Successfully"
    }

@app.get("/health")
def health():

    return {
        "status": "running"
    }