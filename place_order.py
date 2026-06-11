import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="stock_exchange",
    user="postgres",
    password="Password@16"
)

cursor = conn.cursor()

order_id = int(input("Enter Order ID: "))
user_id = int(input("Enter User ID: "))
order_type = input("BUY or SELL: ").upper()
price = int(input("Enter Price: "))
quantity = int(input("Enter Quantity: "))

cursor.execute(
    """
    INSERT INTO Orders
    (order_id,user_id,order_type,price,quantity)
    VALUES(%s,%s,%s,%s,%s)
    """,
    (order_id,user_id,order_type,price,quantity)
)

conn.commit()

print("Order Added Successfully!")

cursor.close()
conn.close()