import psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="stock_exchange",
    user="postgres",
    password="Password@16"
)

cursor = conn.cursor()

cursor.execute("SELECT * FROM Orders")

orders = cursor.fetchall()

print("\nORDERS TABLE\n")

for order in orders:
    print(order)

cursor.close()
conn.close()