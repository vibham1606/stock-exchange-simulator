import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="stock_exchange",
    user="postgres",
    password="Password@16"
)

cursor = conn.cursor()

user_id = int(input("Enter User ID: "))
name = input("Enter Name: ")
balance = int(input("Enter Balance: "))
shares = int(input("Enter Shares: "))

cursor.execute(
    """
    INSERT INTO Users(user_id,name,balance,shares)
    VALUES(%s,%s,%s,%s)
    """,
    (user_id,name,balance,shares)
)

conn.commit()

print("User Added Successfully!")

cursor.close()
conn.close()